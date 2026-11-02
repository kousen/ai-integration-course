# Week 8: Tool use and function calling

**Monday, November 9, 2026 · 1:30–4:10 PM · MC-225**

Until now the model has only ever answered. This week it asks: it writes a request to run one of the functions you described, your program decides whether to run it, and the result goes back as the next message. That one shape is the whole mechanism behind coding agents, MCP servers, and the "agentic" systems of the next four weeks. The lab gives your portfolio chatbot one real tool and then tests the ways a model misuses tools: calls that do not fit the schema, calls to tools that do not exist, loops that never stop, and answers that claim more than the tool returned. Team Project 2 is assigned today.

By the end of the session, you should be able to:

- Write a tool schema (name, description, JSON Schema arguments), say what the model does with it, and say what it cannot do.
- Run the loop: send with tools, read `tool_calls`, run or refuse each one, send the results back, stop when the model answers or when the cap trips.
- Say what a tool call costs and why a question with a tool costs at least two chat calls.
- Name the three failure modes (the bad call, the loop that never ends, the hallucinated tool or result) and the line of plain code that catches each.
- Say why a side-effect tool is never run on the model's request alone, and where you have seen that rule before.
- Describe Team Project 2 and what is due November 16.

## Today's materials

1. [Setup additions](setup.md): pull the repository, one tool call, the no-key tests
2. [Lab: One real tool, and the ways it goes wrong](lab.md) (homework, due November 16)
3. [Week 8 slides (PDF)](../../slides/week08.pdf) · [Slide source](../../slides/week08.md)
4. [Week 8 submission requirements](../../assignments/week08-tool.md)
5. [Team Project 2: Agentic / MCP System](../../assignments/team-project-2.md), assigned today, due December 7
6. [The tool-loop example](../../examples/tool-loop/): `tools.py`, `loop.py`, `github_tool.py`, the no-key tests with a scripted model, the billed eval

## Our afternoon

| Time | Activity |
|---|---|
| 1:30–1:40 | What is due; the peer notes you wrote; the Week 7 lab as seen so far |
| 1:40–2:10 | The model asks, the program decides: the schema, the request, the reply, the result message |
| 2:10–2:40 | **Live:** one tool, one call; the loop with the trace; two models side by side |
| 2:40–2:55 | Break |
| 2:55–3:25 | Failure modes: the bad call, the endless loop, the hallucinated tool; the check in plain code; side effects and permission |
| 3:25–3:40 | Where this goes: Claude Code's tools, the PreToolUse hook, and next week's MCP |
| 3:40–3:55 | **Team Project 2:** the sheet, the milestones, the teams |
| 3:55–4:10 | Lab walkthrough; what is due; questions |

## Due today at 1:30 PM

- The [Week 7 submission](../../assignments/week07-voice.md): your portfolio repository URL and the tag `week07-submitted`.
- The [AI-Native SDLC Playbook](https://academy.claude.com/courses/ai-native-sdlc-playbook) certificate, uploaded to Moodle.
- Portfolio: the repository URL with the required tag in the portfolio assignment.

## After class

**Due Monday, November 16, at 1:30 PM:**

- The [Week 8 submission](../../assignments/week08-tool.md): the lab, in your portfolio repository, tag `week08-submitted`.
- The [Introduction to Model Context Protocol](https://academy.claude.com/courses/introduction-to-model-context-protocol) certificate, uploaded to Moodle (assigned today).
- **Team Project 2 milestone:** `intent/` and `spec.md` in the team repository, tag `tp2-intent-spec` (feedback only). See the [TP2 sheet](../../assignments/team-project-2.md).

### Reading and viewing to support the work

- [OpenRouter: tool and function calling](https://openrouter.ai/docs/features/tool-calling): the request shape, the loop, and which models support it (`supported_parameters` contains `tools`).
- [OpenAI: function calling](https://platform.openai.com/docs/guides/function-calling) and [Anthropic: tool use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use): the same idea in two vendors' native shapes; OpenRouter speaks the first and translates for the second.
- [JSON Schema: getting started](https://json-schema.org/learn/getting-started-step-by-step): the arguments block of every tool is one of these.
- [GitHub REST API: commits](https://docs.github.com/en/rest/commits/commits): the real tool in the lab, no key needed for public repositories.
- [Claude Code hooks](https://docs.anthropic.com/en/docs/claude-code/hooks): the PreToolUse hook from Week 5 is the "program decides" step for a coding agent's tools.

## What comes next

Week 9 (November 16) is the Model Context Protocol: the tool schema you wrote today, standardized so any host can discover and call it. The lab builds an MCP server and connects it to Claude Code; it is the first piece of Team Project 2.
