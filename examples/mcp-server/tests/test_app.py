"""The deployable app: the token gate, and the same tools behind it. No key, no network.

    python3 -m pytest tests -v        # from examples/mcp-server
"""
import sys
from pathlib import Path

import pytest
from starlette.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

LIST = {"jsonrpc": "2.0", "id": 1, "method": "tools/list"}
ACCEPT = {"accept": "application/json, text/event-stream"}


@pytest.fixture(scope="module")
def web():
    mp = pytest.MonkeyPatch()
    mp.setenv("MCP_TOKEN", "test-token")
    sys.modules.pop("app", None)
    import app
    with TestClient(app.app) as client:        # the `with` runs startup and shutdown, as a real server does
        yield client
    mp.undo()


def test_no_token_is_refused(web):
    r = web.post("/mcp", json=LIST, headers=ACCEPT)
    assert r.status_code == 401 and "bearer" in r.text


def test_wrong_token_is_refused(web):
    r = web.post("/mcp", json=LIST, headers={**ACCEPT, "authorization": "Bearer test-toke"})
    assert r.status_code == 401


def test_right_token_lists_the_tools(web):
    r = web.post("/mcp", json=LIST, headers={**ACCEPT, "authorization": "Bearer test-token"})
    assert r.status_code == 200
    assert {t["name"] for t in r.json()["result"]["tools"]} == {"recent_commits", "lookup_project", "request_intro"}


def test_two_requests_in_a_row(web):
    """Stateless: the second request needs nothing the first one left behind."""
    for _ in range(2):
        r = web.post("/mcp", json=LIST, headers={**ACCEPT, "authorization": "Bearer test-token"})
        assert r.status_code == 200


def test_a_public_hostname_is_accepted(web):
    r = web.post("/mcp", json=LIST, headers={**ACCEPT, "authorization": "Bearer test-token",
                                             "host": "portfolio.example.com"})
    assert r.status_code == 200


def test_it_will_not_start_without_a_token(monkeypatch):
    monkeypatch.delenv("MCP_TOKEN", raising=False)
    saved = sys.modules.pop("app", None)
    try:
        with pytest.raises(KeyError):
            import app  # noqa: F401
    finally:
        sys.modules.pop("app", None)
        if saved:
            sys.modules["app"] = saved
