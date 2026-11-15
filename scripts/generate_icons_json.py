#!/usr/bin/env python3
"""Generate icons.json from every image file under icon/.

The produced file mirrors fmz200/wool_scripts' icons-all.json format:
  { "name": ..., "description": ..., "icons": [ {"name": ..., "url": ...} ] }

Usage:
  python scripts/generate_icons_json.py [--repo OWNER/REPO] [--branch main]
                                      [--icons-dir icon] [--output icons.json]

By default the GitHub raw URLs are derived from the local git remote "origin"
and the current branch, so no manual editing is needed.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path

# Image extensions we consider icons.
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".svg"}

# Friendly Chinese names for known files (fallback: filename stem).
DISPLAY_NAMES = {
    "kaiqboy": "凯奇男孩",
    "tuotuoyun": "坨坨云",
    "yidianwanxiang": "一点万象",
}


def git(args: list[str], cwd: Path) -> str | None:
    try:
        return subprocess.check_output(
            ["git", *args], cwd=cwd, stderr=subprocess.DEVNULL, text=True
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def detect_repo_and_branch(root: Path, override_repo: str | None) -> tuple[str, str]:
    """Return (owner/repo, branch) used to build raw.githubusercontent.com URLs."""
    repo = override_repo
    if repo is None:
        remote = git(["remote", "get-url", "origin"], root) or ""
        # Accept both https and ssh forms.
        m = re.search(r"github\.com[:/]([^/]+)/([^/]+?)(?:\.git)?$", remote)
        if m:
            repo = f"{m.group(1)}/{m.group(2)}"
    if not repo:
        repo = "bupangde/Clash"

    branch = git(["rev-parse", "--abbrev-ref", "HEAD"], root) or "main"
    return repo, branch


def display_name(path: Path) -> str:
    return DISPLAY_NAMES.get(path.stem, path.stem)


def build(root: Path, icons_dir: Path, output: Path, repo: str, branch: str) -> dict:
    if not icons_dir.is_dir():
        sys.exit(f"icons dir not found: {icons_dir}")

    files = sorted(
        (p for p in icons_dir.rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_EXTS),
        key=lambda p: p.relative_to(icons_dir).as_posix().lower(),
    )

    base = f"https://raw.githubusercontent.com/{repo}/{branch}"
    icons = []
    for p in files:
        rel = p.relative_to(root).as_posix()  # e.g. icon/kaiqboy.jpg
        icons.append(
            {
                "name": display_name(p),
                "url": f"{base}/{rel}",
            }
        )

    now = dt.datetime.now(dt.timezone(dt.timedelta(hours=8))).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    data = {
        "name": "Kaiq 图标库",
        "description": f"个人收集的图标，共 {len(icons)} 个，更新日期：{now}",
        "icons": icons,
    }

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return data


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", help="OWNER/REPO, default: parse from git remote origin")
    ap.add_argument("--branch", help="branch for raw URLs, default: current branch")
    ap.add_argument("--icons-dir", default="icon")
    ap.add_argument("--output", default="icons.json")
    ap.add_argument("--root", help="repo root (default: parent of this script)")
    args = ap.parse_args()

    root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parent.parent
    repo, detected_branch = detect_repo_and_branch(root, args.repo)
    branch = args.branch or detected_branch

    icons_dir = root / args.icons_dir
    output = root / args.output
    data = build(root, icons_dir, output, repo, branch)
    print(
        f"Wrote {output.relative_to(root)}: {len(data['icons'])} icons "
        f"(repo={repo}, branch={branch})"
    )


if __name__ == "__main__":
    main()
