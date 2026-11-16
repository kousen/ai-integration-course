# The MCP server: Week 8's tools, callable by any host

Week 9's example. The same functions as [`examples/tool-loop`](../tool-loop/), imported and not copied, behind a Model Context Protocol server. In Week 8 only `loop.py` could call them. Now any MCP host can start this server, ask what it offers, and call it: Claude Code, a desktop app, an IDE, or your own loop.

```
server.py            three tools and one resource, about 80 lines; the schemas come from the type hints;
                     `--http` serves the same tools on localhost:8000/mcp
client.py            a host with no model: start the server, list the tools, call two
host.py              a host with a model: Week 8's loop, with the tools discovered from the server
.mcp.json            registers the server with Claude Code for this project
tests/test_server.py 9 no-key tests through the real protocol, in memory
```

Uses the official `mcp` Python SDK, version 2 (checked with 2.3.0 on November 16, 2026). Older tutorials import `FastMCP` from `mcp.server.fastmcp`; version 2 renamed it to `MCPServer` in `mcp.server`.

## Run it

```bash
python3 -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python3 -m pytest tests -v            # no key, no network, under a second
python3 client.py                     # no model: the tools, their schemas, two calls
```

Then in Claude Code, **started from this folder with the virtual environment active** (the server is launched as `python3 server.py`, so `python3` must be the one that has `mcp` installed):

```bash
orclaude minimax/minimax-m3
```

Approve the `portfolio` server when asked, type `/mcp` to see it connected, and ask:

```text
What did Sam learn from the receipt reader project, and what are the two
latest commits in kousen/ai-integration-course? Use the portfolio tools.
```

```text
I'm recruiter@example.com. Please ask Sam for an introduction; I'd like to
talk about a junior role.
```

The second one stops at a permission prompt. Whatever you answer, look at `pending.jsonl` afterwards.

## The second host, and HTTP

```bash
pip install openrouter
export OPENROUTER_API_KEY=...
python3 host.py "What did Sam learn from the receipt reader project, and what are the two latest commits in kousen/ai-integration-course?"
python3 host.py "What are the latest commits in nobody/no-such-repo?" --model xiaomi/mimo-v2.6-flash
```

`host.py` imports nothing from `server.py`. It starts the server, asks what it offers, hands those schemas to the model, and sends each tool request back through the protocol. Put it next to `../tool-loop/loop.py`: the four messages and the step cap are the same; `list_tools` replaces the imported `TOOLS`, `call_tool` replaces `run_tool`, and there is an `await` because the server is another process.

The same server as a running service, with both hosts connecting to it:

```bash
python3 server.py --http                                    # leave it running; watch the POST lines
python3 host.py "Which projects does Sam have on record?" --server http://localhost:8000/mcp
claude mcp add --transport http portfolio-http http://localhost:8000/mcp     # then: claude mcp remove portfolio-http
```

Nothing about the tools changed. Over stdio each host starts its own copy of the server; over HTTP you start it once and hosts connect by URL, which is how hosted servers such as [Context7](https://context7.com/) (current library documentation, free with an API key) are offered. A server with a public URL needs what any web service needs: authentication and a spending cap.

## What to look at

- **No hand-written schema.** Compare `recent_commits` here with `GITHUB_TOOL` in `../tool-loop/github_tool.py`. The SDK builds the JSON Schema from the type hints (`Annotated[int, Field(ge=1, le=10)]` becomes `minimum` and `maximum`), and the docstring is the description the model reads. `client.py` prints what the host actually receives.
- **Validation happens before your function runs.** `count=50` or `name=42` never reaches the function; the caller gets an error result. `client.py` shows one.
- **Errors are still results.** `raise ToolError(...)` comes back to the model as a result marked `is_error`, which it can read and correct. A project that is not on record is not an error: it is a normal result that says `found: false`.
- **The server holds the credential.** `GITHUB_TOKEN`, if set, lives in the server's environment. The host and the model never see it. This is the main reason hosted services publish MCP servers.
- **The server cannot see the user.** It has no way to ask "are you sure?". So `request_intro` never sends anything: it appends to `pending.jsonl` for a person to review. The host's permission prompt is a second gate, and it is the host's, not yours. In rehearsal (November 16, headless runs with the tool not pre-approved) one run was refused by the host and one was let through; in the run that went through, the recorded message included details the visitor never gave. The pending file is where a person catches that.
- **Stdout is the wire.** The host talks to the server over its stdin and stdout. Add `print("looking up", name)` inside `lookup_project`, run `client.py`, and read the error. Use `logging`, which writes to stderr.
- **Tests go through the protocol.** `Client(mcp)` connects to the server object in memory, so every test lists, validates, and calls exactly as a host would, with no subprocess and no model.

## When a server, when something smaller

These tools read a local JSON file and one public API. If one program is the only caller, a function call (Week 8) is enough, and if the only host is a coding agent with a shell, a skill that runs a script is enough. A server earns its place when the system is external and holds its own credentials, or when more than one host needs the same tools. Team Project 2 requires two hosts, which is why it requires a server.

Prof. Kousen's osquery project shows one capability offered three ways (an MCP server, a programmatic client, and a Claude Code skill): [repository](https://github.com/kousen/OsqueryMcpServer), [video](https://youtu.be/q8sXNXR6iKc).

## Costs (November 16, 2026)

The tests and `client.py` cost nothing. In Claude Code the question above took four turns and 11 to 12 seconds on each class model. `host.py` answered the same question in two chat calls: about 5 seconds on `minimax/minimax-m3`, and 25 seconds in one timed run on `xiaomi/mimo-v2.6-flash`. Check the cost on your OpenRouter activity page: the figure Claude Code prints is not priced for these models.
