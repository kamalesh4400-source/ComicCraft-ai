from pathlib import Path
from app.utils.files import ensure_relative_static_path, safe_filename

def test_safe_filename():
    name = safe_filename("hello world!!", ".png")
    assert name.startswith("hello_world_")
    assert name.endswith(".png")

def test_relative_static_path():
    root = Path("/tmp/static")
    assert ensure_relative_static_path(root / "panels" / "x.png", root) == "/panels/x.png"
