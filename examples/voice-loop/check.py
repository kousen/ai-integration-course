"""Check a transcript in plain code. No model, no key.

A transcript is model output. The checks here are the ones a program can make
without hearing the audio: how far the words drift from what was said (word
error rate), whether the words that must survive did (names, numbers), and
whether the model returned anything at all. The lab's tests import these.
"""
import re

_WORD = re.compile(r"[a-z0-9']+")


def words(text: str | None) -> list[str]:
    """Lower-case words with punctuation removed, so 'Hello, world!' == 'hello world'."""
    return _WORD.findall((text or "").lower().replace("’", "'"))


def wer(expected: str, got: str | None) -> float:
    """Word error rate: edits (insert, delete, substitute) per expected word.
    0.0 is a perfect transcript; 1.0 means nothing matched; empty output scores 1.0."""
    e, g = words(expected), words(got)
    if not e:
        return 0.0 if not g else 1.0
    prev = list(range(len(g) + 1))            # ponytail: O(n*m) Levenshtein; fine for sentences
    for i, ew in enumerate(e, 1):
        cur = [i]
        for j, gw in enumerate(g, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ew != gw)))
        prev = cur
    return prev[-1] / len(e)


def compare(expected: str, got: str | None, must_contain: list[str] | None = None, max_wer: float = 0.15) -> dict:
    """The verdict the lab records per clip: the rate, the words that had to survive and did
    not, and ok only when both pass. A missing transcript is a failed transcript, not a crash."""
    heard = "".join(words(got))                 # spacing-insensitive: "boot camp" and "CPSC415" still count
    missing = [w for w in (must_contain or []) if "".join(words(w)) not in heard]
    rate = wer(expected, got)
    return {"ok": rate <= max_wer and not missing and bool(words(got)),
            "wer": round(rate, 3), "missing": missing, "empty": not words(got)}
