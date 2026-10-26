"""Make the fixture clips in clips/ from clips/expected.json, with the class TTS model.

    python3 make_clips.py            # needs OPENROUTER_API_KEY; about $0.005 for the three clips

The clips are WAV, not MP3: see speak.py for why (a wrong MP3 length header made
Whisper stop halfway on October 26). They are also a round trip: a model spoke them,
so a transcription model hearing them is a weaker test than a person's recording in
a real room. That is why the
lab asks for two clips of your own voice as well. Do not edit expected.json by
hand to make a failing clip pass; change the clip or the tolerance, and say why.
"""
import json
import os
import sys
from pathlib import Path

from openrouter import OpenRouter

from speak import speak

HERE = Path(__file__).parent

if __name__ == "__main__":
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        sys.exit("OPENROUTER_API_KEY is not set; nothing was billed.")
    client = OpenRouter(api_key=key)
    total = 0.0
    for entry in json.loads((HERE / "clips" / "expected.json").read_text()):
        info = speak(client, entry["text"], HERE / "clips" / entry["file"], voice=entry.get("voice", "en-US-Harper:MAI-Voice-2.1-Flash"))
        total += info["cost"] or 0
        print(f"{entry['file']}: {info['bytes']} bytes, {info['chars']} chars, ${info['cost']}, voice {info['voice']}")
    print(f"total ${total:.5f}")
