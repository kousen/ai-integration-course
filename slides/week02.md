---
theme: seriph
title: "CPSC 415 · Week 2 · Inside the harness, and your first API call"
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

<div class="kicker">Trinity College · September 21, 2026</div>

# AI Integration

<div class="big">Inside the harness, and your first API call</div>

Ken Kousen · CPSC 415<br>Monday 1:30–4:10 · MC-225

<!--
1:30. Projector: call classroom support before class if it is still blank;
otherwise students join the Zoom link again as they did on Sept 14.
Due today at 1:30: Week 1 repo + tag, Claude Code 101, pledge. Do not collect
in class; Moodle has them. Recording starts now.
-->

---

# Where we are

<div class="two">
<div>

## Last week

Agent built the app<br>You changed one thing<br>You checked it<br>You explained one piece

</div>
<div>

## This week

Your program calls the model<br>You see what the harness sends<br>You write intent before code<br>You verify with the bill

</div>
</div>

<div class="statement">Two or three trainers from the tag, on the screen, first.</div>

<!--
1:30–1:40. Open two or three student repos at week01-submitted. Ask each:
what did you ask for, change, check? Praise honest CHECKS.md entries,
including failures. Then the Week 1 exit questions: where is the current line
stored, what happens after the last line. Keep it to ten minutes.
-->

---

# Model, harness, application

| Part | Week 1 | Week 2 |
|---|---|---|
| **Model** | Selected through OpenRouter | Same, or a local one |
| **Harness** | Claude Code | Claude Code |
| **Application** | HTML page, no AI calls | **Your program calls the model** |

<div class="statement">Today the application makes the call, so you get to read the call.</div>

<!--
1:40–1:43. The distinction from Week 1 pays off now. The harness is itself an
application that calls a model in a loop; your chat client is the smallest
possible version of the same thing, minus the loop and the tools.
-->

---

# The loop, with the tools named

<div class="big">Read → propose → act → observe → decide</div>

| In the Week 1 demo | The tool that ran |
|---|---|
| Looked at `lyrics.txt` | Read a file |
| Created `index.html` | Write a file |
| Started a local server | Run a shell command |
| Opened the page | Drive a browser |

<!--
1:43–1:47. Each tool is a capability the model asks for and the harness
performs. The model never touches your disk; it emits a request and the
harness decides. That decision is the permission system, next slide.
Source: book Chapter 11, The Harness Is the Pattern.
-->

---

# Permissions are a boundary, not a verdict

| Mode | Reads | Edits | Commands |
|---|---|---|---|
| **Default** | Yes | Asks | Asks |
| **Auto** | Yes | Asks for risky ones | Asks for risky ones |
| **Plan** | Yes | No | No |
| **Bypass** | Yes | Yes | Yes |

<div class="statement">Approving an action says it may run.<br>It does not say the result is right.</div>

<!--
1:47–1:51. Sept 14 demo ran in auto mode; explain what that allowed. Bypass
is for sandboxes you can throw away, not this class. Plan mode is next.
The exact labels and Shift+Tab cycling belong to the current Claude Code
release; verify the names the week of class.
-->

---

# Plan mode

<div class="prompt">Read intent/chat-client.md.<br>Tell me your plan: which file, what it contains.<br>Wait for my approval before writing.</div>

Plan mode makes that request structural: the harness will not edit until you say so.

<p class="note">Week 1 asked for a plan in the prompt. Plan mode enforces it.</p>

<!--
1:51–1:54. Live: switch to plan mode, ask for a plan against the demo intent,
show that it stops. Then approve and let it edit. The Codex training
plan-mode warm-up is the same exercise on the other harness.
-->

---

# Context is everything the model sees

<div class="two">
<div>

## Supplied by the harness

System instructions<br>`CLAUDE.md`<br>Tool definitions<br>Files it read

</div>
<div>

## Supplied by you

Your prompts<br>Your corrections<br>The conversation so far

</div>
</div>

<div class="statement">Every turn sends all of it again.</div>

<!--
1:54–1:58. This is the fact most developers do not know: the API is
stateless. Each request carries the whole session. Show /context in Claude
Code so they can see the breakdown. Connect to Week 1: the model "knew" the
file because the harness put the file in the context.
-->

---

# The window fills

<div class="big">Turn 1 is cheap.<br>Turn 40 carries turns 1 through 39.</div>

| Window | Where you see it |
|---|---|
| Published size | The model's page on OpenRouter |
| Current use | `/context` inside the session |
| Compaction | The harness summarizes to make room |

<p class="note">A model not in the harness's catalog is assumed to have a 200K window; the <code>[1m]</code> suffix from Week 1 tells it otherwise.</p>

<!--
1:58–2:01. Later turns cost more in tokens and, past some point, in quality.
Rules of thumb exist ("start fresh at half full"); present them as rules of
thumb. Reasoning about the middle of a long context is an open research
question; do not cite a number.
-->

---

# When to start fresh

- The task changed. New session, new goal.
- The session is arguing with itself. Summarize what worked, start over with the summary.
- Compaction happened twice. What survived may not be what you needed.
- You want a second opinion. A fresh session, or a different model, has no sunk cost.

<div class="statement">Write the handoff note before you close the session.</div>

<!--
2:01–2:04. The handoff note is a file: what was done, what is next, what to
avoid. It becomes the next session's first message. This is also the habit
that makes CLAUDE.md worth writing.
-->

---

# `CLAUDE.md`

```text
# Chat client
- Python 3, standard library only. No pip installs.
- Read configuration from environment variables; never hardcode a key.
- Before editing, state the plan and wait.
- After editing, show how to run it.
```

<div class="statement">Project memory, read before your first prompt.</div>

<!--
2:04–2:07. Live: add the "standard library only" line to a CLAUDE.md, ask for
a client, and watch it not reach for a package. Then remove the line and ask
again if time. Keep it short; long CLAUDE.md files are context spent on every
turn. The course template ships one.
-->

---

# Parameters

<div class="big">7B fits a laptop.<br>27B wants a lot of memory.<br>Hundreds of billions live in the cloud.</div>

<p>Parameters are the trained weights between the layers, not the nodes.<br>Inference uses them; training is the other course.</p>

<!--
2:07–2:11. Owed from Sept 14. Use the OpenRouter model page for a specific
model as the visual (the "27B" in the name). Frontier model sizes are not
published; say "we do not know" rather than guess. Prof. Chakravorti's
course covers training.
-->

---

# Dense and mixture of experts

| Kind | Loads | Runs per token |
|---|---|---|
| **Dense** | All parameters | All of them |
| **Mixture of experts** | All parameters | A chosen subset |

<p class="note">A listing such as "2.4T total, 95B active" is a mixture-of-experts model: the whole thing is stored, a fraction is used for each token.</p>

<!--
2:11–2:14. Example seen in class Sept 14 was a Qwen 3.8 listing on OpenRouter.
Recheck the exact numbers on the model page before projecting. Point: active
parameters set the memory needed to run; total parameters set the download.
-->

---

# Open weights, not open source

<div class="two">
<div>

## Published

The weights<br>A license<br>Often the architecture

</div>
<div>

## Usually not published

Training data<br>Training process<br>Evaluation details

</div>
</div>

<div class="statement">You can run it. You cannot rebuild it.</div>

<!--
2:14–2:16. Many of the models on the OpenRouter leaderboard are open weights.
Distillation came up on Sept 14; if asked, describe it as training a smaller
model on a larger model's outputs, and leave the news story out of the slides.
-->

---

# Long context has a price

- Providers quote **per million tokens**, input and output separately.
- Some charge a **higher rate past a context threshold**.
- **Cached input** can be cheaper when the same prefix repeats.

<div class="statement">Read the pricing page for the model you are using, today.</div>

<p class="note">Numbers change monthly. The slide has none on purpose.</p>

<!--
2:16–2:20. Sept 14 showed one provider's page with short/long-context tiers
and a cache discount; open the same page live rather than quoting figures
from memory. Tie back: a long session in the harness is a long-context
request every turn.
-->

---

# What a chat request contains

```json
{
  "model": "vendor/model-name",
  "messages": [
    {"role": "system", "content": "Answer briefly for a college student."},
    {"role": "user",   "content": "What is a context window?"}
  ],
  "max_tokens": 600,
  "temperature": 0.2
}
```

<p class="note">Sent as JSON to <code>/chat/completions</code> with your key in a header.</p>

<!--
2:20–2:24. This is the OpenAI-compatible shape that OpenRouter, Ollama, and
LM Studio all accept. Roles: system sets the frame, user asks, assistant is
what comes back and what you send back next turn to continue. There is no
memory on the server; the messages array is the memory.
-->

---

# What comes back

```json
{
  "model": "vendor/model-name",
  "choices": [
    {"message": {"role": "assistant", "content": "A context window is ..."},
     "finish_reason": "stop"}
  ],
  "usage": {"prompt_tokens": 33, "completion_tokens": 41}
}
```

<div class="statement">The <code>usage</code> block is what you pay for.<br>The <code>content</code> is what you check.</div>

<!--
2:24–2:27. Point at finish_reason: "stop" is the model's choice, "length"
means max_tokens cut it off. Some models also return a reasoning field and
spend output tokens on it before the visible answer; the reference client
rehearsal hit exactly that with a 200-token cap and got an empty answer.
-->

---

# Parameters you can set

| Parameter | What it does |
|---|---|
| `max_tokens` | Caps the output, including any hidden reasoning |
| `temperature` | Lower favors the most likely next token; higher spreads the choice |
| `stream` | Sends the answer as it is generated |
| `system` message | Sets the frame every answer is generated inside |

<p class="note">Same names across most providers. Defaults differ. Read the docs for yours.</p>

<!--
2:27–2:30. Describe; do not claim which setting is "best." Temperature demo
if time: same question at 0 and at 1, twice each. Streaming is out of scope
for the lab, mention it exists.
-->

---

# Same request, different destinations

| Destination | Base URL | Key |
|---|---|---|
| **OpenRouter** | `https://openrouter.ai/api/v1` | Your OpenRouter key |
| **Local model** | `http://localhost:PORT/v1` | Any string |
| **A vendor directly** | The vendor's URL | That vendor's key |

<div class="statement">One program. Change two environment variables.</div>

<!--
2:30–2:33. The coding agent has the same property: orclaude sets a base URL
and key; a Claude Enterprise seat, if issued, is plain `claude` with no
wrapper. If seats exist by today, say how to keep the two routes separate.
If they do not, say nothing beyond "still pending."
-->

---

# Running a model on your own machine

| Tool | What it is |
|---|---|
| **Ollama** | Command line and background service; pull, run, serve |
| **LM Studio** | Desktop app: model browser, chat window, local server |
| **llama.cpp** | The engine under many of these; loads model files directly |

<p class="note">All three serve the request shape you just saw. None is required for this course.</p>

<!--
2:33–2:38. Demo on Ken's Mac with Ollama and a model already pulled (gemma4
12B or qwen3.8 27B, both MLX builds on Apple Silicon). Run the reference
client against localhost. Show speed, show the answer, show a question it
gets wrong or refuses that the hosted model handled. Verify LM Studio and
llama-server ports/flags the week of class; they change.
-->

---

# Where a small model falls short

<div class="big">Slower. Shorter memory. Less reliable on hard questions.<br>Free after the download, and private.</div>

<div class="statement">Show it. Do not assert it.</div>

<p class="note">For some components it is good enough. That is a design decision you will document.</p>

<!--
2:38–2:42. Syllabus: local models are a legitimate zero-cost choice where
they are good enough. Same question to the hosted model and the local one,
side by side, is the whole argument. Then break, Ken's timing.
-->

---
layout: center
---

<div class="kicker">Chain stage 1 · Plan</div>

# Intent before spec before plan

<div class="big">Goal · Who it is for · Constraints<br>Not in scope · Success looks like · Open questions</div>

<div class="statement">The agent drafts it. You approve it. Then code.</div>

<!--
2:55–2:58 after the break. The six headings are the template's. The AI-Native
SDLC Playbook calls this the Plan stage; the artifact-chain template calls
the file intent.md. One intent per feature or component, under a page.
-->

---

# The discovery interview

<div class="prompt">I want to build a small chat client.<br>Before writing anything, interview me.<br>Ask one question at a time until you can fill in every section of intent/TEMPLATE.md.<br>Then write your draft to intent/chat-client.md and stop.</div>

<div class="statement">"I don't know" is an answer. It goes under Open questions.</div>

<!--
2:58–3:05. Live, with Ken as the interviewee. Answer some questions vaguely
on purpose so the draft has something to correct. Stop the agent if it
starts asking three questions at once; one at a time is the point.
-->

---

# Correct the draft

- It assumed a package you did not ask for. Strike it; say "standard library only."
- It promised streaming. Move it to **Not in scope**.
- It wrote a success criterion it cannot check. Replace it with one you can.

<div class="statement">Sign it. <code>Approved by: your name, date.</code></div>

<!--
3:05–3:10. Make two corrections live in the file, not in the chat, then
commit "Approve intent". The signature line matters: it is the moment
responsibility moves from the draft to you. Students start the lab now.
-->

---
layout: center
---

<div class="kicker">3:10–3:45 · Lab</div>

# Interview, intent, build

<div class="big">Template repository → interview → approve → plan → run</div>

<p class="note">Python or Java. Standard library only. Key from the environment.<br>The full lab is in <a href="https://github.com/kousen/ai-integration-course/blob/main/weeks/02/lab.md">weeks / 02 / lab.md</a>.</p>

<!--
Circulate. Common failures: the agent writes code before the interview ends
(restart in plan mode); a pip install appears (CLAUDE.md line); the key gets
pasted into the prompt (stop, revoke, new key). Checkpoint D first if anyone
skipped setup.
-->

---

# Verify the call

| Evidence | Where |
|---|---|
| The model that answered | OpenRouter Activity, not the program's print statement |
| Tokens in and out | Activity page beside your program's usage line |
| The request shape | Ask the agent to show the JSON it sends |
| A parameter's effect | `max_tokens` at 20; changed system prompt |

<div class="statement">The response's description of itself is not evidence.</div>

<!--
3:45–3:52. Same principle as Week 1's /status check. Expect a few empty
answers at max_tokens 20 from reasoning models; that is the finding, record
it. Token counts may differ slightly between program and provider; ask why.
-->

---

# Swap the model

<div class="big">Change <code>CHAT_MODEL</code>. Same question.<br>Write down both answers and both costs.</div>

<p>Then, if you have one running: change <code>CHAT_BASE_URL</code> to localhost.</p>

<div class="statement">One question, two observations. Not a benchmark.</div>

<!--
3:52–4:00. Name the second hosted model in class (pick from the rehearsed
list). Students with a local model try it; nobody installs one now. README
language: "for this question I observed," never "model X is better."
-->

---

# Save evidence of the work

```text
intent/chat-client.md   Drafted by the agent, corrected and signed by you
chat.py or Chat.java    Reads the environment, sends one question
CHECKS.md               Six checks, expected and observed
README.md               Corrections, one code explanation, the comparison
```

<div class="statement">Commit. Tag <code>week02-submitted</code>. Push both.</div>

<!--
4:00–4:04. The template's spec.md and plan.md stay untouched this week.
Intent is the only required artifact. Anyone whose push fails keeps local
commits and finishes after class with help.
-->

---

# Before next Monday

**September 28 · 1:30 PM**

- Submit your repository URL and `week02-submitted` tag.
- Upload your **AI Fluency for Students** certificate.

**Next week:** from intent to `spec.md`, structured output, a five-case eval, and **teams are formed**. Team Project 1 and the portfolio intent are assigned.

<p class="note">Thinking about an Elting Center sandbox project instead? Tell Prof. Kousen this week.</p>

<!--
4:04–4:08. The sandbox choice affects team formation next week, so collect
signals now. Danny's slides and the recording are on Moodle under Week 1.
-->

---
layout: center
---

# Before you leave

<div class="big">What did the interview get wrong?<br>What did your program send?<br>What did the bill say?</div>

<div class="statement">Three answers, then go.</div>

<!--
4:08–4:10. Verbal exit check. Note anyone still without a working call.
-->

---

# Sources and next steps

<div class="small">

- Ken Kousen, *Claude Code: Up and Running*: Chapters 3–5 and Chapter 11 on context and the harness. Draft readings via Moodle.
- [Artifact-chain template](https://github.com/kousen/artifact-chain-template): the intent template used today.
- [The AI-Native SDLC Playbook](https://claude.com/blog/the-ai-native-sdlc-playbook): the Plan stage.
- [OpenRouter quickstart](https://openrouter.ai/docs/quickstart) · [Ollama OpenAI compatibility](https://docs.ollama.com/openai) · [LM Studio](https://lmstudio.ai) · [llama.cpp](https://github.com/ggml-org/llama.cpp)
- [Claude Code training](https://github.com/kousen/claude-code-training) · [Codex training: plan-mode warm-up](https://github.com/kousen/codex-training/tree/main/exercises/plan-mode-warmup)
- Reference clients rehearsed September 15 against a local Ollama model; hosted rehearsal before class.

</div>

<p class="note">Prepared September 15, 2026. Recheck permission-mode names, local-server ports, and pricing pages before class.</p>
