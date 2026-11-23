# Week 10: Agents from scratch

**Monday, November 23, 2026 · 1:30–4:10 PM · MC-225**

Last week's `host.py` was already a loop: the model asked for a tool, the program ran it, and the result went back. This week that loop becomes an agent, with no framework, by adding six decisions the program makes: ask for a plan first, let the model revise after an error, keep the conversation inside a budget, remember something between runs, ask a person before anything that changes the world, and stop. Each one is a few lines of Python and each one has a test that needs no key. Then the same six are found, by name, in the coding agent you have used all semester. The lab connects this loop to your team's server, which makes it Team Project 2's second host.

By the end of the session, you should be able to:

- Say what separates a workflow from an agent, and where your own TP2 system sits.
- Name the four ways a run can end (`answer`, `steps`, `cost`, `repeat`) and say which of them the model controls.
- Add a planning call to a loop and say what the program does and does not enforce about the plan.
- Return a tool error so the model can revise, and stop a model that repeats a failing call.
- Keep a conversation inside a context budget by summarizing, and say what summarizing can lose.
- Give an agent memory between runs, and explain why a saved note is untrusted input.
- Put an approval gate in the host, and say how it differs from the gate in the server.
- Test every one of those with a scripted model, before paying for a single call.

## Today's materials

1. [Lab: Your team's agent, the second host](lab.md) (homework; started in class; due November 30)
2. [Week 10 slides (PDF)](../../slides/week10.pdf) · [Slide source](../../slides/week10.md)
3. [Week 10 submission requirements](../../assignments/week10-agent.md)
4. [The agent loop example](../../examples/agent-loop/): `agent.py` and 37 no-key tests
5. [Team Project 2: Agentic / MCP System](../../assignments/team-project-2.md), due December 7

Setup is the same as last week: a virtual environment with `pip install mcp openrouter pytest`.

## Our afternoon

| Time | Activity |
|---|---|
| 1:30–1:40 | What is due; Team Project 2 dates |
| 1:40–2:00 | What makes a system an agent; the loop you already have; six decisions |
| 2:00–2:45 | **Live A–D:** the baseline; a plan; errors and the repeat rule; a context budget |
| 2:45–2:55 | Break |
| 2:55–3:35 | **Live E–H:** memory; approval; the two caps; a note nobody should have trusted |
| 3:35–3:50 | **Live I:** the same six in Claude Code; subagents |
| 3:50–4:10 | The lab; ten minutes with your team; questions |

## Team Project 2 dates

- **Presentations are in class on Monday, December 7 (Week 12)**, the same day the project is due at 1:30 PM. Ten minutes per team plus five for questions, order drawn at the start of class.
- **November 30 (Week 11):** the Deploy milestone and this week's lab.
- December 14 (Week 13) is portfolio walkthroughs, not Team Project 2.

## Due today at 1:30 PM

- The [Week 9 submission](../../assignments/week09-mcp-server.md): your team's TP2 repository URL and the tag `week09-submitted`. One submission per team.
- **Team Project 2 milestones:** Build (the Week 9 lab) and Test. See the [TP2 sheet](../../assignments/team-project-2.md).

## After class

**Due Monday, November 30, at 1:30 PM:**

- The [Week 10 submission](../../assignments/week10-agent.md): the lab, in your team's TP2 repository, tag `week10-submitted`. One submission and one grade per team.
- The [Introduction to Subagents](https://academy.claude.com/courses/introduction-to-subagents) **or** [Introduction to Agent Skills](https://academy.claude.com/courses/introduction-to-agent-skills) certificate, uploaded to Moodle. Your choice of the two.
- **Team Project 2 milestone:** Deploy. See the [TP2 sheet](../../assignments/team-project-2.md).

### Reading and viewing to support the work

- [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) (Anthropic): workflows and agents, and the advice to start with the simplest thing that works.
- [The lethal trifecta](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) (Simon Willison): private data, untrusted content, and a way to send data out, and why an agent with all three is exposed.
- [Claude Code: MCP](https://docs.anthropic.com/en/docs/claude-code/mcp), for comparing your second host with the first.

## What comes next

Week 11 (November 30) is skills, subagents, and harnesses, with the Maintain stage: your team packages a skill and puts its eval in CI. Week 12 (December 7) is the Team Project 2 presentations.
