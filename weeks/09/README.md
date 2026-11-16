# Week 9: The Model Context Protocol

**Monday, November 16, 2026 · 1:30–4:10 PM · MC-225**

Last week you wrote a tool schema that only your own loop could read. The Model Context Protocol is that schema standardized: a server describes its tools, and any host that speaks the protocol can discover them and call them, whether it is Claude Code, a desktop app, an IDE, or the loop you write next week. Today's example puts Week 8's functions behind a server without changing them. After the break the same server gets a second host (a loop like Week 8's, with the tools discovered instead of imported), moves from stdio to HTTP, and is set beside a server someone else runs. The lab is your team's own server, one tool per member, which is the first working piece of Team Project 2.

By the end of the session, you should be able to:

- Name the three roles (host, client, server) and say what travels over stdio between them.
- Write an MCP server in Python with the `mcp` SDK: a tool whose schema comes from type hints, and a docstring that tells the model when to call it.
- Register a server in Claude Code with `.mcp.json` and confirm it with `/mcp`.
- Test a server through the protocol with no model, no network, and no subprocess.
- Say what a server can do that a host cannot (hold a credential) and what it cannot do (ask the user), and what follows for a tool with a side effect.
- Decide between a function call, a skill, and a server for a given capability, and give the reason.
- Connect your own loop to a server as a second host, and say what changes when the server moves from stdio to HTTP.

## Today's materials

1. [Lab: Your team's MCP server, one tool each](lab.md) (homework; owners chosen in class; due November 23)
2. [Week 9 slides (PDF)](../../slides/week09.pdf) · [Slide source](../../slides/week09.md)
3. [Week 9 submission requirements](../../assignments/week09-mcp-server.md)
4. [The MCP server example](../../examples/mcp-server/): `server.py`, `client.py` (a host with no model), `host.py` (a host with one), `.mcp.json`, nine no-key tests
5. [Team Project 2: Agentic / MCP System](../../assignments/team-project-2.md), due December 7

Setup is one line, inside a virtual environment: `pip install mcp pytest`. The example's README has the rest.

## Our afternoon

| Time | Activity |
|---|---|
| 1:30–1:40 | What is due; each team's TP2 task in one sentence |
| 1:40–2:05 | What MCP is: host, client, server; a host that is not a coding agent; one capability, three front doors |
| 2:05–2:20 | When a server and when a skill |
| 2:20–2:55 | **Live A–C:** the server in Python; a host with no model; the same server in Claude Code; credentials, the gate, stdout |
| 2:55–3:10 | Break |
| 3:10–3:50 | Tests through the protocol; **Live D–F:** your own loop as the second host; the same server over HTTP; a server you did not write (Context7) |
| 3:50–4:10 | The lab: each team decides who owns which tool; what is due; questions |

## Due today at 1:30 PM

- The [Week 8 submission](../../assignments/week08-tool.md): your portfolio repository URL and the tag `week08-submitted`.
- The [Introduction to Model Context Protocol](https://academy.claude.com/courses/introduction-to-model-context-protocol) certificate, uploaded to Moodle.
- **Team Project 2 milestone:** `intent/` and `spec.md` in the team repository, tag `tp2-intent-spec` (feedback only).

## After class

**Due Monday, November 23, at 1:30 PM:**

- The [Week 9 submission](../../assignments/week09-mcp-server.md): the lab, in your team's TP2 repository, tag `week09-submitted`. Each member submits individually and names the tool they own.
- **Team Project 2 milestones:** Build (this lab) and Test (the billed eval of the task on two models). See the [TP2 sheet](../../assignments/team-project-2.md).

### Reading and viewing to support the work

- [Model Context Protocol: introduction](https://modelcontextprotocol.io/introduction): hosts, clients, servers, and what tools, resources, and prompts are.
- [MCP Python SDK documentation](https://py.sdk.modelcontextprotocol.io/): version 2 of the SDK. If a tutorial imports `FastMCP`, it was written for version 1.
- [Context7](https://context7.com/): a hosted MCP server that returns current documentation for libraries; free with an API key. An example of a server you connect to and do not write.
- [Claude Code: MCP](https://docs.anthropic.com/en/docs/claude-code/mcp): `.mcp.json`, scopes, and the `/mcp` command.
- Prof. Kousen's [osquery MCP server](https://github.com/kousen/OsqueryMcpServer) and [Starfleet voice interface](https://github.com/kousen/starfleet-voice-interface), with the [video](https://youtu.be/q8sXNXR6iKc): a Java server built with Spring AI, a voice client that is not a coding agent, and the same capability offered as a Claude Code skill.

## What comes next

Week 10 (November 23) is agents from scratch: today's `host.py` with planning and stopping rules, connected to your team's server as its second host.
