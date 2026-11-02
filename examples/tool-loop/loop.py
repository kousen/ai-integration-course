"""The tool loop: the model asks, the program decides, the model answers from what it got back.

    export OPENROUTER_API_KEY=...
    python3 loop.py "What did Sam learn from the receipt reader?"
    python3 loop.py "Has Sam shipped anything with Kubernetes?" --model xiaomi/mimo-v2.6-flash
    python3 loop.py "Tell me about Sam's blockchain project"          # nothing to find; watch the answer

The profile is NOT in the system prompt. The only way the model can learn anything about the
person is to call a tool, so every claim in the answer should trace back to a tool result, and
`check_answer` looks for the ones that do not.

One `run` is one question. Each trip through the loop is one billed chat call; a tool request
costs a second call to deliver the result. The loop stops when the model answers without asking
for a tool, or at `max_steps`, whichever comes first.
"""
import argparse
import json
import os
import time

from tools import PROFILE, TOOLS, run_tool

DEFAULT_MODEL = os.environ.get("CHAT_MODEL", "minimax/minimax-m3")
# Per-model decision (Week 5): MiMo must have hidden reasoning off or it thinks for the whole
# budget and returns nothing; M3 must keep it on. Add a model here when you learn what it needs.
REASONING = {"xiaomi/mimo-v2.6-flash": {"enabled": False}}

SYSTEM = f"""You are the assistant on {PROFILE['name']}'s portfolio site. You know nothing about
{PROFILE['name']} except what the tools return. Before you say anything about a project or a skill,
call the matching tool. If a tool says a project is not on record or a skill has no record, say so
plainly and do not guess. Never describe a project or claim a skill the tools did not return.
Answer in two or three plain sentences. Do not mention the tools by name."""


def _call(client, model, messages):
    kwargs = {"model": model, "messages": messages, "tools": TOOLS, "max_tokens": 1500}
    if model in REASONING:
        kwargs["reasoning"] = REASONING[model]
    return client.chat.send(**kwargs)


def run(question: str, model: str = DEFAULT_MODEL, max_steps: int = 4, client=None,
        allow_side_effects: bool = False) -> dict:
    """Returns {"answer", "steps", "stopped_by", "cost", "calls", "pending", "check"}."""
    if client is None:
        from openrouter import OpenRouter
        client = OpenRouter(api_key=os.environ["OPENROUTER_API_KEY"])
    messages = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": question}]
    steps, cost, pending = [], 0.0, []
    for step in range(1, max_steps + 1):
        t0 = time.time()
        c = _call(client, model, messages)
        cost += getattr(c.usage, "cost", None) or 0.0
        msg = c.choices[0].message
        calls = msg.tool_calls or []
        if not calls:                                   # the model answered: the loop is done
            answer = (msg.content or "").strip()
            steps.append({"step": step, "answer": answer, "seconds": round(time.time() - t0, 2),
                          "finish": c.choices[0].finish_reason})
            return _result(answer, steps, "answer", cost, pending)
        # the model asked for one or more tools: record the request exactly as it was made
        messages.append({"role": "assistant", "content": msg.content or "",
                         "tool_calls": [{"id": tc.id, "type": "function",
                                         "function": {"name": tc.function.name, "arguments": tc.function.arguments}}
                                        for tc in calls]})
        for tc in calls:
            result = run_tool(tc.function.name, tc.function.arguments, allow_side_effects)
            if "pending" in result:
                pending.append(result["pending"])
            steps.append({"step": step, "tool": tc.function.name, "arguments": tc.function.arguments,
                          "result": result, "seconds": round(time.time() - t0, 2)})
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": json.dumps(result)})
    # the cap: the model never stopped asking. The answer is what the program says, not the model.
    answer = f"I couldn't finish answering that in {max_steps} steps."
    return _result(answer, steps, "cap", cost, pending)


def _result(answer, steps, stopped_by, cost, pending):
    return {"answer": answer, "steps": steps, "stopped_by": stopped_by, "cost": round(cost, 6),
            "calls": [s["tool"] for s in steps if "tool" in s], "pending": pending,
            "check": check_answer(answer, steps)}


def check_answer(answer: str, steps: list) -> dict:
    """Plain code looking for claims the tools did not support. A project name in the answer must
    have come back from a tool (a lookup that found it, or a not-found result that listed what is
    on record); a skill named as shipped must have been checked and found. This cannot catch everything a model might invent, and that is the point of the lab's
    misuse cases: say what it does catch and what it cannot."""
    found_projects = set()
    for s in steps:
        if s.get("tool") != "lookup_project":
            continue
        if s["result"].get("found"):
            found_projects.add(s["result"]["project"]["name"].lower())
        for name in s["result"].get("projects_on_record", []):     # a not-found result names them
            found_projects.add(name.lower())
    checked_skills = {s["result"].get("as_listed", "").lower() for s in steps
                      if s.get("tool") == "check_skill" and s["result"].get("status") == "shipped"}
    low = answer.lower()
    unsupported = []
    for p in PROFILE["projects"]:
        key = p["name"].split("(")[0].strip().lower()           # "receipt reader", "ask the course"
        if key in low and p["name"].lower() not in found_projects:
            unsupported.append(f"project {p['name']!r} mentioned without a lookup")
    for s in PROFILE["skills_shipped"]:
        word = s.split(" ")[0].lower()                           # "python", "java", "pytest", "git"
        if len(word) > 3 and word in low and s.lower() not in checked_skills and "shipped" in low:
            unsupported.append(f"skill {s!r} described as shipped without a check")
    return {"supported": not unsupported, "unsupported": unsupported}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("question")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--max-steps", type=int, default=4)
    ap.add_argument("--allow-side-effects", action="store_true", help="run request_intro for real")
    a = ap.parse_args()
    r = run(a.question, a.model, a.max_steps, allow_side_effects=a.allow_side_effects)
    for s in r["steps"]:
        if "tool" in s:
            print(f"step {s['step']}  {s['tool']}({s['arguments']})  →  {json.dumps(s['result'])[:160]}  [{s['seconds']}s]")
        else:
            print(f"step {s['step']}  answer  [{s['seconds']}s, finish={s['finish']}]")
    print(f"\n{r['answer']}\n")
    print(f"stopped_by={r['stopped_by']}  calls={r['calls']}  cost=${r['cost']:.6f}  "
          f"check={'ok' if r['check']['supported'] else r['check']['unsupported']}  [{a.model}]")
    if r["pending"]:
        print("pending (not run):", json.dumps(r["pending"]))


if __name__ == "__main__":
    main()
