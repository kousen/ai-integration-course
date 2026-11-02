"""No-key tests: the tools, the decision, and the loop, with a scripted fake model.

    python3 -m pytest tests/test_loop.py -v      # from examples/tool-loop; well under a second

The fake client returns whatever replies the test scripted, in order, so each test says exactly
what the model "did" and checks what the program did about it. That is how you test a loop
without paying for it, and how you test the cases a real model only produces now and then.
"""
import copy
import json
import sys
from pathlib import Path
from types import SimpleNamespace as NS

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import tools
from loop import check_answer, run
from tools import check_skill, lookup_project, run_tool


# ---- a scripted model ---------------------------------------------------------------------------
def tool_call(name, arguments, call_id="call_1"):
    """One reply in which the model asks for a tool. `arguments` is the JSON string the model wrote."""
    tc = NS(id=call_id, function=NS(name=name, arguments=arguments))
    return NS(choices=[NS(message=NS(content="", tool_calls=[tc]), finish_reason="tool_calls")],
              usage=NS(cost=0.0001))


def answer(text):
    return NS(choices=[NS(message=NS(content=text, tool_calls=None), finish_reason="stop")],
              usage=NS(cost=0.0001))


class FakeClient:
    def __init__(self, replies):
        self.replies = list(replies)
        self.sent = []                                   # every messages list the loop sent

    @property
    def chat(self):
        return self

    def send(self, **kwargs):
        self.sent.append(copy.deepcopy(kwargs["messages"]))   # the loop mutates its list
        if not self.replies:
            raise AssertionError("the loop asked the model again after the script ran out")
        return self.replies.pop(0)


# ---- the tools themselves ------------------------------------------------------------------------
def test_lookup_finds_by_partial_name_any_case():
    assert lookup_project("receipt READER")["found"]
    assert lookup_project("Ask the course")["project"]["name"].startswith("Ask the course")


def test_lookup_not_found_lists_what_exists():
    r = lookup_project("blockchain voting")
    assert r["found"] is False and "Receipt reader" in r["projects_on_record"]


def test_check_skill_three_outcomes():
    assert check_skill("python")["status"] == "shipped"
    assert check_skill("Kubernetes")["status"] == "not_yet"
    assert check_skill("COBOL")["status"] == "no_record"


# ---- the decision: bad calls come back as errors, never as exceptions ---------------------------
def test_unknown_tool_is_an_error_result():
    r = run_tool("delete_profile", "{}")
    assert "unknown tool" in r["error"]


def test_missing_argument_is_an_error_result():
    assert "missing required argument 'name'" in run_tool("lookup_project", "{}")["error"]


def test_wrong_type_is_an_error_result():
    assert "must be a string" in run_tool("lookup_project", '{"name": 42}')["error"]


def test_invalid_json_arguments_is_an_error_result():
    assert "not valid JSON" in run_tool("lookup_project", '{"name": "Receipt')["error"]


def test_side_effect_tool_is_not_run_without_permission(tmp_path, monkeypatch):
    monkeypatch.setattr(tools, "HERE", tmp_path)        # the outbox would be written here
    r = run_tool("request_intro", '{"email": "a@b.c", "message": "hi"}')
    assert r["pending"]["tool"] == "request_intro" and "confirmation" in r["error"]
    assert not (tmp_path / "outbox.jsonl").exists()
    r = run_tool("request_intro", '{"email": "a@b.c", "message": "hi"}', allow_side_effects=True)
    assert r == {"sent": True} and (tmp_path / "outbox.jsonl").exists()


# ---- the loop ------------------------------------------------------------------------------------
def test_single_shot_tool_call_then_answer():
    fake = FakeClient([tool_call("lookup_project", '{"name": "Receipt reader"}'),
                       answer("Sam built a receipt reader and learned that edge cases are spec questions.")])
    r = run("What did Sam learn from the receipt reader?", client=fake)
    assert r["stopped_by"] == "answer" and r["calls"] == ["lookup_project"]
    second = fake.sent[1]                                # what the model saw on its second turn
    assert second[-2]["role"] == "assistant" and second[-2]["tool_calls"][0]["id"] == "call_1"
    assert second[-1]["role"] == "tool" and json.loads(second[-1]["content"])["found"] is True
    assert r["check"]["supported"]
    assert abs(r["cost"] - 0.0002) < 1e-9


def test_no_tool_needed_is_one_call():
    fake = FakeClient([answer("Hello! Ask me about Sam's projects or skills.")])
    r = run("Hi", client=fake)
    assert r["calls"] == [] and len(fake.sent) == 1


def test_endless_caller_stops_at_the_cap():
    fake = FakeClient([tool_call("check_skill", '{"skill": "Python"}', f"c{i}") for i in range(10)])
    r = run("Does Sam know Python?", client=fake, max_steps=3)
    assert r["stopped_by"] == "cap" and len(r["calls"]) == 3 and len(fake.sent) == 3
    assert "3 steps" in r["answer"]                      # the program's answer, not the model's


def test_bad_call_goes_back_to_the_model_as_an_error():
    fake = FakeClient([tool_call("lookup_project", '{"title": "Receipt reader"}'),
                       tool_call("lookup_project", '{"name": "Receipt reader"}', "call_2"),
                       answer("Sam built a receipt reader.")])
    r = run("Receipt reader?", client=fake)
    first_result = json.loads(fake.sent[1][-1]["content"])
    assert "missing required argument 'name'" in first_result["error"]
    assert r["stopped_by"] == "answer" and r["check"]["supported"]


def test_hallucinated_tool_name_goes_back_as_an_error():
    fake = FakeClient([tool_call("get_resume", "{}"), answer("I can't retrieve that.")])
    run("Send me the resume", client=fake)
    assert "unknown tool" in json.loads(fake.sent[1][-1]["content"])["error"]


def test_parallel_tool_calls_each_get_a_result():
    tc1 = NS(id="a", function=NS(name="check_skill", arguments='{"skill": "Python"}'))
    tc2 = NS(id="b", function=NS(name="check_skill", arguments='{"skill": "Rust"}'))
    both = NS(choices=[NS(message=NS(content="", tool_calls=[tc1, tc2]), finish_reason="tool_calls")],
              usage=NS(cost=0.0))
    fake = FakeClient([both, answer("Python yes, Rust not yet.")])
    r = run("Python and Rust?", client=fake)
    tool_msgs = [m for m in fake.sent[1] if m["role"] == "tool"]
    assert [m["tool_call_id"] for m in tool_msgs] == ["a", "b"] and r["calls"] == ["check_skill", "check_skill"]


def test_side_effect_is_reported_as_pending_not_done(tmp_path, monkeypatch):
    monkeypatch.setattr(tools, "HERE", tmp_path)
    fake = FakeClient([tool_call("request_intro", '{"email": "r@x.com", "message": "coffee?"}'),
                       answer("I've noted your request; Sam will need to confirm before anything is sent.")])
    r = run("Introduce me to Sam, I'm r@x.com", client=fake)
    assert r["pending"] == [{"tool": "request_intro", "arguments": {"email": "r@x.com", "message": "coffee?"}}]
    assert not (tmp_path / "outbox.jsonl").exists()


# ---- the check: what plain code can and cannot catch --------------------------------------------
def test_project_named_without_a_lookup_is_unsupported():
    r = check_answer("Sam's Receipt reader project was great.", steps=[])
    assert not r["supported"] and "Receipt reader" in r["unsupported"][0]


def test_project_named_after_a_lookup_is_supported():
    steps = [{"tool": "lookup_project", "result": lookup_project("receipt")}]
    assert check_answer("The receipt reader checks the arithmetic in code.", steps)["supported"]


def test_check_cannot_see_an_invented_project():
    """Honest limit: a project that is not in the profile at all is invisible to this check.
    The tool's not-found result is the evidence; the eval reads the answer for it."""
    assert check_answer("Sam's blockchain voting app won an award.", steps=[])["supported"]


# ---- the real tool for the lab: errors as results, no network needed to prove it ---------------
def test_github_tool_rejects_a_bad_name_without_calling_github():
    from github_tool import recent_commits
    assert "owner/name" in recent_commits("just-a-word")["error"]
