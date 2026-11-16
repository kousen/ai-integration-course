# Lab: Your team's MCP server

**Time:** about 75 minutes of your own work, with your team. This lab is homework; in the last twenty minutes of class your team decides which tools come first (step 1).

Last week your program was the only thing that could call your tool. This week the tool moves behind a Model Context Protocol server, so a host you did not write can discover it and call it. The server is the first working piece of Team Project 2, and this lab is the Build milestone on the [TP2 sheet](../../assignments/team-project-2.md): `plan.md`, and the server running and registered in Claude Code.

The lab lives in your **team's TP2 repository** and is a team submission with **one grade for the team**. Python with the official `mcp` SDK, as the sheet says. The worked example is [`examples/mcp-server`](../../examples/mcp-server/); read its README first.

## 0. Repository and working rules (5 minutes)

Everyone, in the team repository:

```bash
git pull
python3 -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install mcp pytest
```

One member adds `mcp` and `pytest` to `requirements.txt` and to **Dependencies** in `spec.md`, each with its reason, and adds to `CLAUDE.md` under **Working rules**:

```markdown
- Week 9: the MCP server is server.py, built with the mcp SDK version 2
  (MCPServer from mcp.server; not FastMCP). Stages assigned: plan, tests.
- Tests for a tool are written before the tool's code, and go through the
  protocol with an in-memory Client, with no model and no network.
- Nothing is printed to stdout: the host reads it as protocol. Use logging.
- Credentials are read from the server's environment and never returned in a
  result. A tool with a side effect records a pending request; it never
  completes the effect on a model's request.
```

Commit (`git commit -am "Week 9 working rules"`), push, and everyone pulls. Check that `.venv/` and any pending or outbox file are in `.gitignore`.

## 1. Which tools first (5 minutes)

Open `spec.md` at the server's tool list and choose the **two or three tools** the server needs first. They should include:

- one that **reads from the system your task is about** (the course materials, the repository, the document set, the spreadsheet), and
- if your task has any tool that changes something, **that one**, because its gate is the hardest part.

Write them in `plan.md` in the next step, with who is doing what; how you divide the work is up to the team. Every member should be able to explain every tool, as the TP2 sheet says.

## 2. The plan (10 minutes)

```text
Read spec.md and add a "Week 9: the server" section to plan.md: the files
(server.py, client.py, tests/, .mcp.json), the first tools, the
order of work, who is doing what, risks, and Proof. In Proof, list for each tool the misuse
cases its no-key tests cover, and say what registering the server in
Claude Code proves that the tests do not. Do not write code.
```

Ask at least two of these, and correct the plan from the answers:

- "A host sends this tool an argument of the wrong type. What comes back, and does our function run?"
- "Where does this tool's credential live, and what would have to go wrong for the model to see it?"
- "The server cannot ask the user anything. For the tool that changes something, what exactly happens when the model calls it, and who finishes the job?"
- "Which of these tools could have been a script the agent runs from the shell, and what do we gain by putting it behind a server?"

Fill in **Approved by**, commit `Approve plan (week 9)`.

## 3. Tests first, through the protocol (20 minutes)

For each of the first tools:

```text
We are adding the tool <name> from spec.md. Write its tests first, in
tests/test_<name>.py, using an in-memory client as
examples/mcp-server/tests/test_server.py does: `async with Client(mcp)`.
No model, no network, no subprocess. Run them so I see them fail, then
stop. Do not write the tool yet.
```

At least five tests per tool:

1. The tool is **listed**, and its schema says what the spec says (argument names, types, any range or length limit).
2. A call with the **wrong type** comes back as an error result (`is_error`), and the function did not run.
3. A call with a value **outside the limit** comes back as an error result.
4. A request for something that **is not there** comes back as a normal result that says so, not as an error.
5. A failure of the system behind the tool (not found upstream, no permission, rate limit) comes back as an **error result with a message the model can act on**. Fake the failure; do not call the real system in a test.

For a tool with a side effect, add: after the call, **nothing has left the machine**, and the pending request is on record.

Commit the failing tests: `git commit -m "Server: tests for <name>, failing"`.

## 4. The server (15 minutes)

Create `server.py` with the `MCPServer` object and the `if __name__ == "__main__": mcp.run()` block. Then, for each tool:

```text
Implement the tool <name> in server.py so its tests pass. The schema comes
from the type hints: use Annotated with Field for descriptions and limits.
The docstring is what the model reads to decide when to call the tool, so
write it as an instruction. Raise ToolError for failures the model should
see. Log with the logging module; print nothing. Run the tests and show me
the output.
```

Read the docstring the agent wrote. It is the only thing the model knows about your tool. Rewrite it yourself until it says **when** to call the tool, not just what the tool is.

Commit: `git commit -m "Server: <name>"`. If more than one of you is editing `server.py`, pull often and commit small.

## 5. A host with no model (5 minutes)

Copy `examples/mcp-server/client.py` and change it to call each of your tools once. Run it and read the schemas it prints: that is exactly what a host receives. Paste the output into `CHECKS.md`.

Then, once: add `print("hello")` inside one tool, run `client.py` again, and copy the error into `CHECKS.md`. Remove the `print`.

## 6. Register it in Claude Code (10 minutes)

Add `.mcp.json` at the repository root, and commit it so every teammate gets the server on `git pull`:

```json
{
  "mcpServers": {
    "<your-server-name>": {"command": "python3", "args": ["server.py"]}
  }
}
```

Start `orclaude` **from the repository root with the virtual environment active**, approve the server, and type `/mcp`: your server should be listed as connected, with your tools. Ask one question that needs a tool, and one that asks for the side effect if you have one. Save the session with `/export transcripts/week09-claude-code.txt` and commit it.

Every member should run this on their own machine; one transcript in the repository is enough.

## 7. What you found (5 minutes)

In `CHECKS.md`, a **Week 9** section:

- **Tools**: one line per tool: the number of tests, and what happened when Claude Code called it.
- **Server or skill?** One paragraph: why this task needs a server, and one piece of it that could have been a script or a skill instead, with your reason for the choice you made.
- **The gate**: for the tool that changes something, what the server does, what the host did, and what a person still has to do. If you have no such tool yet, say which TP2 tool will be the first.

```bash
git add . && git commit -m "Server: checks and findings"
git tag week09-submitted
git push origin main week09-submitted
```

One tag for the team, and one Moodle submission for the team.

## If you finish early

- Add a **resource** (data the host attaches, as `profile://skills` is in the example) and find out how Claude Code offers it to you.
- Give your server a credential it needs (`GITHUB_TOKEN`, or a key for your own system) through the `env` block of `.mcp.json` **without committing the value**, and write down how a teammate gets it.
- Start the second host: copy `examples/mcp-server/host.py`, point it at your server, and ask it the question you asked Claude Code. Next week's lab builds on it.
- Run your server with `--http` as the example does and connect both hosts to the URL. Write down what a public URL would need that localhost does not.

## If you are blocked

Say so early. The usual problems: `/mcp` shows the server as failed (start Claude Code from the repository root, with the virtual environment active, so `python3` is the one with `mcp` installed; then run `python3 server.py` yourself and read the error); `ImportError: FastMCP` (that is the version 1 name; use `from mcp.server import MCPServer`); "Failed to parse JSONRPC message" (something printed to stdout); the model never calls your tool (the docstring does not say when to); merge conflicts in `server.py` (pull before you start a tool, commit small); `structured_content` is `None` in a test (annotate the return type, for example `-> dict[str, Any]`).
