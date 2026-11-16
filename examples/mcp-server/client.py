"""A host with no model in it: start the server, ask what it offers, call two tools.

    python3 client.py

This is everything an MCP host does before a model is involved: launch the server as a child
process, discover its tools and their schemas, and call one by name with JSON arguments.
Claude Code does the same thing, then hands the schemas to the model.
"""
import asyncio
import json
import sys

from mcp import Client, StdioServerParameters


async def main():
    server = StdioServerParameters(command=sys.executable, args=["server.py"])
    async with Client(server) as client:
        listed = await client.list_tools()
        for t in listed.tools:
            print(f"\n{t.name}: {t.description}")
            print("  schema:", json.dumps(t.input_schema.get("properties", {})))

        print("\n--- lookup_project('receipt')")
        result = await client.call_tool("lookup_project", {"name": "receipt"})
        print(json.dumps(result.structured_content, indent=1)[:400])

        print("\n--- recent_commits with count=50 (the schema says 1 to 10)")
        result = await client.call_tool("recent_commits", {"repo": "kousen/ai-integration-course", "count": 50})
        print("is_error:", result.is_error, "|", result.content[0].text[:200])


if __name__ == "__main__":
    asyncio.run(main())
