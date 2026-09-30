import re
from pathlib import Path
from uuid import uuid4

def safe_filename(value: str, extension: str = ".png") -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_-]+", "_", value).strip("_")
    cleaned = cleaned[:60] or "comic_panel"
    if not extension.startswith("."):
        extension = "." + extension
    return f"{cleaned}_{uuid4().hex[:10]}{extension.lower()}"

def ensure_relative_static_path(path: Path, static_root: Path) -> str:
    return "/" + path.relative_to(static_root).as_posix()
