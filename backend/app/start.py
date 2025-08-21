"""Runtime sanitation and app launcher.

Removes UTF BOMs, UTF-16 encodings, and embedded null bytes from all .py files
before starting Uvicorn. This offsets any editor / OS encoding corruption while
developing with a bind mount.
"""
from __future__ import annotations
import pathlib


def sanitize_py(root: pathlib.Path):
    for path in root.rglob('*.py'):
        try:
            raw = path.read_bytes()
        except Exception:
            continue
        changed = False
        if raw.startswith(b'\xef\xbb\xbf'):
            raw = raw[3:]; changed = True
        elif raw.startswith(b'\xff\xfe'):
            try:
                raw = raw[2:].decode('utf-16-le').encode('utf-8'); changed = True
            except Exception:
                pass
        elif raw.startswith(b'\xfe\xff'):
            try:
                raw = raw[2:].decode('utf-16-be').encode('utf-8'); changed = True
            except Exception:
                pass
        if b'\x00' in raw:
            raw = raw.replace(b'\x00', b''); changed = True
        if changed:
            path.write_bytes(raw)


def main():
    sanitize_py(pathlib.Path('.'))
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
