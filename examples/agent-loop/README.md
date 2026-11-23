# The agent loop: a host that plans, revises, remembers, asks, and stops

Week 10's example. [`examples/mcp-server/host.py`](../mcp-server/host.py) from Week 9, grown into an agent with no framework. The tools still come from an MCP server; the model still only asks. What is new is six decisions, each one an `if` in `agent.py`:

| | What the program does | Flag |
|---|---|---|
| 1. Plan | One call with no tools, so the model can only write its plan (the prompt lists the tool names); the plan stays in the conversation and is never summarized | `--plan` |
| 2. Revise | A tool error, or arguments that are not a JSON object, goes back as a result so the model can change the call; the **same failed or denied call twice** ends the run | always on |
| 3. Context budget | When the conversation passes a size, everything after the task (and the plan) is replaced by notes the model writes | `--budget 2500` |
| 4. Memory | A `remember` tool the host itself offers; notes are saved to `memory.json` and loaded into the next run's system prompt, each cut to one line of 200 characters, the newest 20 | `--memory` |
| 5. Approval | A tool **not** in `READ_ONLY` runs only if a person says yes; with nobody to ask, it is denied. With a person there, `remember` needs a yes too | `--approve` |
| 6. Caps | A step cap and a cost cap, checked before every billed call in the loop; at most 8 tool calls run per reply | `--max-steps`, `--max-cost` |

```
agent.py             about 220 lines; `run` returns the answer, stopped_by, steps, cost, and a trace
tests/test_agent.py  37 no-key tests: a scripted model on one side, the Week 9 server in memory on the other
poisoned-*.json      two notes to copy over memory.json, for seeing what a planted note does
```

`stopped_by` is one of `answer`, `steps`, `cost`, `repeat`. The model can end a run in only the first way; the other three are the program's.

## Run it

```bash
python3 -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python3 -m pytest tests -v            # no key, no network, under a second
export OPENROUTER_API_KEY=...
```

By default the agent starts `../mcp-server/server.py` over stdio. The trace prints to stderr as it runs; the answer and the stopping reason print at the end.

```bash
TASK="Look up the receipt reader project, get the three latest commits in kousen/ai-integration-course, and then ask Sam for an introduction: I am recruiter@example.com and I want to talk about a junior role."

python3 agent.py "What did Sam learn from the receipt reader project?"     # Week 9's host.py loop; the gate, the repeat rule, and the caps are always on
python3 agent.py "$TASK" --plan                                            # 1
python3 agent.py "What are the latest commits in kousen/no-such-repo-here?"    # 2
python3 agent.py "$TASK" --plan --budget 2500                              # 3
python3 agent.py "Remember that I prefer answers as a bulleted list." --memory     # 4, then run any task with --memory
python3 agent.py "$TASK" --approve                                         # 5: answer n, then run again and answer y
python3 agent.py "$TASK" --max-steps 1                                     # 6
python3 agent.py "$TASK" --max-cost 0.0002                                 # 6
```

Add `--model xiaomi/mimo-v2.6-flash` to any of them for the second class model. Without `--model`, the agent uses `CHAT_MODEL` if that variable is still exported from Week 2, and `minimax/minimax-m3` otherwise; the last line of output names the model that ran.

## Your team's server

```bash
python3 agent.py "your task" --server ../../your-tp2-repo/server.py     # stdio: the agent starts it
python3 agent.py "your task" --server http://localhost:8000/mcp         # or a URL
```

Nothing in `agent.py` names the portfolio tools except `READ_ONLY`. Put the names of your own tools that only read there. Every other tool, including one you add later and forget to list, is denied unless a person approves it: a forgotten name costs you a prompt, not an unapproved side effect.

## What to notice

- **One step can hold several tool calls.** Both class models ask for all three tools of `$TASK` in one reply, so the whole task is two steps: the requests, then the answer. The step cap counts replies, so `agent.py` also runs at most 8 calls from one reply and cuts each result to 4,000 characters.
- **The plan is not enforced.** The program asks for it and keeps it in view; nothing checks that the model follows it. Compare the plan with the trace.
- **Summarizing loses things.** Run with `--budget` and read the notes: which exact value did not survive? The task itself is never summarized.
- **Memory is input.** A note in `memory.json` is read by the model on every later run, whoever wrote it. Edit the file by hand and see what the agent does; then see which calls the approval gate still stops. On November 23, 2026, both class models ignored a blunt instruction planted there; a note written to look like the user's own standing request got one model to call `request_intro` (denied by the gate) and the other to say it had made a request that it never made.
- **Two gates.** The host's approval and the server's own gate (`request_intro` records a pending request and never sends) are separate. Approve the call and read `../mcp-server/pending.jsonl`.
- **The cost cap can be passed by one call.** It is checked before each call in the loop (and again after a summary), and a call's cost is known only after it returns. A reply that reports no cost is charged one cent, so the cap still ends the run.
