# src/scanner.py

import os
from pathlib import Path
from datetime import datetime
from typing import Iterator, Dict, Optional


def scan_folder(folder_path: str) -> Iterator[Dict[str, Optional[object]]]:
    """
    Recursively scans a folder and yields file metadata one by one.
    """
    base_path = Path(folder_path)

    if not base_path.exists():
        raise ValueError(f"Path does not exist: {folder_path}")

    if not base_path.is_dir():
        raise ValueError(f"Path is not a directory: {folder_path}")

    for path in base_path.rglob("*"):
        if not path.is_file():
            continue

        try:
            stat = path.stat()

            yield {
                "full_path": str(path.resolve()),
                "file_name": path.name,
                "extension": path.suffix[1:] if path.suffix else None,
                "size_bytes": stat.st_size,
                "created_at": datetime.fromtimestamp(stat.st_ctime)
                if hasattr(stat, "st_ctime")
                else None,
                "modified_at": datetime.fromtimestamp(stat.st_mtime),
            }

        except (OSError, PermissionError):
            # Skip files we can't access
            continue
