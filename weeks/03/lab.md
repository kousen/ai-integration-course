# Lab: A structured-output client with a five-case eval

**Time:** about 45 minutes. Start when Prof. Kousen finishes the spec demonstration.

You will build a program that classifies a short customer-support message and returns JSON with three fields, then run it against five known messages and two models. The agent writes the code. You write the intent and approve the spec first, and you decide what the five cases are for.

## 0. Repository and conventions (5 minutes)

Create `cpsc415-week03` from [kousen/artifact-chain-template](https://github.com/kousen/artifact-chain-template) with **Use this template**, make it public, and clone it beside last week's folder. Open `CLAUDE.md` and add these lines under **Working rules**:

```markdown
- This is the Week 3 introductory lab. Stages assigned: intent and spec.
  No plan.md, no branches or pull requests. Commit to main.
- Standard library only, except that Java may add one JSON library jar.
```

Add a **Conventions** entry with your team's choices from the team exercise: language, default model, and how you name files. Start `orclaude` in this folder with the model announced in class.

## 1. Intent, briefly (5 minutes)

You did a full interview last week. This week the interview is short because the task is given:

```text
Interview me until you can write intent/classifier.md, one question at a
time. The program takes one support message, asks a model to classify it,
and prints JSON with category, urgency, and a one-sentence reason.
Category is one of billing, technical, sales, or unknown. Do not write
code or a spec yet.
```

Correct anything the draft got wrong, fill in **Approved by**, and commit: `git commit -m "Approve intent for the classifier"`.

## 2. The spec (10 minutes)

This is the new chain stage. Ask for it:

```text
Read intent/classifier.md and write spec.md from the template. There is
one component. Fill in both design decisions: language, with the
alternative considered, and model, naming the two models we will compare
in the eval. List the behaviors the eval will check, numbered. Do not
write code yet.
```

Read the spec against the intent. If they disagree, the intent wins until you change the intent. Check that:

- **Behavior** lists five numbered checks, including one for a message that is not a support request, which must yield `unknown`.
- **Failure handling** says what happens when the reply is not JSON, when a field has a value outside the allowed set, and when the reply is empty.
- **Cost estimate** has a number in it, even a rough one from last week's usage line.

Correct at least one thing in the file. Commit: `git commit -m "Approve spec"`.

## 3. Build and run the eval (15 minutes)

```text
Read spec.md. Create the program and an eval runner that reads five cases
from a JSON file, calls the program for each, checks the fields the spec
names, and prints PASS or FAIL per case with a summary line. Tell me the
plan first and wait for approval.
```

Approve the plan if it matches the spec. Write the five cases yourself, or edit the agent's draft so that:

1. Three are clear: one billing, one technical, one sales.
2. One is ambiguous between two categories. The case should accept either.
3. One is not a support request at all. The case expects `unknown`.

Run the eval against the class model:

```bash
export CHAT_BASE_URL=https://openrouter.ai/api/v1
export CHAT_MODEL=minimax/minimax-m3
python3 eval.py          # or your Java equivalent
```

Commit once it runs, whatever the score.

## 4. Break it on purpose (5 minutes)

Set `max_tokens` to 400 and run the eval again. Some models spend output tokens on hidden reasoning before the JSON, and at a low budget the reply comes back empty with `finish_reason` set to `length`. Your eval should report that as a failed case, not crash. If it crashes, fix the parser so that a non-JSON reply fails the case cleanly, then put the budget back.

Record both runs in `CHECKS.md`.

## 5. The second model (5 minutes)

Change only `CHAT_MODEL` to `xiaomi/mimo-v2.5` and run the eval again. Then, if a local model is available to you, point `CHAT_BASE_URL` at it and run once more. Record each run: model, cases passed, which case failed and how, tokens in and out from the summary line.

When a case fails on one model and passes on another, ask whether the case or the model is wrong. A case that expects `low` urgency for a sales question is a judgment call; the `unknown` case is not. Say which kind each failure was.

## 6. Explain and save (5 minutes)

`README.md` should have:

- How to run the program and the eval, with the environment variables.
- The five cases and what each one is there to catch.
- The comparison table from `CHECKS.md` and two sentences on what differed. Observations only.
- One correction you made to the spec and why.
- One line of code you can explain: where the JSON is extracted from the reply, or where a case is judged.

```bash
git add .
git commit -m "Classifier with five-case eval, two models"
git tag week03-submitted
git push -u origin main
git push origin week03-submitted
```

## If you finish early

Try OpenRouter's `response_format` parameter with a JSON schema on one of the two models and note whether the number of non-JSON replies changed. Do not make the eval depend on it; not every model honors it.

## If you are blocked

Pair with a teammate and take turns. Record whose environment you used. If the agent starts writing code before the spec is approved, restart in plan mode. If your session was started in the wrong folder and Git complains, exit, check `pwd`, and start again inside the clone.
