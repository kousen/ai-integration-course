# Lab: One real tool, and the ways it goes wrong

**Time:** about 60 minutes of your own work. This lab is homework; the last fifteen minutes of class walk through it.

Your portfolio chatbot gets one real tool: a function your program runs when the model asks for it, with the result sent back as the next message. The tool itself is small. The work is the misuse cases: a call whose arguments do not fit the schema, a call to a tool that does not exist, a loop that never stops asking, a side effect the model requests on its own, and an answer that claims more than the tool returned. Each one gets a test before it gets code, and the tests run without a key, because a scripted model can misbehave on demand and a real one only does it now and then.

The lab lives in your **portfolio repository**, next to the chatbot and the Week 7 voice route. Python with the OpenRouter SDK is the path the example takes.

## 0. Repository and working rules (5 minutes)

```bash
git pull
mkdir -p tools/tests
```

In `CLAUDE.md`, under **Working rules**, add:

```markdown
- Week 8: the chatbot's tools live in tools/. Stages assigned: intent, spec,
  plan, tests. Commit to main.
- The model never runs anything. Every tool request is validated and run (or
  refused) by our code; every problem goes back to the model as a result, not
  an exception. Tools with side effects are never run on the model's request
  alone. The loop has a step cap.
- No model call inside a test that runs without a key; the billed eval is
  separate and skipped when OPENROUTER_API_KEY is unset.
```

Commit (`git commit -am "Week 8 working rules"`) and start `orclaude` with the model announced in class.

## 1. Choose the tool, then intent and spec (10 minutes)

Pick **one** tool that returns something the chatbot's prompt does not already contain:

- **`recent_commits(repo)`**: the last few commits of one of your public repositories, from GitHub's REST API. `examples/tool-loop/github_tool.py` is the whole thing, errors included. Recommended: it is real, it is yours, and it fails in real ways (a repository that does not exist, the rate limit).
- **`request_intro(email, message)`**: a visitor asks to be introduced; the tool would write to an outbox. It has a side effect, so the lab's permission rule is the point of it.
- A tool of your own, if it is about you and returns live data: a reading list, a calendar of talks, the status of a deployed project.

Then:

```text
Interview me until you can write intent/tools.md, one question at a time.
The portfolio chatbot will get one tool: a function our server runs when the
model asks for it, with the result sent back to the model. I have chosen
<the tool>. The model never runs anything itself; our code validates every
request, runs or refuses it, and returns every problem as a result the
model can read. The chatbot must not claim anything the tool did not return.
Do not write code or a spec yet.
```

Correct the draft, fill in **Approved by**, commit. Then:

```text
Read intent/tools.md and add a "Week 8: one tool" section to spec.md: the
tool as a component with a language decision and a model decision (the
class model and one comparison, both of which must support tool calling).
Number the behaviors, including: the schema the model sees (name,
description, JSON Schema arguments); arguments are validated in code
against that schema and a bad call returns an error result; a call to an
unknown tool returns an error result; the loop stops at a step cap and the
answer then is the program's, not the model's; a tool with a side effect is
recorded as pending and not run unless a person confirms; an answer that
names something the tool did not return is flagged by code; every tool call
costs an extra chat call and the eval records the cost per question. Do not
write code.
```

Check it against the intent, correct one thing, commit `Approve spec (week 8)`.

## 2. The plan (5 minutes)

```text
Read the Week 8 section of spec.md and add a "Week 8" section to plan.md:
files under tools/, order of work, risks, and Proof. In Proof, separate the
no-key tests (a scripted fake model: the single-shot call, the bad
arguments, the unknown tool, the endless caller stopped by the cap, the
side effect held, the unsupported claim) from the billed eval (five
questions on two models, the tools called and the answers checked in
code), and say what each proves and what it costs. Do not write code.
```

Ask at least two questions and correct the plan from the answers:

- "If the model asks for the tool with the wrong argument name, what exactly goes back to it, and what does the second test assert?"
- "What stops a model that asks for the same tool ten times, and what does the visitor see when it does?"
- "If the model answers about a repository the tool said does not exist, which line of code notices?"

Fill in **Approved by**, commit `Approve plan (week 8)`.

## 3. Tests first, with a scripted model (15 minutes)

```text
Implement the Week 8 plan one step at a time. For each step write the tests
first, run them so I see them fail, then write the code and run them again,
showing me the output. Use a fake client whose replies are scripted by each
test, as examples/tool-loop/tests/test_loop.py does. You may read
examples/tool-loop/ for the request shapes, but the tests come from
spec.md. Stop after each step.
```

The six no-key tests, at least: the single-shot call delivers the result back as a `tool` message with the right `tool_call_id`; a call with bad arguments gets an error result and the loop continues; a call to a tool that does not exist gets an error result; a model that asks forever is stopped by the cap, and the answer is the program's sentence; a side-effect tool is recorded as pending and its effect does not happen; an answer that names something no tool returned is flagged. Run `ruff check .` and record what it found.

Commit after the first green run: `git commit -m "Tools: the loop and its misuse cases, tests first"`.

## 4. The tool in your chatbot (10 minutes)

Wire the loop into your chatbot's answer function, so the typed path and the voice path both go through it. The profile stays where it is; the tool adds what the profile does not have. Cap the loop at four steps. Keep the trace (which tools were called, with what, and what came back) and return it with the answer, because the next step reads it.

If your chatbot runs on a host where the tool cannot (a static site with the function on Cloudflare Pages, say), the tool runs in the function; the loop is the same.

Commit: `git commit -m "Tools: one real tool in the chatbot"`.

## 5. The billed eval (10 minutes, about $0.01)

Five questions, each on the class model and one comparison model that supports tools, with the tools that must be called, the words the answer must and must not contain, and the claim check, as `examples/tool-loop/tests/test_eval.py` does:

1. A question the tool answers (your latest commits; a real introduction request).
2. A question about something the tool will not find (a repository you do not have).
3. A question the profile answers without the tool (does the model call it anyway?).
4. A question that invites the model to invent a result ("what did you commit yesterday?" when nothing was committed).
5. A question that asks for the side effect, if your tool has one; otherwise a question with two tool calls in it.

`CHECKS.md` gets one line per question per model: the tools called, the number of steps, whether the answer passed, the cost, and the seconds. Then the three totals: cost per question with a tool, cost per question without, and the most steps any question took.

Commit: `git commit -m "Tools: five questions on two models"`.

## 6. What you found (5 minutes)

In `tools/CHECKS.md`, three short sections:

- **Misuse cases**: for each of the six, the test that covers it and, if a real model produced it during the eval, the trace.
- **What the check cannot catch**: at least one invented claim that plain code would miss, and what evidence would catch it (a second model? a person? a stricter prompt?).
- **The cost of a tool**: your numbers for a question with and without a tool call, and what that means for the per-turn cost in your hosting decision.

```bash
git add . && git commit -m "Tools: checks and findings"
git tag week08-submitted
git push origin main week08-submitted
```

## If you finish early

- Give the loop a second tool and ask a question that needs both; watch whether the model asks for them in parallel (one reply, two `tool_calls`) or in sequence, on each model. The example's `test_parallel_tool_calls_each_get_a_result` shows what the program must handle either way.
- Send the same tool schema to a model that does not support tools and record exactly what comes back.
- Write the Anthropic-native version of your schema (`input_schema` instead of `parameters`) and note what else changes in the reply. Next week MCP makes the difference disappear.

## If you are blocked

Say so early. The usual problems: the model never calls the tool (the description does not say when to; make it an instruction); `arguments` arrives as a string (it always does; parse it); the loop reaches the cap on a simple question (read the trace: your error message is what the model is reading, make it say what to do); GitHub's rate limit (`GITHUB_TOKEN`, or wait an hour); the chatbot does not exist yet (do the lab in `examples/tool-loop/` with the fictional profile, say so in `CHECKS.md`, and move it before November 30).
