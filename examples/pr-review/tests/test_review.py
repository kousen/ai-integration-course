"""No-key tests for the reviewer's parsing and exit codes.

    python3 -m pytest tests -v     # from examples/pr-review
"""
import subprocess
import sys
from pathlib import Path

from review import exit_code, parse_findings, report

HERE = Path(__file__).resolve().parents[1]

REPLY = """PASS 1 | server.py:12 | OPENROUTER_API_KEY is hard-coded | read it from the environment
PASS 3 | critique.py:40 | duplicated JSON extraction | reuse extract_json
- PASS 4 | README.md:1 | no run instructions | add a Run section
"""


def test_findings_are_parsed_one_per_line():
    f = parse_findings(REPLY)
    assert [x["pass"] for x in f] == [1, 3, 4]
    assert f[0]["where"] == "server.py:12"
    assert f[0]["fix"] == "read it from the environment"


def test_prose_around_findings_is_ignored():
    text = "Here is my review:\n" + REPLY + "\nLet me know if you want more detail."
    assert len(parse_findings(text)) == 3


def test_pass_one_or_two_means_exit_one():
    assert exit_code(REPLY, parse_findings(REPLY)) == 1
    only2 = "2 | a.py:1 | model output used unchecked | validate before use"
    assert exit_code(only2, parse_findings(only2)) == 1


def test_only_pass_three_and_four_means_exit_zero():
    text = "PASS 3 | a.py:1 | dead code | delete it\nPASS 4 | b.py:2 | comment typo | fix it"
    assert exit_code(text, parse_findings(text)) == 0


def test_none_means_exit_zero():
    assert exit_code("NONE", []) == 0


def test_no_findings_and_no_none_fails_closed():
    assert exit_code("", []) == 2
    assert exit_code("Looks fine to me!", []) == 2


def test_report_groups_by_pass():
    text = report(parse_findings(REPLY))
    assert text.index("Pass 1") < text.index("Pass 3") < text.index("Pass 4")
    assert "server.py:12" in text


def test_command_line_with_saved_findings_sets_exit_code(tmp_path):
    saved = tmp_path / "reply.txt"
    saved.write_text(REPLY)
    r = subprocess.run([sys.executable, str(HERE / "review.py"), "--findings", str(saved)], check=False, capture_output=True, text=True)
    assert r.returncode == 1
    assert "Must not merge" in r.stdout
    saved.write_text("NONE\n")
    r = subprocess.run([sys.executable, str(HERE / "review.py"), "--findings", str(saved)], check=False, capture_output=True, text=True)
    assert r.returncode == 0
