"""An agent from scratch: Week 9's host.py, plus the six things that make a loop an agent.

    export OPENROUTER_API_KEY=...
    python3 agent.py "What did Sam learn from the receipt reader project?"          # host.py again
    python3 agent.py "$TASK" --plan                    # 1. say the plan before acting
    python3 agent.py "Latest commits in kousen/no-such-repo-here?"                  # 2. errors come back; a repeat stops
    python3 agent.py "$TASK" --budget 2500             # 3. a context budget; older steps are summarized
    python3 agent.py "Remember that I prefer short answers." --memory               # 4. notes that outlive the run
    python3 agent.py "$TASK" --approve                 # 5. a person approves anything that changes something
    python3 agent.py "$TASK" --max-steps 1 --max-cost 0.0002                        # 6. two caps the model cannot raise

No framework. The model still only asks; every decision below is an `if` in this file.
The tools come from an MCP server (default: ../mcp-server/server.py, the Week 9 example), so
pointing --server at your team's server gives you TP2's second host.

`run` returns {"answer", "stopped_by", "steps", "cost", "trace"}. `stopped_by` is one of
answer, steps, cost, repeat: the model ends a run in only the first way.
"""
import argparse
import asyncio
import json
import os
import pathlib
import sys

from mcp import Client, StdioServerParameters

HERE = pathlib.Path(__file__).parent
REASONING = {"xiaomi/mimo-v2.6-flash": {"enabled": False}}     # per-model, as in Weeks 8 and 9
SYSTEM = ("You complete the user's task with the tools provided. Answer only from what the tools "
          "return. If a tool reports an error, change something or say plainly that it failed; "
          "never repeat the same call. If a tool call is denied, say it was not done. "
          "Two or three plain sentences at the end.")
PLAN = ("Before using any tool, write a numbered plan of at most four steps for this task and "
        "name the tool each step needs. Do not answer the task yet. The tools are:\n")
GATED = {"request_intro"}      # tools that change something: a person decides, not the model

# 4. Memory is a tool this host offers itself. The server never sees it.
REMEMBER = {"type": "function", "function": {
    "name": "remember",
    "description": "Save one short note for future runs. Only when the user asks you to remember something.",
    "parameters": {"type": "object", "properties": {"note": {"type": "string", "maxLength": 200}},
                   "required": ["note"]}}}


def size(messages) -> int:
    """Characters in the conversation: a rough stand-in for tokens (about four characters each)."""
    return sum(len(json.dumps(m)) for m in messages)


def ask(llm, model, messages, tools=None):
    """One billed call. Returns (message, cost in dollars)."""
    kwargs = {"model": model, "messages": messages, "max_tokens": 1500}
    if tools:
        kwargs["tools"] = tools
    if model in REASONING:
        kwargs["reasoning"] = REASONING[model]
    c = llm.chat.send(**kwargs)
    return c.choices[0].message, getattr(c.usage, "cost", None) or 0.0


def compact(llm, model, messages):
    """3. Replace everything after the task with notes the model writes. Returns (messages, cost).
    Called only between steps, so no tool request is ever separated from its result."""
    transcript = "\n".join(f"{m['role']}: {m.get('content') or json.dumps(m.get('tool_calls'))}"
                           for m in messages[2:])
    msg, cost = ask(llm, model, [
        {"role": "system", "content": "You compress an agent's working transcript into notes."},
        {"role": "user", "content": f"Task: {messages[1]['content']}\n\nTranscript:\n{transcript}\n\n"
                                    "List what has been learned and done so far as short bullet points. Keep exact "
                                    "names, numbers, and errors. Nothing else."}])
    notes = {"role": "user", "content": "Notes so far (earlier steps were summarized to save context):\n"
                                        f"{(msg.content or '').strip()}\nContinue the task."}
    return messages[:2] + [notes], cost


async def run(task: str, model: str, server, llm=None, *, plan=False, max_steps=6, max_cost=0.05,
              budget=None, memory=None, approve=None) -> dict:
    """`memory` is a file path or None; `approve` is a function (name, args) -> bool or None."""
    if llm is None:
        from openrouter import OpenRouter
        llm = OpenRouter(api_key=os.environ["OPENROUTER_API_KEY"])
    trace, cost, failed = [], 0.0, set()

    def note(**entry):
        trace.append(entry)
        print("  ".join(f"{k}={str(v)[:110]!r}" if isinstance(v, str) else f"{k}={v}" for k, v in entry.items()),
              file=sys.stderr)

    def done(answer, stopped_by, step):
        return {"answer": answer, "stopped_by": stopped_by, "steps": step, "cost": round(cost, 6), "trace": trace}

    system = SYSTEM
    notes = json.loads(memory.read_text()) if memory and memory.exists() else []
    if notes:      # 4. loaded as text the model reads: it can be stale or wrong, so the prompt says so
        system += "\nNotes saved in earlier runs (they may be out of date):\n" + "\n".join(f"- {n}" for n in notes)
    messages = [{"role": "system", "content": system}, {"role": "user", "content": task}]

    async with Client(server) as mcp:
        tools = [{"type": "function", "function": {"name": t.name, "description": t.description,
                                                   "parameters": t.input_schema}}
                 for t in (await mcp.list_tools()).tools]
        if memory:
            tools.append(REMEMBER)

        if plan:   # 1. one call with no tools, so the only thing the model can do is write the plan.
            # Without `tools` the model has not seen what exists, so the prompt lists the names.
            menu = "\n".join(f"- {t['function']['name']}: {t['function']['description']}" for t in tools)
            msg, c = ask(llm, model, messages + [{"role": "user", "content": PLAN + menu}])
            cost += c
            note(plan=(msg.content or "").strip())
            messages += [{"role": "assistant", "content": msg.content or ""},
                         {"role": "user", "content": "Carry out the plan. If a step fails, say what you will change."}]

        for step in range(1, max_steps + 1):
            if cost >= max_cost:                                    # 6. checked before every billed call
                return done(f"I stopped: this task reached its ${max_cost} budget.", "cost", step - 1)
            if budget and size(messages) > budget:                  # 3.
                before = size(messages)
                messages, c = compact(llm, model, messages)
                cost += c
                note(step=step, compacted=f"{before} -> {size(messages)} characters")
            msg, c = ask(llm, model, messages, tools)
            cost += c
            if not msg.tool_calls:
                return done((msg.content or "").strip(), "answer", step)
            messages.append({"role": "assistant", "content": msg.content or "",
                             "tool_calls": [{"id": tc.id, "type": "function",
                                             "function": {"name": tc.function.name, "arguments": tc.function.arguments}}
                                            for tc in msg.tool_calls]})
            for tc in msg.tool_calls:
                name, raw = tc.function.name, tc.function.arguments or "{}"
                if (name, raw) in failed:                           # 2. the same failing call, again
                    return done(f"I stopped: {name} failed and was asked for again unchanged.", "repeat", step)
                try:
                    args = json.loads(raw)
                    if name == "remember" and memory:               # 4.
                        notes.append(str(args["note"])[:200])
                        memory.write_text(json.dumps(notes, indent=1))
                        text = "saved"
                    elif name in GATED and not (approve and approve(name, args)):     # 5.
                        text = "DENIED: a person did not approve this call. It was not done; do not retry."
                    else:
                        result = await mcp.call_tool(name, args)
                        text = result.content[0].text if result.content else ""
                        if result.is_error:
                            text = "ERROR: " + text
                except (json.JSONDecodeError, KeyError) as e:
                    text = f"ERROR: bad arguments: {e}"
                if text.startswith("ERROR"):
                    failed.add((name, raw))
                note(step=step, tool=name, arguments=raw, result=text)
                messages.append({"role": "tool", "tool_call_id": tc.id, "content": text})
        return done(f"I stopped: the step limit ({max_steps}) was reached before the task was finished.", "steps", max_steps)   # 6.


def ask_person(name, args) -> bool:
    return input(f"\nThe agent wants to run {name}({json.dumps(args)}). Allow? [y/N] ").strip().lower().startswith("y")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("task")
    p.add_argument("--model", default=os.environ.get("CHAT_MODEL", "minimax/minimax-m3"))
    p.add_argument("--server", default=None, help="URL of an HTTP MCP server, or a path to a server.py; default is ../mcp-server/server.py")
    p.add_argument("--plan", action="store_true")
    p.add_argument("--budget", type=int, help="characters of conversation before older steps are summarized")
    p.add_argument("--memory", action="store_true", help="load and save notes in memory.json")
    p.add_argument("--approve", action="store_true", help="ask before running a gated tool (default: deny)")
    p.add_argument("--max-steps", type=int, default=6)
    p.add_argument("--max-cost", type=float, default=0.05, help="dollars")
    a = p.parse_args()
    if a.server and a.server.startswith("http"):
        target = a.server
    else:
        path = pathlib.Path(a.server) if a.server else HERE.parent / "mcp-server" / "server.py"
        target = StdioServerParameters(command=sys.executable, args=[path.name], cwd=str(path.resolve().parent))
    r = asyncio.run(run(a.task, a.model, target, plan=a.plan, max_steps=a.max_steps, max_cost=a.max_cost,
                        budget=a.budget, memory=HERE / "memory.json" if a.memory else None,
                        approve=ask_person if a.approve else None))
    print(f"\n{r['answer']}\n\nstopped_by={r['stopped_by']}  steps={r['steps']}  cost=${r['cost']:.6f}  [{a.model}]")
