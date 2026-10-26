"""The voice loop: the browser records, the server transcribes, answers from the profile, and speaks.

    export OPENROUTER_API_KEY=...
    python3 server.py                 # then open http://localhost:8000

GET  /            the page: a microphone button, a file picker as the fallback, the transcript and the answer.
POST /api/voice   body = audio bytes; header Content-Type says which format (audio/webm from the
                  browser's recorder, audio/mpeg for an uploaded clip). Three billed calls on the server:
                  transcription, chat grounded in profile.json, speech. Returns JSON with the transcript,
                  the answer, the MP3 as base64, and the three costs. The browser never sees the key.
POST /api/ask     body = the question as text; same answer path without the transcription step.

Standard library http.server plus the openrouter SDK, so the whole mechanism is visible.
In your portfolio this is one more route next to the chatbot's, in whatever framework it uses.
"""
import base64
import json
import os
import pathlib
import time
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from openrouter import OpenRouter

from speak import DEFAULT_MODEL as TTS_MODEL
from speak import DEFAULT_VOICE as TTS_VOICE
from speak import speak
from transcribe import DEFAULT_MODEL as STT_MODEL
from transcribe import transcribe

HERE = pathlib.Path(__file__).parent
KEY = os.environ["OPENROUTER_API_KEY"]                       # read once at startup; never sent to the browser
CHAT_MODEL = os.environ.get("CHAT_MODEL", "minimax/minimax-m3")
PAGE = (HERE / "index.html").read_bytes()
PROFILE = json.loads((HERE / "profile.json").read_text())
FORMATS = {"audio/webm": "webm", "audio/mpeg": "mp3", "audio/mp3": "mp3", "audio/wav": "wav", "audio/ogg": "ogg",
           "audio/x-wav": "wav", "audio/mp4": "m4a", "audio/x-m4a": "m4a", "audio/flac": "flac"}

SYSTEM = """You answer a visitor's questions about one person, from the profile below and nothing else.
Rules: shipped work is in "projects" and "skills_shipped"; anything in "not_yet" is something the person has
deliberately not done, and you say so plainly. If the profile does not cover the question, say that you don't
know rather than guessing. Never claim experience the profile does not record. Answer in two or three spoken
sentences: this answer will be read aloud, so no lists, no markdown, no URLs.

PROFILE:
""" + json.dumps(PROFILE, indent=1)

client = OpenRouter(api_key=KEY)


def answer(question: str) -> tuple[str, float | None]:
    """The chatbot's answer function; the typed path and the voice path both call it.
    max_tokens counts the model's hidden reasoning too: at 400, minimax-m3 sometimes spent it all
    thinking and returned an empty answer (October 26), which the speech model then refused."""
    c = client.chat.send(model=CHAT_MODEL, max_tokens=1500,
                         messages=[{"role": "system", "content": SYSTEM}, {"role": "user", "content": question}])
    text = (c.choices[0].message.content or "").strip()
    if not text:                                    # an empty answer is a failed answer, said so, not spoken
        text = f"I couldn't put an answer together (the model stopped: {c.choices[0].finish_reason}). Please ask again."
    return text, getattr(c.usage, "cost", None)


def voice_turn(audio: bytes, fmt: str) -> dict:
    """The loop, once: hear, think, speak. Each step's cost and seconds are recorded for CHECKS.md.
    A failed speech call still returns the transcript and the answer: the visitor can read what
    they could not hear, and the error is in the reply instead of in place of it."""
    t0 = time.time()
    heard = transcribe(client, audio, fmt, STT_MODEL)
    question = heard["text"].strip()
    if not question:
        return {"transcript": "", "answer": "I didn't catch that.", "audio_b64": None,
                "cost": {"stt": heard["cost"], "chat": 0, "tts": 0}, "seconds": {"stt": heard["seconds"]}}
    t1 = time.time()
    reply, chat_cost = answer(question)
    t2 = time.time()
    audio_b64, tts_cost, tts_error = None, 0, None
    try:
        spoken = speak(client, reply, HERE / "last-answer.mp3", TTS_MODEL, TTS_VOICE)
        audio_b64, tts_cost = base64.b64encode((HERE / "last-answer.mp3").read_bytes()).decode(), spoken["cost"]
    except Exception as e:  # noqa: BLE001  (the provider's message, without the key)
        tts_error = str(e)[:300]
    seconds = {"stt": round(t1 - t0, 1), "chat": round(t2 - t1, 1), "tts": round(time.time() - t2, 1)}
    print(f"turn: stt {seconds['stt']}s  chat {seconds['chat']}s  tts {seconds['tts']}s"
          + (f"  TTS FAILED: {tts_error}  on: {reply[:160]!r}" if tts_error else ""), flush=True)
    return {"transcript": question, "answer": reply, "audio_b64": audio_b64, "tts_error": tts_error,
            "cost": {"stt": heard["cost"], "chat": chat_cost, "tts": tts_cost}, "seconds": seconds,
            "models": {"stt": STT_MODEL, "chat": CHAT_MODEL, "tts": f"{TTS_MODEL} / {TTS_VOICE}"}}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/api/"):
            return self.reply(405, {"error": "POST only"})
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(PAGE)

    def do_POST(self):
        body = self.rfile.read(min(int(self.headers.get("Content-Length", 0)), 10_000_000))   # 10 MB cap on what a visitor can send
        try:
            if self.path == "/api/voice":
                ctype = self.headers.get("Content-Type", "").split(";")[0]
                fmt = FORMATS.get(ctype)
                if not fmt:
                    return self.reply(415, {"error": f"unsupported audio type {ctype!r}; send one of {sorted(FORMATS)}"})
                return self.reply(200, voice_turn(body, fmt))
            if self.path == "/api/ask":
                reply, cost = answer(body.decode()[:2000])
                return self.reply(200, {"transcript": body.decode()[:2000], "answer": reply, "audio_b64": None,
                                        "cost": {"stt": 0, "chat": cost, "tts": 0}})
            self.reply(404, {"error": "not found"})
        except Exception as e:  # noqa: BLE001  (the provider's message goes back, never the key)
            traceback.print_exc()
            self.reply(502, {"error": str(e)[:500]})

    def reply(self, status: int, data: dict):
        payload = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


if __name__ == "__main__":
    print(f"http://localhost:8000  (stt {STT_MODEL}, chat {CHAT_MODEL}, tts {TTS_MODEL}/{TTS_VOICE})")
    try:
        ThreadingHTTPServer(("localhost", 8000), Handler).serve_forever()    # a slow turn must not block the next visitor
    except KeyboardInterrupt:
        print("\nstopped")
