"""The second host: Week 8's loop, with the tools discovered from the server instead of imported.

    export OPENROUTER_API_KEY=...
    python3 host.py "What did Sam learn from the receipt reader project?"
    python3 host.py "What are the two latest commits in kousen/ai-integration-course?" --model xiaomi/mimo-v2.6-flash
    python3 host.py "What is in the repo?" --server http://localhost:8000/mcp     # the same server, over HTTP

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

from mcp import Client, StdioServerParameters
from openrouter import OpenRouter

REASONING = {"xiaomi/mimo-v2.6-flash": {"enabled": False}}     # per-model, as in Week 8
SYSTEM = ("Answer only from what the tools return. If a tool reports an error or finds nothing, "
          "say so plainly and do not guess. Two or three plain sentences.")


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
    p.add_argument("--server", default=None, help="URL of an HTTP MCP server; default starts server.py over stdio")
    a = p.parse_args()
    target = a.server or StdioServerParameters(command=sys.executable, args=["server.py"])
    print(asyncio.run(run(a.question, a.model, target)))
