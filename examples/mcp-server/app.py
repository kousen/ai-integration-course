"""The same server as a web service you can deploy: a URL in place of a child process.

    export MCP_TOKEN=...        # any long random string; the hosts send the same one
    python3 app.py              # listens on $PORT if the platform sets it, otherwise 8000

server.py is unchanged. Three things differ from `python3 server.py --http`:
  1. The platform chooses the port and the address is public, so listen on 0.0.0.0 and $PORT.
  2. Anyone who finds the URL can call it, so every request must carry a bearer token.
     Without MCP_TOKEN this file refuses to start: an open server is not a default.
  3. The transport is stateless. A platform may restart the process, put it to sleep, or run
     a new copy for each request, so nothing about a conversation is kept in memory.

What it does not fix: request_intro writes pending.jsonl next to this file. Where the disk is
replaced on every deploy, or is read-only, that record needs a database or key-value store.
"""
import hmac
import os

from server import mcp

TOKEN = os.environ["MCP_TOKEN"].encode()


class BearerToken:
    """Refuse any request whose Authorization header is not `Bearer <MCP_TOKEN>`."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            sent = dict(scope["headers"]).get(b"authorization", b"")
            if not hmac.compare_digest(sent, b"Bearer " + TOKEN):       # constant time: no hint about how close a guess was
                await send({"type": "http.response.start", "status": 401,
                            "headers": [(b"content-type", b"text/plain"), (b"www-authenticate", b"Bearer")]})
                await send({"type": "http.response.body", "body": b"missing or wrong bearer token\n"})
                return
        await self.app(scope, receive, send)


# host="0.0.0.0": with the default, 127.0.0.1, the SDK rejects requests addressed to a public hostname.
app = mcp.streamable_http_app(stateless_http=True, json_response=True, host="0.0.0.0")
app.add_middleware(BearerToken)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
