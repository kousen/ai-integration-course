"""No-key tests for the transcript checker.

    python3 -m pytest tests/test_check.py -v     # from examples/voice-loop; well under a second
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from check import compare, wer, words

SAID = "My name is Ken Kousen and I teach CPSC 415 at Trinity College."


def test_words_ignore_case_and_punctuation():
    assert words("Hello, World!  It's 415.") == ["hello", "world", "it's", "415"]


def test_perfect_transcript_scores_zero():
    assert wer(SAID, SAID) == 0.0
    assert wer(SAID, "my name is ken kousen, and i teach cpsc 415 at trinity college") == 0.0


def test_one_substitution_in_thirteen_words():
    got = SAID.replace("Kousen", "Cousin")               # what Whisper does to the name
    assert abs(wer(SAID, got) - 1 / 13) < 1e-9


def test_empty_transcript_is_a_failed_transcript_not_a_crash():
    assert wer(SAID, "") == 1.0
    assert wer(SAID, None) == 1.0
    result = compare(SAID, None)
    assert not result["ok"] and result["empty"]


def test_names_that_must_survive_are_checked_separately():
    got = SAID.replace("Kousen", "Cousin")
    result = compare(SAID, got, must_contain=["Kousen", "415"])
    assert result["missing"] == ["Kousen"]              # a 1-in-13 rate would have passed on its own
    assert not result["ok"]


def test_small_drift_within_tolerance_is_ok():
    got = "My name is Ken Kousen and I teach CPSC 415 at Trinity."    # one word dropped
    result = compare(SAID, got, must_contain=["Kousen"], max_wer=0.15)
    assert result["ok"] and result["wer"] == round(1 / 13, 3)


def test_number_read_as_words_is_a_miss():
    got = SAID.replace("415", "four fifteen")
    assert compare(SAID, got, must_contain=["415"])["missing"] == ["415"]


def test_must_contain_ignores_spacing_and_case():
    got = "Compared with a boot camp graduate from cpsc415"
    assert compare("x", got, must_contain=["bootcamp", "CPSC 415"], max_wer=9)["missing"] == []
