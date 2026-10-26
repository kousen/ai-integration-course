# The voice loop: hear, think, speak

The Week 7 example and the piece Team Project 1's stretch goal and the portfolio chatbot's spoken interface are built from. Standard library plus the `openrouter` SDK; no framework. Two new request shapes, both on the same key as chat:

| Direction | Endpoint | Request | Reply | Priced by |
|---|---|---|---|---|
| Speech to text | `POST /api/v1/audio/transcriptions` | `model`, `input_audio: {data: <base64>, format: "wav"}` | JSON: `text`, `usage.seconds`, `usage.cost` | the audio's length in seconds, or tokens on the newest models |
| Text to speech | `POST /api/v1/audio/speech` | `model`, `input`, `voice`, `response_format: "mp3"` or `"pcm"` | raw audio bytes, `X-Generation-Id` header, no usage object | characters of input text (Gemini TTS: tokens) |

| File | What it is |
|---|---|
| `transcribe.py` | One clip or a whole `expected.json` set through `client.stt.create_transcription`; prints the text, the audio seconds, the cost, and the checker's verdict. |
| `speak.py` | Text through `client.tts.create_speech` to an MP3, or to a WAV when the output name ends in `.wav` (asks for PCM and frames it with `wave`). Prints bytes, characters, and the cost. |
| `check.py` | The checker, plain code: word error rate, words that must survive (names, numbers), empty transcript. No key. |
| `clips/` | Three fixture questions a recruiter might ask the profile's owner, spoken by the class TTS model, with `expected.json` (the text, the words that must survive, the tolerance). `make_clips.py` regenerates them. |
| `profile.json` | A fictional student's profile in the portfolio's shape: projects with the four questions, shipped skills, a "not yet" list. |
| `server.py` + `index.html` | The loop: the browser records (or uploads a clip), the server transcribes, answers from the profile with the class chat model, speaks the answer, and returns all three with their costs. The key never leaves the server. |
| `tests/test_check.py` | Eight no-key tests of the checker. |
| `tests/test_eval.py` | The billed eval: each fixture clip transcribed once and checked, plus one speech call. Skipped without a key. |
| `test_browser.py` | Playwright: uploads a fixture clip through the page, waits for the spoken answer, and asserts the browser never saw the key or the provider. |

## Run it

```bash
pip install -r requirements.txt pytest                      # openrouter; playwright for the browser check
python3 -m pytest tests/test_check.py -v                    # no key, under a second
export OPENROUTER_API_KEY=...
python3 speak.py "Hello from CPSC 415." --out hello.mp3     # about $0.0004; open hello.mp3
python3 transcribe.py clips/clip-01.wav --expect "What programming languages have you shipped code in, and which one would you choose for a new web service?"
python3 transcribe.py --set clips/expected.json             # three clips on openai/whisper-large-v3-turbo, about $0.00007
python3 transcribe.py --set clips/expected.json --model elevenlabs/scribe-v2 --out transcripts-scribe.json
python3 -m pytest tests/test_eval.py -v -s                  # the billed eval, about $0.002
python3 server.py                                           # then http://localhost:8000; hold the button and ask
python3 -m pytest test_browser.py -v                        # with the server running; three billed calls
```

Without a key, `speak.py`, `transcribe.py`, and `make_clips.py` stop with one line saying so; nothing is billed by accident.

## The models (measured October 26, 2026)

| Role | Model | Measured | Why |
|---|---|---|---|
| Transcription, class | `openai/whisper-large-v3-turbo` | $0.000019 for a 5.6 s clip, $0.000031 for 9.3 s; 0.4–0.7 s | Cheapest serious transcriber, priced per second of audio |
| Transcription, comparison | `elevenlabs/scribe-v2` | $0.00034–0.00057 per clip (about 18× Whisper); 0.5–0.7 s | Read every fixture perfectly, including the one Whisper got wrong |
| Speech, class | `microsoft/mai-voice-2.1-flash` | $0.0015 for a 103-character question, $0.0024–0.0052 for a spoken answer; 0.4–1.4 s | Priced per character, 23 languages with a voice per locale, MP3 that transcribers read correctly |
| Speech, comparison | `elevenlabs/eleven-v4-turbo` | $0.0027 for 67 characters; 1.5–2.1 s | The expressive one, with audio tags; about 2.7× the class model per character |
| Chat, the answer | `minimax/minimax-m3` | $0.0003–0.0007 per answer with the profile in the system prompt; 1.8–3.5 s | The class model since Week 1; `max_tokens` must cover its hidden reasoning or the answer comes back empty |

One voice turn on the class models costs about **half a cent** (measured $0.0035–$0.0057 on October 26): transcription under one percent of it, the chat answer about a tenth, and the speech the rest, because the answer is two or three sentences at $0.000015 a character. A visitor who leaves the button held down is spending your money three ways, which is why the deployed version needs a cap (see `weeks/07/hosting.md`).

## What the checker can and cannot say

The transcript is model output. The code cannot hear the audio; it knows how far the words drift from what was said (word error rate against the text you wrote down first), whether the words that had to survive did (`must_contain`: names, course numbers), and whether anything came back at all. Spacing and case are ignored, so Whisper's "boot camp" counts as "bootcamp" and "CPSC415" as "CPSC 415"; a name that came back as a different word does not.

What the rehearsal found:

- **Whisper stopped halfway through MP3s from two cheap speech models** (`hexgrad/kokoro-82m`, `mistralai/voxtral-mini-tts-3-0`): their MP3 headers carry a wrong length, Whisper's host trusted it, and `usage.seconds` matched the header, not the audio. Scribe read the whole clip. Raw PCM has no header to be wrong, so `speak.py` writes a WAV when you ask for one, and the fixtures are WAV. The MP3s from the class model and from ElevenLabs transcribed completely.
- **The second transcriber is the check.** Whisper heard "boot camp" on clip 2 from every speech model, and on one run appended "Music" to the trailing silence (a known Whisper habit on quiet audio), which is why that clip's tolerance in `expected.json` is 0.2 with a note saying so. Scribe heard "bootcamp" every time. Both heard "CPSC 415". Hindi through three speech models came back from Scribe as "CPSE 415" twice and "CPSC 415" once, with "program" transliterated as the English word.
- **The speech reply carries no bill.** It is bytes. The `X-Generation-Id` header names a generation record that holds the cost, but on October 26 the record did not exist for about a minute (NotFound), so `speak.py` reports the catalog price times characters and marks it estimated; the record agreed to the cent when it appeared.
- **Format support varies by model.** Gemini TTS answers only `pcm`; Voxtral's documentation says MP3 only but it returned PCM when asked; a voice id belongs to one model and the next model rejects it.

## Settings that matter

- **Language hint.** `--language hi` (ISO-639-1) removes ambiguity on short clips; omitted, the model detects it. Try your own language with the lab's own-voice clips.
- **Reasoning.** The answer step runs on `minimax/minimax-m3` with reasoning on, as in Weeks 5 and 6. Switching the chat model to `xiaomi/mimo-v2.6-flash` needs `reasoning={"effort": "none"}` or the answer comes back empty (Week 5 setup, section 2).
- **Cost.** One transcription per clip, one speech call per answer, never a model call inside a loop of tests. The eval is three transcriptions and one speech call; `CHECKS.md` quotes what each cost.
- **The spoken answer is still the chatbot's answer.** The system prompt in `server.py` keeps the portfolio's rule: shipped work, "not yet" said plainly, no guessing. Hear clip 2 ("Have you ever deployed anything with Kubernetes?") answered with "No, I haven't" and the reason from the profile.
