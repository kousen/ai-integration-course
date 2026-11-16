# Week 9: Your team's MCP server

**Due:** Monday, November 23, 2026, 1:30 PM, on Moodle.

**Category:** Participation and labs.

Complete the [Week 9 lab](../weeks/09/lab.md) with your team. Submit the **team's TP2 repository** URL and the tag **`week09-submitted`** in the Moodle Week 9 assignment. It is a team submission: one member submits for the team, and the team receives one grade.

This lab is also the Build milestone of [Team Project 2](team-project-2.md).

## At the submitted tag

- `plan.md` with a "Week 9: the server" section approved before the first code commit: files, the first tools, order, who is doing what, risks, and Proof.
- `server.py`: an MCP server built with the `mcp` SDK, with at least two tools. Schemas come from type hints; each docstring says when to call the tool. Nothing prints to stdout. No credential in a result or in the repository.
- `tests/`: for each tool, at least five no-key tests through an in-memory client (listed with the right schema, wrong type, out of range, not found as a normal result, upstream failure as an error result), committed before the tool's code. A tool with a side effect also has a test that nothing left the machine.
- `client.py`: a host with no model that lists the tools and calls each once.
- `.mcp.json` registering the server with Claude Code, and `transcripts/week09-claude-code.txt` showing a session that used it.
- `CHECKS.md` with a Week 9 section: the tools table, the output of `client.py`, the stray `print` error, **Server or skill?**, and **The gate**.
- `mcp` and `pytest` under Dependencies in `spec.md`, each with its reason.

**No API key in the repository.**

## What Prof. Kousen will look for

| Evidence | Satisfactory for Week 9 |
|---|---|
| Tests before tools | At least two tools in `server.py`, each with tests that are in the commit history failing before the tool's code and passing after it. |
| Misuse cases through the protocol | At least five no-key tests per tool using an in-memory client: schema as specified, wrong type, out of range, not found as a result, upstream failure as an error result. |
| A host you did not write | `.mcp.json` is committed; the transcript shows Claude Code calling the server's tools; `client.py` lists and calls them with no model. |
| The gate and the credential | A tool that changes something records a pending request and completes nothing on the model's say-so, with a test; credentials come from the server's environment. If the team has no such tool yet, `CHECKS.md` says which one will be first. |
| Understanding | Any member of the team can say what a host learns from your server before any model is involved, why the server cannot ask the user for confirmation, why `print` breaks it, and which part of your task could have been a skill instead. |

## This week's chain stage

No new stage: plan and tests, in the team repository. The next stage for TP2 is Test (November 23, with this lab): the billed eval of the task on two models.
