from types import SimpleNamespace
from pathlib import Path
from PIL import Image

import image_tool


def make_image(path: Path, size=(300, 200), color=(255, 0, 0)) -> Path:
    img = Image.new("RGB", size, color)
    img.save(path)
    return path


def test_resize_with_preset(tmp_path: Path):
    inp = make_image(tmp_path / "in.jpg", size=(400, 300))
    out = tmp_path / "out.jpg"

    args = SimpleNamespace(
        input_path=str(inp),
        output_path=str(out),
        preset="instagram_square",
        size=None,
        aspect_ratio=None,
    )
    image_tool.resize_image(args)

    with Image.open(out) as img:
        assert img.size == (1080, 1080)


def test_resize_to_size(tmp_path: Path):
    inp = make_image(tmp_path / "in.jpg", size=(40, 30))
    out = tmp_path / "out.jpg"

    args = SimpleNamespace(
        input_path=str(inp),
        output_path=str(out),
        preset=None,
        size=(100, 50),
        aspect_ratio=None,
    )
    image_tool.resize_image(args)

    with Image.open(out) as img:
        assert img.size == (100, 50)


def test_resize_to_aspect_ratio(tmp_path: Path):
    inp = make_image(tmp_path / "in.jpg", size=(300, 300))
    out = tmp_path / "out.jpg"

    args = SimpleNamespace(
        input_path=str(inp),
        output_path=str(out),
        preset=None,
        size=None,
        aspect_ratio=(2, 1),
    )
    image_tool.resize_image(args)

    with Image.open(out) as img:
        assert img.size == (300, 150)


def test_crop_image(tmp_path: Path):
    inp = make_image(tmp_path / "in.jpg", size=(200, 200))
    out = tmp_path / "out.jpg"

    args = SimpleNamespace(
        input_path=str(inp),
        output_path=str(out),
        x=10,
        y=20,
        width=50,
        height=60,
    )
    image_tool.crop_image(args)

    with Image.open(out) as img:
        assert img.size == (50, 60)


def test_tile_image(tmp_path: Path):
    tile = make_image(tmp_path / "tile.jpg", size=(10, 10), color=(0, 255, 0))
    out = tmp_path / "out.jpg"

    args = SimpleNamespace(
        input_path=str(tile),
        output_path=str(out),
        final_width=25,
        final_height=25,
    )
    image_tool.tile_image(args)

    with Image.open(out) as img:
        assert img.size == (25, 25)


def test_mirror_image(tmp_path: Path):
    inp = make_image(tmp_path / "in.jpg", size=(123, 45))
    out = tmp_path / "out.jpg"

    args = SimpleNamespace(input_path=str(inp), output_path=str(out))
    image_tool.mirror_image(args)

    with Image.open(out) as img:
        assert img.size == (123, 45)

