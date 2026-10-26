# Week 7: A spoken interface for the portfolio chatbot

**Due:** Monday, November 9, 2026, 1:30 PM, on Moodle.

**Category:** Participation and labs.

Complete the [Week 7 lab](../weeks/07/lab.md). Submit your **portfolio repository** URL and the tag **`week07-submitted`** in the Moodle Week 7 assignment.

## At the submitted tag

- `intent/voice.md`, approved by you.
- `spec.md` with a "Week 7: spoken interface" section: a transcriber component (language decision; model decision naming `openai/whisper-large-v3-turbo` and the comparison transcription model) and a speaker component (model decision naming `microsoft/mai-voice-2.1-flash` with its voice and the comparison model or voice); `openrouter` under Dependencies with its reason; numbered behaviors including the empty transcript, the non-audio reply, word error rate with a stated tolerance and the words that must survive, the three-sentence spoken answer, and the key on the server.
- `plan.md` with a Week 7 section approved before the first code commit, Proof split into no-key tests and the billed eval, with the eval's cost.
- `voice/`: the checker and its tests, the transcriber and speaker, `clips/` with at least two clips of your own voice and `expected.json` written before the model heard them, the transcript files from both transcription models, and the two spoken answers. Tests that call a model are skipped when no key is set.
- `/api/voice` in your server and the recorder on your page, or, if the chatbot does not exist yet, the example's server with your clips and a line in `CHECKS.md` saying so.
- `voice/CHECKS.md`: per clip per model, the word error rate, the missing words, the audio seconds, the cost, and the seconds the call took; which model got your name right; the two spoken answers with characters, bytes, estimated cost, and what each did with your name and the course number; the language experiment if you did one; the linter's findings; the browser check's run; and the **One turn** section with the three costs and the total.
- `.claude/hooks/guard.py` and `.claude/settings.json`, installed.

**No API key in the repository.**

## What Prof. Kousen will look for

| Evidence | Satisfactory for Week 7 |
|---|---|
| Two request shapes, with the bill | Clips transcribed through the transcription endpoint with the audio seconds and cost from the reply; answers spoken through the speech endpoint with characters, bytes, and the estimated cost; both recorded in `CHECKS.md`. |
| Transcript checked by code | The checker computes word error rate against text a person wrote first, reports the words that had to survive and did not, and treats an empty reply as a failure, not a crash. No-key tests cover each case. |
| The transcriber checked | `CHECKS.md` records both models on every clip, which one got your name and numbers right, and what you heard yourself. |
| The loop, with the key on the server | `/api/voice` transcribes, answers through the same function as the typed path, and speaks; the browser sends only audio; the browser check's last three assertions pass and are recorded; one real turn's three costs and total are in `CHECKS.md`. |
| Understanding | You can say why the speech reply carries no bill and where the bill is, why the transcript has to be checked by something other than the transcriber, what one voice turn costs and why that number belongs in the hosting decision, and where the key lives on the host you chose. |

## This week's chain stage

No new stage: intent, spec, plan, tests, and a commit history that shows the tests before the code. The hosting decision (`weeks/07/hosting.md`) goes into `spec.md` before November 30, with the per-turn cost from this lab as its evidence.
