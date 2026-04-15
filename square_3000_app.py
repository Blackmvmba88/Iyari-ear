#!/usr/bin/env python3
import cgi
import html
import os
import shutil
import subprocess
import tempfile
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

HOST = "127.0.0.1"
PORT = int(os.environ.get("SQUARE_3000_PORT", "8765"))
TARGET = "3000x3000"
BASE_DIR = Path(tempfile.mkdtemp(prefix="square_3000_"))
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "output"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def convert_to_square_3000(input_path: Path) -> Path:
    output_path = OUTPUT_DIR / f"{input_path.stem}_{TARGET}{input_path.suffix or '.jpg'}"
    cmd = [
        "sips",
        "--cropToHeightWidth",
        "3000",
        "3000",
        "--resampleHeightWidth",
        "3000",
        "3000",
        str(input_path),
        "--out",
        str(output_path),
    ]
    subprocess.run(cmd, check=True, capture_output=True, text=True)
    return output_path


def page(message: str = "", download: str = "") -> str:
    link = ""
    if download:
        link = f'<p><a class="btn" href="/download?file={html.escape(download)}">Descargar resultado</a></p>'
    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Crop 3000x3000</title>
  <style>
    body{{font-family:system-ui,-apple-system,sans-serif;background:#0b0f14;color:#e8eef6;margin:0;padding:32px}}
    .card{{max-width:720px;margin:0 auto;background:#111823;border:1px solid #243040;border-radius:18px;padding:24px;box-shadow:0 18px 60px rgba(0,0,0,.35)}}
    h1{{margin:0 0 8px;font-size:28px}}
    p{{line-height:1.5;color:#b8c3d1}}
    form{{display:grid;gap:14px;margin-top:20px}}
    input[type=file]{{padding:12px;background:#0e1620;border:1px solid #263242;border-radius:12px;color:#dce7f3}}
    button,.btn{{display:inline-block;background:#4ce1a1;color:#06110c;border:0;border-radius:12px;padding:12px 16px;font-weight:700;text-decoration:none;cursor:pointer}}
    .msg{{margin-top:16px;padding:12px 14px;background:#0e1620;border:1px solid #263242;border-radius:12px}}
    .small{{font-size:13px;color:#91a3b7}}
  </style>
</head>
<body>
  <div class="card">
    <h1>Crop 3000x3000</h1>
    <p>Sube una imagen, haz clic una vez y se genera una versión cuadrada exacta de <strong>3000x3000</strong>.</p>
    <form action="/process" method="post" enctype="multipart/form-data">
      <input type="file" name="image" accept="image/*" required>
      <button type="submit">Generar 3000x3000</button>
    </form>
    {link}
    {f'<div class="msg">{html.escape(message)}</div>' if message else ''}
    <p class="small">Procesa al centro con `sips` y guarda el resultado localmente.</p>
  </div>
</body>
</html>"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/download":
            params = parse_qs(parsed.query)
            filename = params.get("file", [""])[0]
            file_path = OUTPUT_DIR / Path(filename).name
            if file_path.exists():
                self.send_response(200)
                self.send_header("Content-Type", "application/octet-stream")
                self.send_header("Content-Disposition", f'attachment; filename="{file_path.name}"')
                self.end_headers()
                with open(file_path, "rb") as f:
                    shutil.copyfileobj(f, self.wfile)
            else:
                self.send_error(404, "Archivo no encontrado")
            return

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(page().encode("utf-8"))

    def do_POST(self):
        if self.path != "/process":
            self.send_error(404, "Ruta no encontrada")
            return

        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={"REQUEST_METHOD": "POST", "CONTENT_TYPE": self.headers.get("Content-Type")},
        )

        field = form["image"] if "image" in form else None
        if field is None or not getattr(field, "filename", ""):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(page("Falta seleccionar una imagen.").encode("utf-8"))
            return

        input_name = Path(field.filename).name
        input_path = UPLOAD_DIR / input_name
        with open(input_path, "wb") as out:
            shutil.copyfileobj(field.file, out)

        try:
            output_path = convert_to_square_3000(input_path)
            msg = f"Listo: {output_path.name}"
            download = output_path.name
        except subprocess.CalledProcessError as exc:
            msg = f"Error procesando imagen: {exc.stderr or exc.stdout or exc}"
            download = ""

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(page(msg, download).encode("utf-8"))

    def log_message(self, format, *args):
        return


def main():
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    url = f"http://{HOST}:{PORT}"
    print(f"Abriendo {url}")
    threading.Timer(0.5, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
