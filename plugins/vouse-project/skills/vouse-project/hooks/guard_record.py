#!/usr/bin/env python3
"""Claude Code PreToolUse hook: record/ is append-only.

Blocks Write/Edit to an EXISTING file under record/ (new files pass, so
findings and supersessions can land). Corrections route as new dated files
with `supersedes:` — see the vouse-project record reference.

Wire via hooks/settings.hooks.json. Contract: hook receives tool-call JSON
on stdin; exit 2 blocks the call with stderr shown to the model; exit 0
allows. This hook prints one line on every decision so its liveness is
visible — a silent gate is an unverifiable gate.
"""
import json
import sys
from pathlib import Path


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0  # malformed input: never block on our own failure
    tool = payload.get("tool_name", "")
    if tool not in ("Write", "Edit"):
        return 0
    fp = payload.get("tool_input", {}).get("file_path", "")
    if not fp:
        return 0
    p = Path(fp)
    parts = [q.lower() for q in p.parts]
    if "record" not in parts:
        return 0
    if p.exists():
        print(
            f"guard_record: BLOCKED edit to existing record file {p.name} — "
            "record/ is append-only. Write a new dated file with "
            "`supersedes: " + p.name + "` instead.",
            file=sys.stderr,
        )
        return 2
    print(f"guard_record: allowed new record file {p.name}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
