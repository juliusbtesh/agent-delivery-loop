#!/usr/bin/env python3
"""Check or install local Codex and Claude Code skill links."""

import argparse
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
            if link.is_symlink() and link.resolve() == source.resolve():
                state = "OK"
            elif link.is_symlink() or link.exists():
                state = "CONFLICT"
                incomplete = True
            elif args.install:
                destination.mkdir(parents=True, exist_ok=True)
                link.symlink_to(source, target_is_directory=True)
                state = "INSTALLED"
            else:
                state = "MISSING"
                incomplete = True
            print(f"{agent:6} {state:9} {link}")

    return 1 if incomplete else 0


if __name__ == "__main__":
    raise SystemExit(main())
