"""The second host: Week 8's loop, with the tools discovered from the server instead of imported.

    export OPENROUTER_API_KEY=...
    python3 host.py "What did Sam learn from the receipt reader project?"
    python3 host.py "What are the two latest commits in kousen/ai-integration-course?" --model xiaomi/mimo-v2.6-flash
    python3 host.py "What is in the repo?" --server http://localhost:8000/mcp     # the same server, over HTTP
    MCP_TOKEN=... python3 host.py "..." --server https://your-host.example/mcp    # deployed (app.py): the token goes with every request

This file imports nothing from server.py or tools.py. It learns what the server offers by asking
it, hands those schemas to the model, and sends every tool request back through the protocol.
Point --server at a different MCP server and the loop works unchanged.

Compare with ../tool-loop/loop.py: the four messages and the step cap are the same. Three lines
differ: where the schemas come from (list_tools), who runs the tool (call_tool), and `await`,
because the server is another process and the SDK's client is asynchronous.
"""
import argparse
import asyncio
import json
import os
import sys

import httpx2
from mcp import Client, MCPError, StdioServerParameters
from mcp.client.streamable_http import streamable_http_client
from openrouter import OpenRouter

REASONING = {"xiaomi/mimo-v2.6-flash": {"enabled": False}}     # per-model, as in Week 8
SYSTEM = ("Answer only from what the tools return. If a tool reports an error or finds nothing, "
          "say so plainly and do not guess. Two or three plain sentences.")


def connect_to(url: str):
    """A deployed server should want a token. If MCP_TOKEN is set, send it with every request."""
    token = os.environ.get("MCP_TOKEN")
    if not token:
        return url
    return streamable_http_client(url, http_client=httpx2.AsyncClient(
        headers={"Authorization": f"Bearer {token}"}, timeout=30))


def refused(e: BaseException) -> bool:
    """True if the server answered with a protocol error, which is what a missing or wrong token
    looks like from here. Errors raised inside the client arrive wrapped in groups, so look through them."""
    inner = getattr(e, "exceptions", None)
    return any(refused(x) for x in inner) if inner else isinstance(e, MCPError)


async def run(question: str, model: str, server, max_steps: int = 4) -> str:
    llm = OpenRouter(api_key=os.environ["OPENROUTER_API_KEY"])
    async with Client(server) as mcp:
        # 1. discovery: the server's schemas become the `tools` of the chat request
        listed = (await mcp.list_tools()).tools
        tools = [{"type": "function", "function": {"name": t.name, "description": t.description,
                                                   "parameters": t.input_schema}} for t in listed]
        print(f"server offers: {[t.name for t in listed]}", file=sys.stderr)

        messages = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": question}]
        for step in range(1, max_steps + 1):
            kwargs = {"model": model, "messages": messages, "tools": tools, "max_tokens": 1500}
            if model in REASONING:
                kwargs["reasoning"] = REASONING[model]
            msg = llm.chat.send(**kwargs).choices[0].message
            if not msg.tool_calls:
                return (msg.content or "").strip()
            messages.append({"role": "assistant", "content": msg.content or "",
                             "tool_calls": [{"id": tc.id, "type": "function",
                                             "function": {"name": tc.function.name, "arguments": tc.function.arguments}}
                                            for tc in msg.tool_calls]})
            for tc in msg.tool_calls:
                # 2. the call goes to the server; it validates, runs or refuses, and answers
                try:
                    result = await mcp.call_tool(tc.function.name, json.loads(tc.function.arguments or "{}"))
                    text = result.content[0].text if result.content else ""
                    if result.is_error:
                        text = "ERROR: " + text
                except json.JSONDecodeError as e:
                    text = f"ERROR: arguments were not valid JSON: {e.msg}"
                print(f"step {step}  {tc.function.name}({tc.function.arguments})  ->  {text[:90]!r}", file=sys.stderr)
                messages.append({"role": "tool", "tool_call_id": tc.id, "content": text})
        return f"I couldn't finish answering that in {max_steps} steps."      # the program's sentence


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("question")
    p.add_argument("--model", default=os.environ.get("CHAT_MODEL", "minimax/minimax-m3"))
    p.add_argument("--server", default=None, help="URL of an HTTP MCP server (MCP_TOKEN, if set, is sent as a bearer token); default starts server.py over stdio")
    a = p.parse_args()
    target = connect_to(a.server) if a.server else StdioServerParameters(command=sys.executable, args=["server.py"])
    try:
        print(asyncio.run(run(a.question, a.model, target)))
    except Exception as e:
        if not (a.server and refused(e)):
            raise
        sys.exit(f"{a.server} answered with an error instead of a result. A deployed server does this when "
                 "MCP_TOKEN is missing or wrong: set it to the value the server was started with.")
