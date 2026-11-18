#!/usr/bin/env python3
"""Check or install local Codex and Claude Code skill links."""

import argparse
import os
import subprocess
from pathlib import Path


SKILLS = (
    "delivery-setup",
    "delivery-discover",
    "delivery-backlog",
    "delivery-implement",
    "delivery-audit",
    "delivery-loop",
)
CLAUDE_ALIASES = {
    "backlog": "delivery-backlog",
    "implement": "delivery-implement",
    "audit": "delivery-audit",
}
DESTINATIONS = {
    "codex": Path(".agents/skills"),
    "claude": Path(".claude/skills"),
}
SOURCE_ROOT = Path(__file__).resolve().parent.parent / "skills"


def is_link(path: Path) -> bool:
    """True for a symbolic link or a Windows directory junction, including a broken one."""
    if path.is_symlink():
        return True
    is_junction = getattr(path, "is_junction", None)
    return bool(is_junction and is_junction())


def make_link(link: Path, source: Path) -> str:
    """Link `link` to `source`. Windows refuses symbolic links without elevated rights or Developer Mode,
    so fall back to a directory junction there: it needs no privilege and behaves the same for a local folder."""
    try:
        link.symlink_to(source, target_is_directory=True)
        return "INSTALLED"
    except OSError:
        if os.name != "nt":
            raise
    result = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(source)], capture_output=True, text=True)
    if result.returncode != 0:
        raise OSError(f"could not create a symbolic link or a junction at {link}: {result.stderr.strip() or result.stdout.strip()}")
    return "INSTALLED (junction)"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--install", action="store_true", help="create missing links; never replace existing entries")
    parser.add_argument(
        "--claude-aliases", action="store_true",
        help="also check or install the optional /backlog, /implement, and /audit shortcuts",
    )
    parser.add_argument(
        "--agent", choices=tuple(DESTINATIONS), action="append",
        help="agent to check or install (repeatable; default: both)",
    )
    parser.add_argument("--home", type=Path, default=Path.home(), help=argparse.SUPPRESS)
    args = parser.parse_args()

    agents = tuple(dict.fromkeys(args.agent or DESTINATIONS))
    home = args.home.expanduser().resolve()
    incomplete = False

    for agent in agents:
        destination = home / DESTINATIONS[agent]
        links = [(name, name) for name in SKILLS]
        if agent == "claude" and args.claude_aliases:
            links.extend(CLAUDE_ALIASES.items())
        for name, source_name in links:
            source = SOURCE_ROOT / source_name
            if not (source / "SKILL.md").is_file():
                parser.error(f"source skill is missing: {source}")
            link = destination / name
            if is_link(link) and link.exists() and link.resolve() == source.resolve():
                state = "OK"
            elif is_link(link) or link.exists():
                state = "CONFLICT"
                incomplete = True
            elif args.install:
                destination.mkdir(parents=True, exist_ok=True)
                state = make_link(link, source)
            else:
                state = "MISSING"
                incomplete = True
            print(f"{agent:6} {state:20} {link}")

    return 1 if incomplete else 0


if __name__ == "__main__":
    raise SystemExit(main())
