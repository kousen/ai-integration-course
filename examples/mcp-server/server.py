"""Week 8's tools behind a new front door: an MCP server any MCP host can start and call.

    python3 client.py                  # no model: list the tools, call two of them
    python3 -m pytest tests -v         # no key, no network, no subprocess

Nothing about the tools is new. `recent_commits` and `lookup_project` are imported from
examples/tool-loop and run unchanged. What changed is who can call them: in Week 8 only loop.py
could; now Claude Code, Claude Desktop, an IDE, or your own loop can, without sharing any code.

Three things to notice:
  1. No hand-written schema. The SDK builds each tool's JSON Schema from the type hints, and the
     docstring is the description the model reads. Write it as an instruction, as in Week 8.
  2. The server holds the credential. GITHUB_TOKEN lives in this process's environment. The host
     and the model never see it.
  3. The server cannot see the user, so it cannot ask for confirmation. `request_intro` therefore
     never sends anything: it writes a pending request for a person to review. The host's
     permission prompt is a second gate, not the only one.
"""
import json
import logging
import pathlib
import re
import sys
from typing import Annotated, Any

from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from pydantic import Field

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "tool-loop"))   # the Week 8 functions, imported, not copied
import github_tool  # noqa: E402
import tools  # noqa: E402

PENDING = HERE / "pending.jsonl"
log = logging.getLogger("portfolio")     # logging goes to stderr; stdout belongs to the protocol

mcp = MCPServer("portfolio")


@mcp.tool()
def recent_commits(repo: Annotated[str, Field(description="owner/name, for example kousen/ai-integration-course")],
                   count: Annotated[int, Field(ge=1, le=10, description="How many commits")] = 5) -> dict[str, Any]:
    """The most recent commits in a public GitHub repository. Use this before saying anything
    about what someone has worked on lately."""
    log.info("recent_commits %s %s", repo, count)
    result = github_tool.recent_commits(repo, count)
    if "error" in result:
        raise ToolError(result["error"])      # goes back to the model as an error result, not a crash
    return result


@mcp.tool()
def lookup_project(name: Annotated[str, Field(description="The project's name, or part of it")]) -> dict[str, Any]:
    """Look up one of Sam Rivera's projects by name and return its four-question annotation
    (what, why, what breaks, what was learned). Use this before saying anything about a project."""
    return tools.lookup_project(name)


@mcp.tool()
def request_intro(email: Annotated[str, Field(description="The visitor's email address")],
                  message: Annotated[str, Field(max_length=500, description="What the visitor wants")]) -> dict[str, Any]:
    """Record a visitor's request to be introduced to Sam Rivera. Only when the visitor explicitly
    asks to be introduced and gives an email address. Nothing is sent: a person reviews it."""
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        raise ToolError(f"{email!r} is not an email address")
    with open(PENDING, "a", encoding="utf-8") as f:
        f.write(json.dumps({"email": email, "message": message}) + "\n")
    return {"sent": False, "pending": True, "note": "recorded for Sam to review; nothing was sent"}


@mcp.resource("profile://skills")
def skills() -> str:
    """The skills Sam has shipped work with, one per line. A resource is data the host attaches;
    a tool is something the model asks for."""
    return "\n".join(tools.PROFILE["skills_shipped"])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stderr)
    if "--http" in sys.argv:                   # python3 server.py --http: one running process,
        mcp.run(transport="streamable-http", port=8000)      # any host connects to localhost:8000/mcp
    else:
        mcp.run()                              # stdio: the host starts this file and talks over pipes
