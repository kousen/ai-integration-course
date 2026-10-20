"""Review a diff against REVIEW.md with a second model. Exit 1 on any pass-1 or pass-2 finding.

    python3 review.py                              # diff of this branch against main, needs OPENROUTER_API_KEY
    python3 review.py --diff change.patch          # a saved diff instead
    REVIEW_MODEL=xiaomi/mimo-v2.6-flash python3 review.py
    python3 review.py --findings saved.txt         # no key: re-parse a saved reply (for tests and demos)

The model gets REVIEW.md (the policy), spec.md (what the code is supposed to do) and
the diff, and must answer one finding per line:

    PASS <1-4> | <file>:<line> | <what is wrong> | <what to do instead>

or the single word NONE. The code groups the findings by pass and sets the exit
code; a gate (pre-push hook or CI) uses the exit code. The reviewer is a model and
can be wrong in both directions; the findings are a list to check, not a verdict.

Exit codes: 0 nothing in pass 1 or 2; 1 something must be fixed; 2 the reviewer's
reply could not be parsed (fail closed: a gate must not pass on silence).
"""
import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

DEFAULT_MODEL = "minimax/minimax-m3"
REASONING = {"xiaomi/mimo-v2.6-flash": {"effort": "none"}}     # SDK form of {"enabled": false}; weeks/05/setup.md, section 2
MAX_DIFF_CHARS = 60_000          # about 15k tokens; a bigger PR should be smaller PRs
PASS_NAMES = {1: "Must not merge", 2: "Must fix before merge", 3: "Should fix", 4: "Nice to have"}
LINE = re.compile(r"^\s*(?:[-*]\s*)?(?:PASS\s*)?([1-4])\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*(?:\|\s*(.*?))?\s*$", re.IGNORECASE)

PROMPT = """You are a code reviewer. Review the diff below against the review policy, using the spec to
judge whether the code does what was agreed. Report only what you can point to in the diff.

Reply with one finding per line in exactly this form, most severe first, and nothing else:
PASS <1-4> | <file>:<line> | <what is wrong> | <what to do instead>
If there is nothing to report in any pass, reply with the single word NONE.

=== REVIEW.md (the policy) ===
{review}

=== spec.md (what the code should do) ===
{spec}

=== The diff ===
{diff}
"""


def parse_findings(text: str) -> list[dict]:
    """Findings from the model's reply, one per line. Lines that do not fit the form are ignored."""
    out = []
    for line in (text or "").splitlines():
        m = LINE.match(line)
        if m:
            out.append({"pass": int(m.group(1)), "where": m.group(2), "what": m.group(3), "fix": m.group(4) or ""})
    return out


def exit_code(text: str, findings: list[dict]) -> int:
    if any(f["pass"] <= 2 for f in findings):
        return 1
    if findings or re.search(r"\bNONE\b", text or ""):
        return 0
    return 2            # neither findings nor NONE: the reviewer did not answer; do not pass the gate


def report(findings: list[dict]) -> str:
    if not findings:
        return "No findings."
    lines = []
    for p in (1, 2, 3, 4):
        group = [f for f in findings if f["pass"] == p]
        if group:
            lines.append(f"Pass {p}: {PASS_NAMES[p]} ({len(group)})")
            lines += [f"  {f['where']}: {f['what']}" + (f" -> {f['fix']}" if f["fix"] else "") for f in group]
    return "\n".join(lines)


def git_diff(base: str) -> str:
    return subprocess.run(["git", "diff", f"{base}...HEAD"], capture_output=True, text=True, check=True).stdout


def ask_model(model: str, review: str, spec: str, diff: str) -> tuple[str, dict]:
    from openrouter import OpenRouter

    client = OpenRouter(api_key=os.environ["OPENROUTER_API_KEY"])
    kwargs = {"reasoning": REASONING[model]} if model in REASONING else {}
    c = client.chat.send(model=model, max_tokens=2000,
                         messages=[{"role": "user", "content": PROMPT.format(review=review, spec=spec, diff=diff)}],
                         **kwargs)
    usage = {"in": c.usage.prompt_tokens, "out": c.usage.completion_tokens, "cost": getattr(c.usage, "cost", None)} if c.usage else {}
    return c.choices[0].message.content or "", usage


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--diff", type=Path, help="a saved diff; default is git diff <base>...HEAD")
    ap.add_argument("--base", default="main")
    ap.add_argument("--review", type=Path, default=Path("REVIEW.md"))
    ap.add_argument("--spec", type=Path, default=Path("spec.md"))
    ap.add_argument("--model", default=os.environ.get("REVIEW_MODEL", DEFAULT_MODEL))
    ap.add_argument("--findings", type=Path, help="a saved reply to parse instead of calling a model")
    args = ap.parse_args()

    if args.findings:
        text, usage = args.findings.read_text(), {}
    else:
        diff = args.diff.read_text() if args.diff else git_diff(args.base)
        if not diff.strip():
            print("Empty diff: nothing to review.")
            return 0
        if len(diff) > MAX_DIFF_CHARS:
            print(f"Diff is {len(diff):,} characters; the limit is {MAX_DIFF_CHARS:,}. Split the PR.", file=sys.stderr)
            return 2
        if not os.environ.get("OPENROUTER_API_KEY"):
            print("OPENROUTER_API_KEY is not set; the review is a billed call. Not reviewed.", file=sys.stderr)
            return 2
        spec = args.spec.read_text() if args.spec.exists() else "(no spec.md found)"
        text, usage = ask_model(args.model, args.review.read_text(), spec, diff)

    findings = parse_findings(text)
    code = exit_code(text, findings)
    print(report(findings))
    if code == 2:
        print("The reviewer's reply had no findings and no NONE. Raw reply follows; the gate stays closed.\n" + text)
    if usage:
        print(f"[{args.model} · {usage.get('in')} in / {usage.get('out')} out · cost {usage.get('cost')}]")
    return code


if __name__ == "__main__":
    sys.exit(main())
