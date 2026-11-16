"""No-key tests through the real protocol, in memory: no subprocess, no network, no model.

    python3 -m pytest tests -v        # from examples/mcp-server

`Client(mcp)` connects to the server object directly, so each call is listed, validated, and
invoked exactly as a host would do it. The misuse cases are the point: a host you did not write
will send arguments you did not expect.
"""
import json
import sys
from pathlib import Path

import pytest
from mcp import Client

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import server
from server import mcp

pytestmark = pytest.mark.anyio


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture(autouse=True)
def pending(tmp_path, monkeypatch):
    path = tmp_path / "pending.jsonl"
    monkeypatch.setattr(server, "PENDING", path)
    return path


async def call(name, args):
    """Call a tool; a rejected call may come back as an error result or be raised by the client."""
    async with Client(mcp) as client:
        return await client.call_tool(name, args)


async def test_the_three_tools_are_discoverable_with_schemas():
    async with Client(mcp) as client:
        listed = {t.name: t for t in (await client.list_tools()).tools}
    assert set(listed) == {"recent_commits", "lookup_project", "request_intro"}
    count = listed["recent_commits"].input_schema["properties"]["count"]
    assert (count["minimum"], count["maximum"]) == (1, 10)       # built from the type hints
    assert "before saying anything" in listed["lookup_project"].description


async def test_lookup_project_runs_the_week8_function():
    result = await call("lookup_project", {"name": "receipt"})
    assert result.structured_content["found"] is True


async def test_unknown_project_is_a_result_not_an_error():
    result = await call("lookup_project", {"name": "blockchain voting"})
    assert not result.is_error and result.structured_content["found"] is False


async def test_wrong_type_is_rejected_before_the_function_runs():
    result = await call("lookup_project", {"name": 42})
    assert result.is_error


async def test_count_out_of_range_is_rejected_without_calling_github():
    result = await call("recent_commits", {"repo": "kousen/ai-integration-course", "count": 50})
    assert result.is_error


async def test_bad_repo_name_is_an_error_result_without_calling_github():
    result = await call("recent_commits", {"repo": "not a repo"})
    assert result.is_error and "owner/name" in result.content[0].text


async def test_request_intro_records_and_never_sends(pending):
    result = await call("request_intro", {"email": "recruiter@example.com", "message": "Coffee?"})
    assert result.structured_content["sent"] is False
    assert json.loads(pending.read_text())["email"] == "recruiter@example.com"


async def test_request_intro_refuses_a_bad_email_and_writes_nothing(pending):
    result = await call("request_intro", {"email": "not-an-email", "message": "hi"})
    assert result.is_error and not pending.exists()


async def test_the_resource_lists_shipped_skills():
    async with Client(mcp) as client:
        listed = await client.list_resources()
    assert [str(r.uri) for r in listed.resources] == ["profile://skills"]
