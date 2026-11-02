#!/usr/bin/env python3
# Developer: Hamdy Abou El Anein
# Contact: info@daylightlinux.ch
# SPDX-License-Identifier: GPL-3.0-only
"""Preview-first cleanup of Wayback Machine wrappers in local HTML."""
from __future__ import annotations
import argparse
from pathlib import Path
import re
import shutil

WAYBACK = re.compile(r"https?://web\.archive\.org/web/\d+(?:[a-z_]+)?/(https?://[^\s\"'<>]+)", re.I)

def clean_html(html: str) -> str:
    # Preserve original formatting; do not reserialize whole documents.
    return WAYBACK.sub(lambda match: match.group(1), html)

def plan(root: Path) -> list[tuple[Path, str]]:
    if not root.is_dir() or root.is_symlink():
        raise ValueError("Expected a real directory")
    changes = []
    for path in root.rglob("*"):
        if path.is_symlink() or not path.is_file() or path.suffix.lower() not in (".html", ".htm"):
            continue
        try:
            original = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
        cleaned = clean_html(original)
        if cleaned != original:
            changes.append((path, cleaned))
    return changes

def apply_changes(changes: list[tuple[Path, str]]) -> int:
    completed = 0
    for path, cleaned in changes:
        if path.is_symlink():
            continue
        backup = path.with_name(path.name + ".wayback-backup")
        if backup.exists():
            print(f"SKIP: backup already exists for {path}")
            continue
        shutil.copy2(path, backup)
        # Exclusive backup protects original contents. Never delete the backup.
        temp = path.with_name(path.name + ".wayback-temp")
        if temp.exists() or temp.is_symlink():
            print(f"SKIP: temporary file already exists for {path}")
            continue
        try:
            with temp.open("x", encoding="utf-8") as stream:
                stream.write(cleaned)
            temp.replace(path)
            completed += 1
        finally:
            temp.unlink(missing_ok=True)
    return completed

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--apply", action="store_true", help="Write changes after creating backups")
    args = parser.parse_args()
    try:
        changes = plan(args.directory)
    except ValueError as exc:
        parser.error(str(exc))
    for path, _ in changes:
        print("CHANGE" if args.apply else "DRY-RUN", path)
    if args.apply:
        print("Updated:", apply_changes(changes))
    else:
        print(f"{len(changes)} files would change. Add --apply to write.")

if __name__ == "__main__":
    main()
