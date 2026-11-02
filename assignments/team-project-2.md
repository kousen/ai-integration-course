# Team Project 2: Agentic / MCP System

**Assigned:** Monday, November 9, 2026. **Due:** Monday, December 7, 2026, 1:30 PM, on Moodle (group submission: one member submits the repository URL and the tag `tp2-submitted`). Presentations in class that day.

**Weight:** 20% of the course grade. Same four teams as Team Project 1.

## What to build

An **MCP server** that a coding agent can call, and an **agent that uses it** to carry out a task that takes more than one model call. The server is required. It exposes the tools (and, if useful, resources or prompts) that make the task possible; the agent is the loop that plans, calls them, reads what comes back, and decides what to do next. The task is your choice. Examples that fit: a study assistant whose server exposes a course's materials and a quiz bank, and whose agent builds and grades a practice session; a release helper whose server wraps a repository's tests, linter, and changelog, and whose agent prepares a release and refuses when the tests fail; a research assistant whose server searches a document set and records citations, and whose agent writes a sourced brief and flags claims it could not source; a data-cleaning agent whose server reads and validates a spreadsheet and whose agent fixes what it can and reports what it cannot.

Two clients must use the server:

1. **Claude Code** (through `orclaude`, or the Enterprise seat), with the server registered as an MCP server. A saved session transcript in the repository shows the agent completing the task through your tools.
2. **Your own loop**, built on the Week 8 tool loop and the Week 10 agent lab, calling the same server. Same task, your code deciding.

One task, one server, two hosts. If the task works in one and not the other, the presentation says why.

Every team member must be able to explain every part of the submission. That is checked in the presentation and again in the Comprehension Defense.

## The chain is the submission

Submitted as a full artifact chain, as Team Project 1 was. Working code with no chain, or a chain the team cannot explain, earns at most half credit.

| Stage | Artifact | Due |
|---|---|---|
| Plan | `intent/*.md`, one per major feature, each approved by a named team member | **November 16**, tag `tp2-intent-spec` (feedback only) |
| Design | `spec.md`: the task; the server's tools with their schemas; two decisions per component, **language** and **model**, with the alternative considered; every dependency under Dependencies with its reason | November 16, with the intent |
| Build | `plan.md`: files, order, risks, Proof; the server running and registered in Claude Code (the Week 9 lab) | **November 23** (Week 10) |
| Test | No-key tests for every tool's misuse cases (the Week 8 pattern); the billed eval of the task on two models; the side-effect tools gated | November 23 |
| Deploy | At least one reviewed pull request per team member with a `REVIEW.md` pass from a separate reviewing agent; the eval in CI (the Week 11 lab); a skill packaged from the team's reusable workflow | **November 30** (Week 11) |
| Maintain | `CLAUDE.md` current; `ANNOTATION.md` with the four questions per component; the cost ledger | December 7, with the final submission |

Milestones before December 7 are checked in class and get feedback, not grades.

## Rules

- **Python**, with the official `mcp` Python SDK for the server and the `openrouter` SDK for your own loop. Each dependency is justified in `spec.md`.
- Models are your choice and are justified in `spec.md`, with a cheap model compared against a stronger one on the task itself. Both must support tool calling.
- **The program decides.** Every tool validates its arguments in code and returns problems as results. Tools with side effects (anything that writes, sends, deletes, or spends) are gated: the agent records them as pending and a person confirms, or the spec says exactly why that tool is safe to run unattended.
- **The loop has a cap** on steps and on cost per task, and the eval records how often it trips.
- API keys stay in the environment. A key in any commit is treated as compromised.
- Cost: a running total in `README.md`. A project that costs more than about $10 in total should say why. Team Project 1 ran $20–25 for several teams; this one has fewer billed images and should not.
- Everything in the syllabus's Responsible AI section applies. An agent that acts on the world (sends mail, files issues, edits files outside the repository) needs the side-effect gate above and a note in the intent on what it may and may not touch.

## The four-question annotation

For each component, `ANNOTATION.md` answers: What is this? Why this choice? What breaks? What did I learn? "What did I learn" includes at least one place the agent gave confidently wrong output, or called a tool wrongly, that you corrected.

## Presentation (Week 12, December 7)

Ten minutes per team plus five of questions, order drawn at the start of class: the task running live in Claude Code **and** in your own loop (localhost is fine), one artifact from the chain, one thing that failed or that you took out, and the cost ledger. The other teams write notes in the peer form; each team receives the notes written about it.

## What Prof. Kousen will look for

| Evidence | Weight |
|---|---|
| The chain: intent, spec, plan, tests, PR history, eval in CI, annotation, all consistent with each other and with the code | about half |
| The system: the server's tools, validated and gated; the task completed through them by both hosts; the misuse cases tested; the cap and the cost recorded | about half |
| Every member can explain every part | required |
