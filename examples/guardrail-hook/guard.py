"""PreToolUse guard: the agent may not touch the answer key, run destructive commands,
or install a package that spec.md does not list. Exit 2 blocks the call and the
message on stderr is shown to the agent. Anything else is allowed.

Install: copy to .claude/hooks/guard.py and register it in .claude/settings.json.
Test:    echo '{"tool_name":"Edit","tool_input":{"file_path":"images/expected.json"}}' | python3 guard.py
"""
import json
import re
import sys
from pathlib import Path

PROTECTED = ("images/", "expected.json")            # the answer key: tests check against it, nobody edits it
DESTRUCTIVE = [r"\brm\s+-[a-z]*r", r"\bgit\s+push\b.*(--force|-f)\b", r"\bgit\s+reset\s+--hard",
               r"\bgit\s+checkout\s+--\s", r"\bgit\s+clean\b"]
WRITES = r"(>|\bsed\s+-i|\bmv\b|\brm\b|\bcp\b|\btee\b|\btruncate\b)"
INSTALL = r"\b(?:pip3?|uv)\s+(?:install|add)\s+(.*)|\bnpm\s+(?:install|i|add)\s+(.*)"


def deny(reason: str) -> None:
    print(reason, file=sys.stderr)
    sys.exit(2)


def packages(args: str) -> list[str]:
    out = []
    for tok in args.split():
        if tok.startswith("-") or tok.startswith(".") or "/" in tok or tok.endswith(".txt"):
            continue
        out.append(re.split(r"[\[<>=!~@]", tok)[0].lower())
    return out


def main() -> None:
    call = json.load(sys.stdin)
    tool, inp = call.get("tool_name", ""), call.get("tool_input", {})
    if tool in ("Edit", "Write", "MultiEdit"):
        path = inp.get("file_path", "")
        if any(p in path for p in PROTECTED):
            deny(f"{path} is the answer key. Fix the code, not the expected values. "
                 "If you believe the key is wrong, say so and stop.")
    elif tool == "Bash":
        cmd = inp.get("command", "")
        for pat in DESTRUCTIVE:
            if re.search(pat, cmd):
                deny(f"Blocked destructive command ({pat}). Ask the user to run it by hand if it is really needed.")
        if any(p in cmd for p in PROTECTED) and re.search(WRITES, cmd):
            deny("That command writes to the answer key (images/ or expected.json). Fix the code instead.")
        m = re.search(INSTALL, cmd)
        if m:
            spec = Path("spec.md").read_text().lower() if Path("spec.md").exists() else ""
            missing = [p for p in packages(m.group(1) or m.group(2) or "") if p not in spec]
            if missing:
                deny(f"{', '.join(missing)} is not in spec.md. Add it under Dependencies with the reason, "
                     "get that approved, then install.")
    sys.exit(0)


if __name__ == "__main__":
    main()
