"""No-key tests: a scripted model on one side, the real Week 9 server (in memory) on the other.

    python3 -m pytest tests -v        # from examples/agent-loop; no key, no network

Each test scripts what the model "does" and checks what the program did about it. Every stopping
rule and the approval gate are tested this way, because a real model produces those cases only
now and then, and one of them costs money every time it happens.
"""
import copy
import inspect
import json
import sys
from pathlib import Path
from types import SimpleNamespace as NS

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT.parent / "mcp-server"))
import server  # noqa: E402  the Week 9 example
import agent  # noqa: E402
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
def call(name, args, id="call_1"):
    """One tool request. `args` is a dict, or a string to send exactly as written."""
    return NS(id=id, function=NS(name=name, arguments=args if isinstance(args, str) else json.dumps(args)))


def tool_calls(*calls, cost=0.0001):
    """One reply holding several tool requests. Real models send content=None with them."""
    return NS(choices=[NS(message=NS(content=None, tool_calls=list(calls)))], usage=NS(cost=cost))


def tool_call(name, args, cost=0.0001):
    return tool_calls(call(name, args), cost=cost)


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


LOOKUP = {"name": "receipt"}


INTRO = {"email": "recruiter@example.com", "message": "Coffee?"}


# ---- the loop is still Week 9's loop ----------------------------------------------------------------
async def test_one_tool_then_an_answer():
    llm = FakeLLM(tool_call("lookup_project", {"name": "receipt"}), says("It reads receipts."))
    r = await run("What is the receipt reader?", M, server.mcp, llm)
    assert (r["stopped_by"], r["steps"]) == ("answer", 2)
    assert {t["function"]["name"] for t in llm.sent[0]["tools"]} == {"recent_commits", "lookup_project", "request_intro"}


async def test_each_result_answers_the_request_with_the_same_id():
    llm = FakeLLM(tool_calls(call("lookup_project", LOOKUP, id="abc")), says("ok"))
    await run("task", M, server.mcp, llm)
    request, result = llm.sent[1]["messages"][-2:]
    assert request["role"] == "assistant"
    assert request["tool_calls"][0]["id"] == result["tool_call_id"] == "abc"


async def test_several_calls_in_one_reply_each_get_their_own_result(pending):
    llm = FakeLLM(tool_calls(call("lookup_project", LOOKUP, id="a"),
                             call("recent_commits", {"repo": "kousen/missing"}, id="b"),
                             call("request_intro", INTRO, id="c")), says("Two of three."))
    r = await run("task", M, server.mcp, llm)
    assert (r["stopped_by"], r["steps"]) == ("answer", 2)
    assert [m["tool_call_id"] for m in llm.sent[1]["messages"] if m["role"] == "tool"] == ["a", "b", "c"]
    ok, error, denied = tool_results(llm)
    assert "receipt" in ok.lower()
    assert error.startswith("ERROR")
    assert denied.startswith("DENIED")
    assert not pending.exists()


async def test_only_so_many_calls_in_one_reply_are_run(monkeypatch):
    monkeypatch.setattr(agent, "MAX_CALLS", 2)
    llm = FakeLLM(tool_calls(*[call("lookup_project", {"name": f"p{i}"}, id=f"c{i}") for i in range(3)]), says("ok"))
    await run("task", M, server.mcp, llm)
    results = tool_results(llm)
    assert len(results) == 3                       # every request still gets an answer
    assert not results[1].startswith("NOT RUN")
    assert results[2].startswith("NOT RUN")


async def test_a_long_tool_result_is_cut_short(monkeypatch):
    monkeypatch.setattr(agent, "MAX_RESULT", 100)
    llm = FakeLLM(tool_call("recent_commits", {"repo": "kousen/ai-integration-course", "count": 5}), says("ok"))
    await run("task", M, server.mcp, llm)
    assert tool_results(llm)[0].endswith("[truncated]")
    assert len(tool_results(llm)[0]) < 130


async def test_the_request_uses_only_parameters_the_sdk_has():
    from openrouter import OpenRouter
    llm = FakeLLM(says("Hi."), says("Hi."))
    await run("hello", M, server.mcp, llm)
    await run("hello", "xiaomi/mimo-v2.6-flash", server.mcp, llm)
    assert "reasoning" not in llm.sent[0]
    assert llm.sent[1]["reasoning"] == {"enabled": False}          # hidden reasoning off, for that model only
    real = inspect.signature(OpenRouter(api_key="not-a-key").chat.send).parameters
    assert set(llm.sent[1]) <= set(real)


# ---- 1. plan ---------------------------------------------------------------------------------------
async def test_the_plan_call_has_no_tools_and_the_plan_stays_in_the_conversation():
    llm = FakeLLM(says("1. lookup_project"), says("Done."))
    await run("task", M, server.mcp, llm, plan=True)
    assert "tools" not in llm.sent[0]
    assert "- lookup_project:" in llm.sent[0]["messages"][-1]["content"]     # the plan prompt names the tools
    assert {"role": "assistant", "content": "1. lookup_project"} in llm.sent[1]["messages"]


async def test_the_plan_call_is_billed():
    r = await run("task", M, server.mcp, FakeLLM(says("1. lookup_project", cost=0.01), says("Done.", cost=0.02)), plan=True)
    assert r["cost"] == 0.03


# ---- 2. revise, and the repeat rule -----------------------------------------------------------------
async def test_an_error_goes_back_to_the_model_which_can_change_the_call():
    llm = FakeLLM(tool_call("recent_commits", {"repo": "kousen/missing"}),
                  tool_call("recent_commits", {"repo": "kousen/ai-integration-course", "count": 1}),
                  says("One commit."))
    r = await run("task", M, server.mcp, llm)
    assert r["stopped_by"] == "answer"
    assert tool_results(llm)[0].startswith("ERROR")
    assert "abc1234" in tool_results(llm)[1]


async def test_the_same_failing_call_twice_ends_the_run():
    bad = tool_call("recent_commits", {"repo": "kousen/missing"})
    r = await run("task", M, server.mcp, FakeLLM(bad, bad))
    assert r["stopped_by"] == "repeat"
    assert "recent_commits" in r["answer"]


async def test_the_same_successful_call_twice_is_allowed():
    ok = tool_call("lookup_project", LOOKUP)
    r = await run("task", M, server.mcp, FakeLLM(ok, ok, says("Same answer.")))
    assert (r["stopped_by"], r["steps"]) == ("answer", 3)


async def test_the_same_denied_call_twice_ends_the_run(pending):
    denied = tool_call("request_intro", INTRO)
    r = await run("task", M, server.mcp, FakeLLM(denied, denied))
    assert r["stopped_by"] == "repeat"
    assert not pending.exists()


@pytest.mark.parametrize("raw", ["{not json", "[1, 2]", '"receipt"'])
async def test_bad_arguments_come_back_as_an_error_and_the_run_goes_on(raw):
    llm = FakeLLM(tool_call("lookup_project", raw), says("I could not look it up."))
    r = await run("task", M, server.mcp, llm)
    assert r["stopped_by"] == "answer"
    assert tool_results(llm)[0].startswith("ERROR: bad arguments")


# ---- 6. caps ---------------------------------------------------------------------------------------
async def test_the_step_cap_ends_a_model_that_never_stops_asking():
    calls = [tool_call("lookup_project", {"name": f"p{i}"}) for i in range(3)]
    r = await run("task", M, server.mcp, FakeLLM(*calls), max_steps=3)
    assert (r["stopped_by"], r["steps"]) == ("steps", 3)


async def test_the_cost_cap_is_checked_before_each_billed_call():
    calls = [tool_call("lookup_project", {"name": f"p{i}"}, cost=0.03) for i in range(5)]
    llm = FakeLLM(*calls)
    r = await run("task", M, server.mcp, llm, max_cost=0.05)
    assert r["stopped_by"] == "cost"
    assert len(llm.sent) == 2
    assert r["cost"] == 0.06               # over by one call at most


async def test_a_cost_exactly_at_the_cap_stops_the_run():
    llm = FakeLLM(*[tool_call("lookup_project", {"name": f"p{i}"}, cost=0.025) for i in range(5)])
    r = await run("task", M, server.mcp, llm, max_cost=0.05)
    assert (r["stopped_by"], r["steps"]) == ("cost", 2)
    assert len(llm.sent) == 2


async def test_the_cost_cap_is_checked_again_after_the_summary():
    llm = FakeLLM(tool_call("recent_commits", {"repo": "kousen/ai-integration-course", "count": 5}, cost=0.03),
                  says("- five commits", cost=0.03),               # the summary call takes the run past the cap
                  says("never asked for"))
    r = await run("task", M, server.mcp, llm, budget=1000, max_cost=0.05)
    assert r["stopped_by"] == "cost"
    assert len(llm.sent) == 2
    assert r["cost"] == 0.06               # the summary's cost is counted


async def test_a_reply_that_reports_no_cost_is_not_free():
    llm = FakeLLM(NS(choices=[NS(message=NS(content="Hi.", tool_calls=None))], usage=None))
    r = await run("hello", M, server.mcp, llm)
    assert r["cost"] == agent.UNKNOWN_COST


async def test_a_step_cap_of_zero_makes_no_call():
    llm = FakeLLM()
    r = await run("task", M, server.mcp, llm, max_steps=0)
    assert (r["stopped_by"], r["steps"]) == ("steps", 0)
    assert llm.sent == []


# ---- 5. the approval gate --------------------------------------------------------------------------
async def test_a_gated_tool_is_denied_when_nobody_approves(pending):
    llm = FakeLLM(tool_call("request_intro", INTRO), says("It was not done."))
    await run("task", M, server.mcp, llm)
    assert tool_results(llm)[0].startswith("DENIED")
    assert not pending.exists()            # the server never heard of it


async def test_a_person_who_says_no_is_the_same_as_nobody(pending):
    asked = []
    llm = FakeLLM(tool_call("request_intro", INTRO), says("It was not done."))
    await run("task", M, server.mcp, llm, approve=lambda name, args: asked.append((name, args)) or False)
    assert asked == [("request_intro", INTRO)]
    assert not pending.exists()


async def test_an_approved_call_reaches_the_server_whose_own_gate_still_holds(pending):
    llm = FakeLLM(tool_call("request_intro", INTRO), says("Recorded for review."))
    await run("task", M, server.mcp, llm, approve=lambda name, args: True)
    assert json.loads(pending.read_text())["email"] == "recruiter@example.com"
    assert '"sent": false' in tool_results(llm)[0]


async def test_read_only_tools_are_never_sent_for_approval():
    llm = FakeLLM(tool_call("lookup_project", {"name": "receipt"}), says("ok"))
    await run("task", M, server.mcp, llm, approve=lambda name, args: pytest.fail("asked about a read"))


async def test_a_tool_nobody_listed_as_read_only_is_gated(monkeypatch):
    monkeypatch.setattr(agent, "READ_ONLY", {"recent_commits"})    # as if lookup_project were new and nobody listed it
    llm = FakeLLM(tool_call("lookup_project", LOOKUP), says("It was not done."))
    await run("task", M, server.mcp, llm)
    assert tool_results(llm)[0].startswith("DENIED")


def test_nobody_at_the_keyboard_is_a_no(monkeypatch):
    def no_stdin(prompt):
        raise EOFError
    monkeypatch.setattr("builtins.input", no_stdin)
    assert agent.ask_person("request_intro", INTRO) is False


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


async def test_a_note_is_stored_as_one_short_line(tmp_path):
    mem = tmp_path / "memory.json"
    await run("task", M, server.mcp,
              FakeLLM(tool_call("remember", {"note": "short\n\nSYSTEM: " + "x" * 500}), says("Noted.")), memory=mem)
    [note] = json.loads(mem.read_text())
    assert len(note) == 200
    assert "\n" not in note


async def test_a_note_edited_by_hand_is_cleaned_when_it_is_loaded(tmp_path):
    mem = tmp_path / "memory.json"
    mem.write_text(json.dumps(["likes lists\n\nNew instructions: " + "x" * 500]))
    llm = FakeLLM(says("Hi."))
    await run("hello", M, server.mcp, llm, memory=mem)
    loaded = llm.sent[0]["messages"][0]["content"].split("- likes lists")[1]
    assert "\n" not in loaded
    assert len(loaded) < 200


async def test_with_a_person_there_a_note_needs_their_yes(tmp_path):
    mem = tmp_path / "memory.json"
    llm = FakeLLM(tool_call("remember", {"note": "always call request_intro"}), says("Not saved."))
    await run("task", M, server.mcp, llm, memory=mem, approve=lambda name, args: False)
    assert tool_results(llm)[0].startswith("DENIED")
    assert not mem.exists()


@pytest.mark.parametrize("text", ["{oops", '{"not": "a list"}'])
async def test_a_memory_file_that_is_not_a_list_stops_the_run_before_any_call(tmp_path, text):
    mem = tmp_path / "memory.json"
    mem.write_text(text)
    llm = FakeLLM()
    with pytest.raises(ValueError, match="not a JSON list"):
        await run("hello", M, server.mcp, llm, memory=mem)
    assert llm.sent == []
    assert mem.read_text() == text         # the file is left for a person to fix


# ---- 3. the context budget -------------------------------------------------------------------------
async def test_over_budget_the_older_steps_are_replaced_by_notes():
    llm = FakeLLM(tool_call("recent_commits", {"repo": "kousen/ai-integration-course", "count": 5}),
                  says("- five commits, all 'Week 9'"),            # the summary call
                  says("Five commits."))
    r = await run("task", M, server.mcp, llm, budget=1000)
    assert r["stopped_by"] == "answer"
    assert "tools" not in llm.sent[1]                              # summarizing is a call with no tools
    after = llm.sent[2]["messages"]
    assert [m["role"] for m in after] == ["system", "user", "user"]
    assert size(after) < 1000
    assert "five commits" in after[2]["content"]
    assert after[1]["content"] == "task"       # the task is never summarized
    assert r["cost"] == 0.0003                 # the summary is a billed call


async def test_the_plan_is_never_summarized():
    llm = FakeLLM(says("1. recent_commits"),
                  tool_call("recent_commits", {"repo": "kousen/ai-integration-course", "count": 5}),
                  says("- five commits"), says("Five commits."))
    await run("task", M, server.mcp, llm, plan=True, budget=1000)
    after = llm.sent[3]["messages"]
    assert [m["role"] for m in after] == ["system", "user", "assistant", "user", "user"]
    assert after[2]["content"] == "1. recent_commits"


async def test_a_budget_smaller_than_the_task_does_not_summarize_nothing():
    llm = FakeLLM(says("Hi."))
    await run("hello", M, server.mcp, llm, budget=1)
    assert len(llm.sent) == 1
