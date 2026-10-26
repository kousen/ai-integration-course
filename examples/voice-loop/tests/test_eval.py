"""The billed eval: one transcription per fixture clip, checked in code, and one speech call.
Skipped without a key, so CI and the gate stay free. Record the output in CHECKS.md.

    export OPENROUTER_API_KEY=...
    python3 -m pytest tests/test_eval.py -v -s       # about $0.002 on the class models
"""
import json
import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from check import compare

KEY = os.environ.get("OPENROUTER_API_KEY")
pytestmark = pytest.mark.skipif(not KEY, reason="OPENROUTER_API_KEY not set: the billed eval is skipped")
EXPECTED = json.loads((ROOT / "clips" / "expected.json").read_text())


@pytest.fixture(scope="module")
def client():
    from openrouter import OpenRouter
    return OpenRouter(api_key=KEY)


@pytest.mark.parametrize("entry", EXPECTED, ids=[e["file"] for e in EXPECTED])
def test_each_clip_transcribes_within_tolerance(client, entry):
    from transcribe import transcribe_file
    clip = ROOT / "clips" / entry["file"]
    if not clip.exists():
        pytest.skip(f"{clip.name} missing; run make_clips.py")
    r = transcribe_file(client, clip, language=entry.get("language"))
    verdict = compare(entry["text"], r["text"], entry.get("must_contain"), entry.get("max_wer", 0.15))
    print(f"\n{entry['file']}: wer={verdict['wer']} missing={verdict['missing']} ${r['cost']}  got={r['text']!r}")
    assert verdict["ok"], verdict


def test_speech_comes_back_as_audio(client, tmp_path):
    from speak import speak
    info = speak(client, "The eval ran, and this sentence cost a fraction of a cent.", tmp_path / "eval.mp3")
    print(f"\nspeech: {info['bytes']} bytes, ${info['cost']}")
    assert info["bytes"] > 2000                              # a JSON error body is a few hundred bytes
    head = (tmp_path / "eval.mp3").read_bytes()[:3]
    assert head.startswith(b"ID3") or head[:2] in (b"\xff\xfb", b"\xff\xf3", b"\xff\xf2")   # MP3 frame sync or ID3 tag
