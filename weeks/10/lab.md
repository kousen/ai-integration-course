# Lab: Your team's agent, the second host

**Time:** about 60 minutes of your own work, with your team. This lab is homework; in the last ten minutes of class your team chooses its two decisions (step 1).

Team Project 2 needs two hosts for one server. Claude Code is the first. This lab builds the second: your own loop, connected to your team's server, carrying out your task, with stopping rules you chose and tested. It is short on purpose, because it is the week of Thanksgiving and because it is work Team Project 2 needs anyway.

The lab lives in your **team's TP2 repository** and is a team submission with **one grade for the team**. The worked example is [`examples/agent-loop`](../../examples/agent-loop/); read its README first and run its tests.

## 0. Working rules (5 minutes)

One member adds `openrouter` to `requirements.txt` and to **Dependencies** in `spec.md` with its reason (if it is not there already), and adds to `CLAUDE.md` under **Working rules**:

```markdown
- Week 10: agent.py is our own loop and the second host for server.py. No
  agent framework. It discovers the tools from the server; it does not
  import them.
- The loop always has a step cap and a cost cap. Every way a run can end
  has a no-key test with a scripted model, written before the code.
- A tool that changes something runs only after a person approves it in the
  host. With nobody to ask, it is denied.
- memory.json and any pending file are in .gitignore.
```

Commit (`git commit -am "Week 10 working rules"`), push, and everyone pulls.

## 1. Choose two decisions (10 minutes, in class)

Every team's agent has the **step cap and the cost cap**. Those are required by the TP2 sheet and are not a choice.

Then choose **two more** of these for your task, and write in `plan.md` why your task needs each one:

| Decision | Choose it if |
|---|---|
| A plan first | your task takes three or more tool calls in an order that matters |
| The repeat rule | a tool of yours can fail in a way the model might retry unchanged |
| A context budget | a tool of yours returns long results (documents, file contents, long lists) |
| Memory between runs | your task improves when the agent knows something from last time |
| An approval gate | your server has any tool that changes something. **If it does, this one is required** and counts as one of your two |

## 2. The plan (10 minutes)

```text
Read spec.md and examples/agent-loop/agent.py from the course repository.
Add a "Week 10: the agent" section to plan.md: the files (agent.py,
tests/test_agent.py), the two decisions we chose and why our task needs
them, the step cap and cost cap with their values and how we chose the
values, who is doing what, risks, and Proof. In Proof, list every way a
run can end and the no-key test that covers it. Do not write code.
```

Ask at least two of these, and correct the plan from the answers:

- "For each way a run can end, who decided it ended: the model or the program?"
- "Our cost cap is checked before each call. By how much can one run exceed it, and is that acceptable?"
- "The model writes a plan and then does something else. What does our program do about that?"
- "What would have to be in a tool result, or in memory.json, for the agent to call our side-effect tool when the user never asked for it? What stops it?"

Fill in **Approved by**, commit `Approve plan (week 10)`.

## 3. Tests first, with a scripted model (15 minutes)

```text
Write tests/test_agent.py before agent.py exists, following
examples/agent-loop/tests/test_agent.py: a FakeLLM that returns scripted
replies, and our real server connected in memory with Client(mcp). No key,
no network. Cover: one tool call then an answer; the step cap; the cost
cap; and each of our two decisions. Run them so I see them fail, then stop.
```

At least **six tests**: the baseline, one for each cap, and at least one for each of your two decisions (an approval gate needs two: denied and approved). If neither decision is the approval gate, that list is five: make the sixth a second case for one of your decisions, such as the same successful call twice not ending the run. In each test, the script says what the model "did" and the assertions say what the program did about it.

Commit the failing tests: `git commit -m "Agent: tests, failing"`.

## 4. The agent (10 minutes)

```text
Implement agent.py so the tests pass. Start from
examples/agent-loop/agent.py and keep only the decisions in our plan. It
connects to our server.py, discovers the tools, and never imports them.
Put the names of our tools that only read in READ_ONLY, so that every
other tool needs a person's yes. Run the tests and show me
the output.
```

Read what the agent wrote. Find the `if` for each way a run can end, and make sure any member of the team can point to it.

Commit: `git commit -m "Agent: the loop"`.

## 5. Run your task on two models (10 minutes)

Run your TP2 task through `agent.py` on two models, twice each. In `CHECKS.md`, a **Week 10** section with one row per run:

| Model | stopped_by | Steps | Cost | Right? |
|---|---|---|---|---|

Then once, on purpose, trip each cap (`--max-steps 1`, and a cost cap of a fraction of a cent) and add those two rows. Paste one full trace from stderr below the table.

This table is also the start of the billed eval for TP2's Test milestone.

## 6. What you found (5 minutes)

In `CHECKS.md`, under the table:

- **Two hosts**: you asked Claude Code this task last week. What did your own loop do differently, and what does Claude Code do that yours does not?
- **Our two decisions**: for each, one sentence on what it changed in a real run, or that it never triggered and why you are keeping it anyway.
- **What the model controls**: one sentence. **What the program controls**: one sentence.

```bash
git add . && git commit -m "Agent: checks and findings"
git tag week10-submitted
git push origin main week10-submitted
```

One tag for the team, and one Moodle submission for the team.

## If you finish early

- Add a third decision from the table.
- Write a note into `memory.json` by hand that tells the agent to call your side-effect tool, run a harmless task with memory on, and record what happened and what stopped it.
- Run `agent.py` against your server over HTTP (`--server http://localhost:8000/mcp`). If your team is deploying the server, this is the same command with a different URL.
- Make the plan checkable: have the model return the plan as JSON (Week 3), and have the program report any tool the trace used that the plan did not name.

## If you are blocked

Say so early. The usual problems: the agent cannot start the server (run `python3 server.py` yourself from the repository root and read the error; activate the virtual environment first); the model answers without calling any tool (the system prompt must say to answer only from tool results, and the tool docstrings must say when to call them); the reply is empty on `xiaomi/mimo-v2.6-flash` (hidden reasoning must be off for that model: keep the `REASONING` table); the step cap trips on every run (print the trace and look for a call repeated with the same arguments); a test fails with `the agent asked the model again after the script ran out` (the FakeLLM needs one more reply, or the loop should have stopped); a test calls the network (a tool was not faked); `KeyError: OPENROUTER_API_KEY` (the key is not set in this terminal).
