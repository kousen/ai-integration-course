---
theme: seriph
title: "CPSC 415 · Week 3 · Structured output, evaluation, and the spec"
colorSchema: light
transition: slide-left
fonts:
  sans: Arial
  serif: Georgia
  mono: monospace
  provider: none
download: false
mdc: true
layout: center
---

<style src="./style.css"></style>

<div class="kicker">Trinity College · September 28, 2026</div>

# AI Integration

<div class="big">Structured output, evaluation, and the specification</div>

Ken Kousen · CPSC 415<br>Monday 1:30–4:10 · MC-225

<!--
1:30. Desk source switcher for the projector. Recording on. Due today: Week 2
repo + tag, AI Fluency certificate. Ask who got the Anthropic email.
-->

---

# Where we are

<div class="two">
<div>

## Last week

Your program called the model<br>You wrote intent before code<br>You verified with the bill

</div>
<div>

## This week

Your program asks for data<br>Five cases say whether it worked<br>You write the spec before code<br>Teams form

</div>
</div>

<div class="statement">Two chat clients from the tag, on screen, first.</div>

<!--
1:30–1:40. Two Week 2 repos at week02-submitted: the intent corrections and
the CHECKS.md table. Then seats: who has the email, nobody switches today.
-->

---

# Same client, a different address

```bash
export CHAT_BASE_URL=http://localhost:11434/v1
export CHAT_API_KEY=ollama            # any string; nothing checks it
export CHAT_MODEL=gemma4:12b-mlx
python3 chat.py "In one sentence, what is a context window?"
```

- No key, no bill, no Activity entry. The cost was the hardware.
- Same request shape. Ollama, LM Studio, and llama.cpp all serve it.
- Slower, and weaker on some questions. Watch for which.

<!--
1:40–1:50, carried over from Week 2. Run it. Then one question the local
model handles worse than M3 did last week; show, do not assert. Then unset
CHAT_API_KEY before the next demo or the OpenRouter call gets a 401.
-->

---

# A prompt is an interface, not a wish

| Pattern | What it does | Costs |
|---|---|---|
| **Role** | "You route support messages." Sets the frame | Almost nothing |
| **Delimiters** | Fences or tags around the data | Almost nothing |
| **Few-shot** | Two or three worked examples | Input tokens every call |
| **Chain of thought** | "Think step by step" | Output tokens; can hurt on simple tasks |

<div class="note">Reasoning models already think before answering. Asking them to think more mostly buys tokens.</div>

<!--
1:50–1:58. Describe each; no claims about which vendor's models need which.
The CoT point: on a three-field classification, asking for reasoning raises
cost and can lower consistency. Show the Week 2 hidden-reasoning finding as
the evidence that thinking already happens.
-->

---

# Ask for data, not prose

<div class="prompt">
Reply with one JSON object and nothing else:<br>
{"category": "billing" | "technical" | "sales" | "unknown",<br>
&nbsp;"urgency": "low" | "medium" | "high",<br>
&nbsp;"reason": "one short sentence"}<br>
Use "unknown" when you cannot tell. Never guess.
</div>

- The shape is in the system prompt. The message is the user turn.
- `temperature` 0: you want the same answer for the same input.
- `unknown` is an allowed answer. Without it, the model invents one.

<!--
1:58–2:04. This is the reference classify.py system prompt. Run it once on a
billing message and once on gibberish; the second must return unknown.
-->

---

# The reply is text until you check it

```python
start, end = text.find("{"), text.rfind("}")
obj = json.loads(text[start:end + 1])
if obj.get("category") not in CATEGORIES:
    raise ValueError(...)
```

- Models wrap JSON in fences, add a sentence, or return nothing.
- Providers offer `response_format` with a schema. Some models honor it; some ignore it. Your parser is the guarantee.
- A reply you cannot parse is a **failed case**, not a crash.

<!--
2:04–2:10. Three failure shapes seen in rehearsal: fenced JSON, empty reply
at a low token budget, urgency outside the allowed set. Mention
response_format as an option students can try at the end of the lab.
-->

---

# Five cases are an eval

| # | Message | Expect | There to catch |
|---|---|---|---|
| 1 | Charged twice this month | billing | the easy case |
| 2 | App crashes on large PDF | technical | the easy case |
| 3 | Discount for 50 seats? | sales, low | urgency judgment |
| 4 | Payment failed, can't log in | billing **or** technical | ambiguity |
| 5 | asdf qwerty %%% | unknown | fabrication |

<div class="statement">Case 5 is the one you will want to skip. It is the one that matters.</div>

<!--
2:10–2:18. Run eval.py on M3: 5/5 in rehearsal. Then the same on MiMo with
CHAT_MAX_TOKENS=400: two empty replies, finish_reason length. The eval
caught it; last week you had to notice by eye.
-->

---

# When a case fails, which is wrong?

<div class="two">
<div>

## The model

Returned prose<br>Invented a category<br>Ran out of tokens

</div>
<div>

## The case

Expected `low` where `medium` is defensible<br>Ambiguous message, one accepted answer

</div>
</div>

<div class="statement">Say which kind it was. Do not edit the case to make the model pass.</div>

<!--
2:18–2:25. Local gemma4 in rehearsal: 4/5, case 3 urgency medium. That is a
judgment-call failure. An empty reply is not. Students classify each failure
in CHECKS.md. Hallucination and refusal: case 5 is the refusal test.
-->

---

# Chain stage 2: the spec

| Stage | Artifact | Who writes | Who approves |
|---|---|---|---|
| Plan | `intent/*.md` | Agent, from the interview | You |
| **Design** | **`spec.md`** | **Agent, from the intent** | **You, against the intent** |
| Build | `plan.md` | Week 4 | |

<div class="statement">If the spec and the intent disagree, the intent wins until you change the intent.</div>

<!--
2:25–2:30. Open the template spec.md. Six headings. Two required decisions
per component. Behaviors are numbered because the eval checks them.
-->

---

# Two decisions per component

<div class="two">
<div>

## Language

Which, and **why**<br>The alternative you considered<br>What it cost you: Java has no stdlib JSON

</div>
<div>

## Model

Which, and **why**<br>What you compared it against<br>On which real task, with what result

</div>
</div>

<div class="note">Today's eval on two models is the model comparison. Write down what happened; that is the "why."</div>

<!--
2:30–2:35. The comparison is an observation on five cases, not a benchmark.
The spec records it as such.
-->

---

# Live: intent to spec

<div class="prompt">
Read intent/chat-client.md and write spec.md from the template. One component. Fill in both design decisions with the alternative considered. Number the behaviors. Do not write code.
</div>

- Read it against the intent. Find the thing it made up.
- Correct it in the file. Commit "Approve spec."

<!--
2:35–2:45. Use last week's demo repo (cpsc415-week02). The agent will invent
a cost estimate or a dependency; correct it live. Break after, Ken's timing.
-->

---

# Teams

- Four teams of two or three.
- Both team projects, or re-form in Week 8.
- Every member explains every part. Checked at the presentation and the Defense.

<div class="statement">Ten minutes: form, name, and write three conventions in a shared note.</div>

<!--
2:55–3:05. Form teams in the room. Each team records: name, members, language
for TP1, default model, one naming rule. That block goes into every team
repo's CLAUDE.md under Conventions. Ken records teams for Moodle groups.
-->

---

# Team Project 1: Multimodal Web App

- Generates images, displays them, critiques them, **plus** vision or audio.
- Due **November 2** with a ten-minute presentation.
- Team intent due **October 5**. Spec and plan October 19. Reviewed PRs October 26.
- Chain and code weigh about the same. Code with no chain: half credit at most.

<div class="note">Sheet: assignments/team-project-1.md</div>

<!--
3:05–3:08. Walk the milestone table. The Week 6 lab wires the image set in
through a reviewed PR, so the repo must exist by then.
-->

---

# Individual Portfolio: the profile site

- A site with a chatbot that answers "should we work together?" **only from your profile**.
- It **refuses to fabricate**. Ten adversarial questions test that.
- Profile, "not yet" inventory, grounding prompt, test set, site. The site is the smallest part.
- `intent/` and `spec.md` due **October 5**. Final December 14. The Defense is over this repo.

<div class="note">Sheet: assignments/portfolio.md · Reference: github.com/kousen/kousenit</div>

<!--
3:08–3:10. Four-question annotation is the Defense. Point at Ken's site for
the shape of the grounding prompt; stack is not the lesson.
-->

---

# Lab: spec, client, eval, second model

<div class="two">
<div>

<span class="step">1</span> Template repo, `CLAUDE.md` lines<br>
<span class="step">2</span> Short interview, approve intent<br>
<span class="step">3</span> Spec from intent, correct one thing

</div>
<div>

<span class="step">4</span> Build; five cases; run<br>
<span class="step">5</span> `max_tokens` 400, run again<br>
<span class="step">6</span> Second model; local if you have one

</div>
</div>

<div class="note">weeks/03/lab.md · 45 minutes · Prof. Kousen circulates</div>

<!--
3:10–3:55. Protect steps 2–4. If time runs short, step 5 becomes "read the
finding in setup.md" and step 6 becomes one run, not two.
-->

---

# Save evidence of the work

```bash
git add .
git commit -m "Classifier with five-case eval, two models"
git tag week03-submitted
git push -u origin main
git push origin week03-submitted
```

`CHECKS.md`: one row per model per run. `README.md`: the five cases and why, the comparison, one spec correction, one line of code.

<!--
3:55–4:00.
-->

---

# Before next Monday

- **October 5, 1:30:** Week 3 submission; portfolio `intent/` and `spec.md`; team intent for TP1.
- Enterprise seat: sign in if the email came; setup walkthrough next week.
- Week 4: retrieval-augmented generation, and `plan.md`.

<!--
4:00–4:05. Three things due; say them twice.
-->

---

# Before you leave

- What is case 5 there to catch?
- When one model fails a case and another passes, what do you write down?
- What are the two decisions every component in a spec must carry?

<!--
4:05–4:10. Answered aloud.
-->

---

# Sources and next steps

<div class="small">

- Ken Kousen, *Claude Code: Up and Running*: chapters on structured output and evaluation, via Moodle.
- [Artifact-chain template](https://github.com/kousen/artifact-chain-template): `spec.md`.
- [The AI-Native SDLC Playbook](https://claude.com/blog/the-ai-native-sdlc-playbook): the Design stage.
- [OpenRouter structured outputs](https://openrouter.ai/docs/features/structured-outputs) · [Ollama OpenAI compatibility](https://docs.ollama.com/openai)
- Reference classifier and eval rehearsed September 22 on `minimax/minimax-m3`, `xiaomi/mimo-v2.5`, and a local `gemma4:12b-mlx`.

</div>

<p class="note">Prepared September 22, 2026.</p>
