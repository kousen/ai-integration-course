# Week 10: Your team's agent, the second host

**Due:** Monday, November 30, 2026, 1:30 PM, on Moodle.

**Category:** Participation and labs.

Complete the [Week 10 lab](../weeks/10/lab.md) with your team. Submit the **team's TP2 repository** URL and the tag **`week10-submitted`** in the Moodle Week 10 assignment. It is a team submission: one member submits for the team, and the team receives one grade.

The agent built here is the second host that [Team Project 2](team-project-2.md) requires.

## At the submitted tag

- `plan.md` with a "Week 10: the agent" section approved before the first code commit: the two decisions chosen and why the task needs them, the values of the step cap and the cost cap, and Proof listing every way a run can end with the test that covers it.
- `agent.py`: your own loop, with no agent framework. It discovers the tools from the team's server and does not import them. It has a step cap, a cost cap, and the two decisions from the plan. If the server has a tool that changes something, one of the two is an approval gate.
- `tests/test_agent.py`: at least six no-key tests with a scripted model and the real server in memory (the baseline, each cap, each decision), committed before `agent.py`.
- `CHECKS.md` with a Week 10 section: the table of runs on two models (stopped by, steps, cost, right or not), one row for each cap tripped on purpose, one full trace, and the three findings.
- `openrouter` under Dependencies in `spec.md`, with its reason.

**No API key in the repository.** `memory.json` and any pending file are not committed.

## What Prof. Kousen will look for

| Evidence | Satisfactory for Week 10 |
|---|---|
| Tests before the agent | At least six no-key tests with a scripted model, in the commit history failing before `agent.py` and passing after it. |
| Two hosts, one server | `agent.py` connects to the team's server, discovers its tools, and completes the task; nothing is imported from the server. |
| The program stops the run | A step cap and a cost cap, each with a test and each tripped once on purpose in `CHECKS.md`. |
| Two decisions, chosen for the task | Two of plan, repeat rule, context budget, memory, approval gate, each with its reason in `plan.md` and a test. A tool that changes something is behind an approval gate that denies when nobody is asked. |
| Understanding | Any member of the team can point to the line that ends a run in each way, say which endings the model controls, and say what the host's gate does that the server's gate does not. |

## This week's chain stage

No new stage: plan and tests, in the team repository. The table of runs begins the billed eval of Team Project 2's Test stage.
