# Repository Guidelines

## Project Structure & Module Organization
- `image_tool.py`: Python CLI for image ops (resize, crop, tile, mirror, ocr). Exposes `PRESETS`.
- `webui.py`: Gradio UI using Pillow and optional `PRESETS` import.
- `index.html`, `js/matrix.js`, `styles/style.css`: Static Matrix Rain visualizer.
- `matrix_blender_script.py`: Blender 4.x script to generate a Matrix-style scene.
- Add new Python modules at repo root or a `src/` folder; place web assets under `js/`, `styles/`, and `assets/` (if introduced). Tests go in `tests/`.

## Build, Test, and Development Commands
- Create venv: `python3 -m venv .venv && source .venv/bin/activate`
- Install deps (dev): `pip install pillow gradio pytesseract` (OCR optional; requires system Tesseract).
- Run CLI (example): `python image_tool.py resize in.jpg out.jpg --preset instagram_square`
- Run Web UI: `python webui.py` (opens Gradio interface).
- Serve Matrix demo: `python -m http.server` then open `http://localhost:8000/index.html`.
- Blender: open `matrix_blender_script.py` in Blender > Scripting and Run.

## Coding Style & Naming Conventions
- Python: 4-space indent, type hints, snake_case functions, UPPER_CASE constants (e.g., `PRESETS`). Keep Spanish user-facing strings consistent with current UI.
- JS: `const`/`let`, camelCase, no globals beyond needed canvas state. Keep labels in Spanish.
- CSS: consistent indentation; keep selectors simple and scoped to existing structure.
- File names: Python `snake_case.py`; web assets `kebab-case`.

## Testing Guidelines
- No formal suite yet. If adding tests, use `pytest` with `tests/test_*.py` and sample images under `tests/data/` (small files, checked in).
- Manual checks: run sample CLI commands and verify sizes; in Web UI, exercise each tab; for Matrix demo, verify controls update render.
- Static checks: enable VS Code Python “strict” type checking (already configured in `.vscode/settings.json`).

## Commit & Pull Request Guidelines
- Prefer Conventional Commits: `feat:`, `fix:`, `docs:`, `refactor:`. Be descriptive and scoped.
- PRs must include: summary, before/after notes, reproduction steps, and screenshots/GIFs for UI changes. Link related issues.
- Do not commit large/generated binaries (output images, renders). If presets change, update both `image_tool.py` and `webui.py`.

## Security & Configuration Tips
- OCR requires Tesseract installed on the system (e.g., macOS: `brew install tesseract`).
- Validate paths and sizes; avoid unbounded image sizes to prevent OOM. Keep error messages helpful and in Spanish to match UI.

