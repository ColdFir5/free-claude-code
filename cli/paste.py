"""Clipboard image utility for Windows, macOS, and Linux.

Reads an image from the system clipboard and saves it to a temp file so it can
be referenced from within a Claude Code session (e.g. ``!fcc-paste``).
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


def _output_dir() -> Path:
    env = os.environ.get("FCC_PASTE_DIR", "").strip()
    if env:
        return Path(env)
    return Path(tempfile.gettempdir()) / "free-claude-code" / "pastes"


def _grab_clipboard_image():
    """Return a PIL Image from the clipboard, or None."""
    try:
        from PIL import ImageGrab
    except ImportError:
        return None

    result = ImageGrab.grabclipboard()
    if result is None:
        return None
    if isinstance(result, list):
        # CF_HDROP — the clipboard contains file paths, not raw image data.
        # Return the first path that looks like an image.
        for path_str in result:
            if isinstance(path_str, str):
                p = Path(path_str)
                if p.suffix.lower() in (
                    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp",
                ):
                    return str(p.resolve())
        return None
    return result


def _save_image(image, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
    path = output_dir / f"paste_{ts}.png"
    image.save(str(path), format="PNG")
    return path


def main() -> None:
    image = _grab_clipboard_image()

    if image is None:
        print(
            json.dumps(
                {
                    "status": "no_image",
                    "message": "No image found on clipboard. "
                    "Copy an image first (e.g. Win+Shift+S).",
                }
            )
        )
        return

    if isinstance(image, str):
        # Already a path from CF_HDROP
        print(json.dumps({"status": "ok", "path": image}))
        return

    try:
        out_dir = _output_dir()
        saved_path = _save_image(image, out_dir)
        print(
            json.dumps(
                {
                    "status": "ok",
                    "path": str(saved_path.resolve()),
                    "size": list(image.size),
                }
            )
        )
    except Exception as exc:
        print(
            json.dumps(
                {
                    "status": "error",
                    "message": f"Failed to save clipboard image: {exc}",
                }
            )
        )
        sys.exit(1)
