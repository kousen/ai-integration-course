# Lab: Hear, think, speak

**Time:** about 60 minutes of your own work, plus a few minutes recording. This lab is homework; the last ten minutes of class walk through it.

Your portfolio chatbot gets a spoken interface: a visitor asks a question out loud, your server transcribes it, the chatbot answers from the profile as it already does, and the answer is spoken back. Along the way you check the transcript in code, because a transcript is model output and can be confidently wrong in exactly the places that matter to a recruiter, which are names and numbers. The lab lives in your **portfolio repository**, because that is where the chatbot and its chain are.

If your chatbot is not answering from the profile yet (the November 2 milestone), do the lab against `examples/voice-loop/profile.json` and the example's answer step, and swap in your own when it exists. The tests and the checker are the same either way.

Python with the OpenRouter SDK is the path the example takes. Any language is allowed if `spec.md` says why; the two requests are small.

## 0. Repository, dependencies, and working rules (5 minutes)

In your portfolio repository, from the root of the clone:

```bash
git pull
mkdir -p voice/tests voice/clips
grep -q openrouter requirements.txt || echo openrouter >> requirements.txt
pip install -r requirements.txt pytest ruff            # in the virtual environment
echo '{"tool_name":"Bash","tool_input":{"command":"pip install openrouter"}}' | python3 .claude/hooks/guard.py
```

The last line prints "openrouter is not in spec.md" unless your spec already names it; step 1 fixes that. (The Week 5 guard must be installed here too: copy `examples/guardrail-hook/` if it is not.) In `CLAUDE.md`, under **Working rules**, add:

```markdown
- Week 7: the spoken interface lives in voice/. Stages assigned: intent, spec,
  plan, tests. Commit to main.
- Transcription and speech calls are billed. One transcription per clip, one
  speech call per answer, never a model call inside a loop of tests. Fixture
  clips are WAV; expected.json is written by a person before the model hears it.
- The spoken answer is the chatbot's answer: the refuse-to-fabricate rule
  applies to what is said aloud exactly as to what is typed.
```

Commit (`git commit -am "Week 7 working rules"`) and start `orclaude` with the model announced in class.

## 1. Intent and spec (10 minutes)

```text
Interview me until you can write intent/voice.md, one question at a time.
A visitor to my portfolio site will ask the chatbot a question by voice.
The server transcribes the recording, the chatbot answers from the profile
exactly as it does for typed questions, and the answer is spoken back. The
transcript is model output and may be wrong; the program must check it
where it can and make the rest visible. Do not write code or a spec yet.
```

Correct the draft, fill in **Approved by**, commit. Then:

```text
Read intent/voice.md and add two components to spec.md under a "Week 7:
spoken interface" heading, each with a language decision and a model
decision. The transcriber calls OpenRouter's transcription endpoint through
the openrouter SDK (name it under Dependencies with the reason) with
openai/whisper-large-v3-turbo as the default and one comparison
transcription model; it records the text, the audio seconds, and the cost
per clip. The speaker calls the speech endpoint with
microsoft/mai-voice-2.1-flash and a named voice as the default and one
comparison speech model or voice; it records characters, bytes, and cost.
Number the behaviors, including: an empty transcript is a failed transcript,
not a crash; a reply that is not audio is an error, never saved as audio;
expected text is compared in code by word error rate with a stated
tolerance, and named words (my name, the course number) must survive;
the spoken answer is at most three sentences with no markdown; the key
stays on the server and the browser sends only audio. Do not write code.
```

Check it against the intent, correct one thing, commit `Approve spec (week 7)`. Now `pip install openrouter` passes the guard.

## 2. The plan (5 minutes)

```text
Read the Week 7 section of spec.md and add a "Week 7" section to plan.md:
files under voice/, order of work, risks, and Proof. In Proof, separate the
tests that run without an API key (the checker: word error rate, words that
must survive, the empty transcript, spacing and case) from the billed eval
(each fixture clip and each of my own clips transcribed once on two models,
one speech call per model), and say what each proves and what it costs.
Do not write code.
```

Ask at least two questions and correct the plan from the answers:

- "If the transcriber turns my name into a different word, what does the chatbot do with the question, and which test notices?"
- "What does one voice turn cost on the class models, and what happens if a visitor holds the button down for a minute?"
- "What does the server do with a recording in a format the model rejects?"

Fill in **Approved by**, commit `Approve plan (week 7)`.

## 3. Tests first, then the checker (10 minutes)

```text
Implement the Week 7 plan one step at a time. For each step write the tests
first, run them so I see them fail, then write the code and run them again,
showing me the output. You may read ../ai-integration-course/examples/voice-loop/
for the request shapes, but the tests come from spec.md. Stop after each step.
```

The no-key tests cover the checker on hand-written transcripts: a perfect transcript scores zero; one substituted word in thirteen scores one thirteenth; the empty reply scores one and is reported, not raised; a name that must survive is reported even when the rate is within tolerance; a number read as words is a miss; spacing and case do not count. `examples/voice-loop/tests/test_check.py` is the shape to aim for. Run `ruff check .` and record what it found.

Commit after the first green run: `git commit -m "Voice: transcript checker with tests"`.

## 4. Your own voice (10 minutes, about $0.002)

The course clips were spoken by a model, which is a weaker test than a person in a room. Record **two clips of your own voice**, five to ten seconds each: one question from your adversarial test set that the profile can answer, and one it cannot. Write what you said into `voice/clips/expected.json` **before** the model hears it, with the words that must survive (your name, a project name, a number). Then, with the key in your environment:

```bash
cd voice
python3 transcribe.py --set clips/expected.json                                   # class model
python3 transcribe.py --set clips/expected.json --model elevenlabs/scribe-v2 --out transcripts-scribe.json
```

`CHECKS.md` gets one line per clip per model: the word error rate, the words that went missing, the audio seconds, the cost, and the seconds the call took. If you speak another language, record one clip in it and transcribe it with `--language xx` and without; record what changed. The three course clips go through the same two models so you have a baseline a person did not speak.

Then, in your own terminal (not through the agent), play the clip and read the two transcripts aloud. Which model got your name right? Record it.

Commit: `git commit -m "Voice: own clips transcribed on two models"`.

## 5. The answer, spoken (5 minutes, about $0.01)

Take the chatbot's typed answer to your first clip and speak it twice: once with the class model and voice, once with a comparison (`--model elevenlabs/eleven-v4-turbo --voice george`, or a different locale of the class model such as `en-IN-Priya:MAI-Voice-2.1-Flash`). Record characters, bytes, the estimated cost, and the seconds for each in `CHECKS.md`, and listen to both. Note what each voice did with your name, the course number, and any abbreviation. If you speak another language, speak the answer in it with a voice for that locale and say whether it sounded like a native speaker to you.

Commit: `git commit -m "Voice: the answer spoken, two voices"`.

## 6. The loop, in your server (15 minutes, about $0.02)

Add `POST /api/voice` next to your chatbot's route, in whatever framework the portfolio uses: body is the recording, the content type says the format, the server transcribes, calls the same answer function the typed path uses, speaks the reply, and returns JSON with the transcript, the answer, the audio as base64, and the three costs. Add the recorder to the page (`examples/voice-loop/index.html` is forty lines; the file picker fallback is three of them). Cap what the server accepts (the example takes 10 MB and refuses unknown types with 415).

Then prove it the Week 5 way: adapt `examples/voice-loop/test_browser.py` to your page, run it with your server up, and read its last three assertions out loud. Try the microphone yourself, once, with a question from your test set: write the transcript, the answer, and the three costs into `CHECKS.md` as the **One turn** section, with the total. That total is what a visitor costs you per question; it belongs in `spec.md` under the hosting decision (Week 7's `hosting.md`) before November 30.

```bash
cd path/to/portfolio
git add . && git commit -m "Voice: the loop, with the browser check"
git tag week07-submitted
git push origin main week07-submitted
```

## If you finish early

- Send one of your own clips through the chat endpoint instead, as an `input_audio` content part on an audio-capable chat model, with the question "what did the speaker ask, and in what tone?" Note what you got that the transcription endpoint cannot give you, and what it cost.
- Ask the speech model for `pcm` and write the WAV yourself with Python's `wave` module, as `speak.py` does; compare the file sizes and what each transcriber makes of each.
- Run the Week 6 reviewer (`examples/pr-review/review.py`) over your `voice/` diff before you tag; record its findings by pass in `CHECKS.md`.

## If you are blocked

Say so early. The usual problems: the guard refusing `pip install openrouter` (step 1: the spec names it first); a speech call that returns JSON (a voice the model does not have; the message says so); a transcript that stops halfway (the MP3 header, setup section 3: use WAV); the browser recording as `audio/webm` and the server not mapping it (the example's `FORMATS` table does); the chatbot not existing yet (use the example's profile and answer step, say so in `CHECKS.md`, and swap yours in before November 30).
