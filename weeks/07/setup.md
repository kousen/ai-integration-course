# Week 7 setup additions

Nothing new to install beyond what Week 6 gave you: the `openrouter` SDK already carries the two audio endpoints. Two checkpoints before the lab, each a fraction of a cent, and one browser permission.

## 1. Pull the course repository

```bash
cd path/to/ai-integration-course
git pull
```

That gets you `examples/voice-loop/` (the transcriber, the speaker, the checker, three fixture clips, the server and page, the tests) and `weeks/07/hosting.md`.

## 2. One speech call

Text to speech is `POST /api/v1/audio/speech`. The reply is audio bytes, not JSON.

```bash
cd examples/voice-loop
python3 speak.py "Hello from CPSC 415. This is the class speech model." --out hello.mp3
open hello.mp3            # Windows: start hello.mp3
```

**Checkpoint A:** a line like `hello.mp3  39000 bytes  54 chars  0.5s  cost $0.00081 (estimated)  [microsoft/mai-voice-2.1-flash / en-US-Harper:MAI-Voice-2.1-Flash]`, and a voice saying the sentence. The cost is **estimated** from the catalog price per character because the reply carries no usage object; the generation record that holds the real bill appeared about a minute after the call on October 26 and agreed to the cent. Try `--voice en-GB-Emily:MAI-Voice-2.1-Flash` or `en-IN-Priya:MAI-Voice-2.1-Flash`: the voice id carries the locale, and the model has 23 languages.

## 3. One transcription

Speech to text is `POST /api/v1/audio/transcriptions`. The audio travels as base64 in JSON, the way the receipt images did in Week 5; the reply is JSON with the text and a usage object.

```bash
python3 transcribe.py clips/clip-01.wav --expect "What programming languages have you shipped code in, and which one would you choose for a new web service?"
```

**Checkpoint B:** the sentence printed back, a line like `[openai/whisper-large-v3-turbo  5.575s audio  $1.86e-05  0.6s]`, and `check: {'ok': True, 'wer': 0.0, ...}`. The cost is in the reply this time, priced per second of audio. If `wer` is not 0.0, read the two sentences side by side: on October 26 Whisper read "bootcamp" as "boot camp" from one speech model and correctly from another.

**Why the clips are WAV.** On October 26, MP3s from two cheap speech models carried a wrong length in their header, and Whisper's host trusted it: the transcript stopped halfway and `usage.seconds` matched the header, not the audio. A second transcriber read the whole clip. Raw PCM has no header to be wrong, so `speak.py` writes a WAV when the output name ends in `.wav`, and the fixtures are WAV. Keep that in mind when a transcript ends early: check the audio before you blame the model.

## 4. The microphone

The lab's page records with the browser's `MediaRecorder`. Open http://localhost:8000 once the server is running (lab step 6) and Chrome, Firefox, or Safari asks for microphone permission; `localhost` is treated as secure, so the prompt appears. If you decline or the room is noisy, the page has a file picker: pick a clip and press Ask. Record your own clips (lab step 4) with Voice Memos, QuickTime, or the page itself; `.m4a`, `.wav`, `.mp3`, and `.webm` are all accepted.

**Checkpoint C (optional before class):** `python3 server.py`, open the page, upload `clips/clip-02.wav`, press Ask. You should read a transcript, read an answer that says the profile's owner has not used Kubernetes, and hear it. Three calls, about half a cent, most of it the speech.

## 5. Playwright, still

The browser check `test_browser.py` is the Week 5 one adapted: it uploads a clip through the page and asserts the browser never saw the key or the provider. `pip install playwright && playwright install chromium` if you skipped it in Week 5.

## If something goes wrong

| Symptom | Likely cause |
|---|---|
| `expected audio, got application/json` | The request was rejected; the message after it is the provider's. Usually a voice the model does not have, or a `response_format` it does not support (Gemini TTS answers only `pcm`) |
| The MP3 is a few hundred bytes and will not play | An error body saved as audio. `speak.py` refuses to do this; a hand-written request must check the content type first |
| The transcript stops halfway | The clip's MP3 header is wrong (section 3). Use WAV, or a second transcriber |
| `415 unsupported audio type` from the server | The browser sent a type the server does not map to a format; `.m4a` from Safari is `audio/mp4`, which it accepts; anything else, add it to `FORMATS` |
| `usage.cost` is `None` on a transcription | A token-priced model (`openai/gpt-4o-mini-transcribe`) that reports tokens, not seconds; the cost is still there in the generation record |
| A speech call takes minutes | `hexgrad/kokoro-82m` took 0.4 s, 10 s, and 197 s for three calls on October 26; the class model took under a second every time. Change the model; never wait inside a test |
| The answer is empty on `xiaomi/mimo-v2.6-flash` | Hidden reasoning; `reasoning={"effort": "none"}` through the SDK (Week 5 setup, section 2) |
