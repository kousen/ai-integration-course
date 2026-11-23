"""No-key tests: a scripted model on one side, the real Week 9 server (in memory) on the other.

    python3 -m pytest tests -v        # from examples/agent-loop; no key, no network

Each test scripts what the model "does" and checks what the program did about it. Every stopping
rule and the approval gate are tested this way, because a real model produces those cases only
now and then, and one of them costs money every time it happens.
"""
import copy
import json
import sys
from pathlib import Path
from types import SimpleNamespace as NS

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT.parent / "mcp-server"))
import server  # noqa: E402  the Week 9 example
from agent import run, size  # noqa: E402

pytestmark = pytest.mark.anyio
M = "test-model"


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture(autouse=True)
def pending(tmp_path, monkeypatch):
    """The server's side effect goes to a temp file, and GitHub is never called."""
    path = tmp_path / "pending.jsonl"
    monkeypatch.setattr(server, "PENDING", path)
    monkeypatch.setattr(server.github_tool, "recent_commits", lambda repo, count=5: (
        {"error": f"{repo} not found"} if "missing" in repo
        else {"repo": repo, "commits": [{"sha": "abc1234", "message": "Week 9 " + "x" * 300}] * count}))
    return path


# ---- a scripted model, as in Week 8 ---------------------------------------------------------------
def tool_call(name, args, cost=0.0001):
    tc = NS(id="call_1", function=NS(name=name, arguments=json.dumps(args)))
    return NS(choices=[NS(message=NS(content="", tool_calls=[tc]))], usage=NS(cost=cost))


def says(text, cost=0.0001):
    return NS(choices=[NS(message=NS(content=text, tool_calls=None))], usage=NS(cost=cost))


class FakeLLM:
    def __init__(self, *replies):
        self.replies, self.sent = list(replies), []     # sent: the kwargs of every call the agent made

    @property
    def chat(self):
        return self

    def send(self, **kwargs):
        self.sent.append(copy.deepcopy(kwargs))
        assert self.replies, "the agent asked the model again after the script ran out"
        return self.replies.pop(0)


def tool_results(llm):
    """Every tool result the model was shown, in order."""
    return [m["content"] for m in llm.sent[-1]["messages"] if m["role"] == "tool"]


INTRO = {"email": "recruiter@example.com", "message": "Coffee?"}


# ---- the loop is still Week 9's loop ----------------------------------------------------------------
async def test_one_tool_then_an_answer():
    llm = FakeLLM(tool_call("lookup_project", {"name": "receipt"}), says("It reads receipts."))
    r = await run("What is the receipt reader?", M, server.mcp, llm)
    assert (r["stopped_by"], r["steps"]) == ("answer", 2)
    assert {t["function"]["name"] for t in llm.sent[0]["tools"]} == {"recent_commits", "lookup_project", "request_intro"}


# ---- 1. plan ---------------------------------------------------------------------------------------
async def test_the_plan_call_has_no_tools_and_the_plan_stays_in_the_conversation():
    llm = FakeLLM(says("1. lookup_project"), says("Done."))
    await run("task", M, server.mcp, llm, plan=True)
    assert "tools" not in llm.sent[0]
    assert "- lookup_project:" in llm.sent[0]["messages"][-1]["content"]     # the plan prompt names the tools
    assert {"role": "assistant", "content": "1. lookup_project"} in llm.sent[1]["messages"]


# ---- 2. revise, and the repeat rule -----------------------------------------------------------------
async def test_an_error_goes_back_to_the_model_which_can_change_the_call():
    llm = FakeLLM(tool_call("recent_commits", {"repo": "kousen/missing"}),
                  tool_call("recent_commits", {"repo": "kousen/ai-integration-course", "count": 1}),
                  says("One commit."))
    r = await run("task", M, server.mcp, llm)
    assert r["stopped_by"] == "answer"
    assert tool_results(llm)[0].startswith("ERROR") and "abc1234" in tool_results(llm)[1]


async def test_the_same_failing_call_twice_ends_the_run():
    bad = tool_call("recent_commits", {"repo": "kousen/missing"})
    r = await run("task", M, server.mcp, FakeLLM(bad, bad))
    assert r["stopped_by"] == "repeat" and "recent_commits" in r["answer"]


# ---- 6. caps ---------------------------------------------------------------------------------------
async def test_the_step_cap_ends_a_model_that_never_stops_asking():
    calls = [tool_call("lookup_project", {"name": f"p{i}"}) for i in range(3)]
    r = await run("task", M, server.mcp, FakeLLM(*calls), max_steps=3)
    assert (r["stopped_by"], r["steps"]) == ("steps", 3)


async def test_the_cost_cap_is_checked_before_each_billed_call():
    calls = [tool_call("lookup_project", {"name": f"p{i}"}, cost=0.03) for i in range(5)]
    llm = FakeLLM(*calls)
    r = await run("task", M, server.mcp, llm, max_cost=0.05)
    assert r["stopped_by"] == "cost" and len(llm.sent) == 2 and r["cost"] == 0.06     # over by one call at most


# ---- 5. the approval gate --------------------------------------------------------------------------
async def test_a_gated_tool_is_denied_when_nobody_approves(pending):
    llm = FakeLLM(tool_call("request_intro", INTRO), says("It was not done."))
    await run("task", M, server.mcp, llm)
    assert tool_results(llm)[0].startswith("DENIED") and not pending.exists()      # the server never heard of it


async def test_a_person_who_says_no_is_the_same_as_nobody(pending):
    asked = []
    llm = FakeLLM(tool_call("request_intro", INTRO), says("It was not done."))
    await run("task", M, server.mcp, llm, approve=lambda name, args: asked.append((name, args)) or False)
    assert asked == [("request_intro", INTRO)] and not pending.exists()


async def test_an_approved_call_reaches_the_server_whose_own_gate_still_holds(pending):
    llm = FakeLLM(tool_call("request_intro", INTRO), says("Recorded for review."))
    await run("task", M, server.mcp, llm, approve=lambda name, args: True)
    assert json.loads(pending.read_text())["email"] == "recruiter@example.com"
    assert '"sent": false' in tool_results(llm)[0]


async def test_read_only_tools_are_never_sent_for_approval():
    llm = FakeLLM(tool_call("lookup_project", {"name": "receipt"}), says("ok"))
    await run("task", M, server.mcp, llm, approve=lambda name, args: pytest.fail("asked about a read"))


# ---- 4. memory -------------------------------------------------------------------------------------
async def test_a_note_saved_in_one_run_is_in_the_next_runs_system_prompt(tmp_path):
    mem = tmp_path / "memory.json"
    await run("Remember I like short answers.", M, server.mcp,
              FakeLLM(tool_call("remember", {"note": "prefers short answers"}), says("Noted.")), memory=mem)
    llm = FakeLLM(says("Hi."))
    await run("hello", M, server.mcp, llm, memory=mem)
    assert "- prefers short answers" in llm.sent[0]["messages"][0]["content"]


async def test_without_memory_the_remember_tool_is_not_offered():
    llm = FakeLLM(says("Hi."))
    await run("hello", M, server.mcp, llm)
    assert "remember" not in [t["function"]["name"] for t in llm.sent[0]["tools"]]


# ---- 3. the context budget -------------------------------------------------------------------------
async def test_over_budget_the_older_steps_are_replaced_by_notes():
    llm = FakeLLM(tool_call("recent_commits", {"repo": "kousen/ai-integration-course", "count": 5}),
                  says("- five commits, all 'Week 9'"),            # the summary call
                  says("Five commits."))
    r = await run("task", M, server.mcp, llm, budget=1000)
    assert r["stopped_by"] == "answer"
    assert "tools" not in llm.sent[1]                              # summarizing is a call with no tools
    after = llm.sent[2]["messages"]
    assert [m["role"] for m in after] == ["system", "user", "user"] and size(after) < 1000
    assert "five commits" in after[2]["content"] and after[1]["content"] == "task"   # the task is never summarized
