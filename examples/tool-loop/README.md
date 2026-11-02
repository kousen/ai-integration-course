# The tool loop: the model asks, the program decides

Week 8's example. A chatbot for a fictional student's portfolio that knows **nothing** about the student except what its tools return. Three tools, a loop with a step cap, a checker that looks for claims the tools did not support, no-key tests with a scripted model, and a billed eval on the two class models.

```
tools.py          the three schemas (what the model sees) and functions (what the program runs);
                  validate() and run_tool(): bad calls come back as error results, never exceptions;
                  request_intro has a side effect and is never run on the model's say-so alone
loop.py           run(): send with tools, run what the model asked for, send the results back, repeat
                  until the model answers or max_steps; check_answer() in plain code
github_tool.py    a real tool for the lab: recent commits of a public repository, errors as results
profile.json      the fictional student (same file as examples/voice-loop)
tests/test_loop.py   18 no-key tests: the tools, the decision, the loop with a FakeClient, the check
tests/test_eval.py   five questions on each class model, skipped without a key, about a cent in all
```

## Run it

```bash
pip install -r requirements.txt pytest
python3 -m pytest tests/test_loop.py -v                       # no key, under a second

export OPENROUTER_API_KEY=...
python3 loop.py "What did Sam learn from the receipt reader project?"
python3 loop.py "Tell me about Sam's blockchain voting project."          # nothing to find
python3 loop.py "Introduce me to Sam, I'm recruiter@example.com"         # a side effect, held
python3 loop.py "Has Sam shipped Kubernetes?" --model xiaomi/mimo-v2.6-flash
python3 -m pytest tests/test_eval.py -v -s                    # both class models, about $0.01
```

One trip through the loop prints like this (November 2, `minimax/minimax-m3`):

```
step 1  lookup_project({"name":"receipt reader"})  →  {"found": true, "project": {"name": "Receipt reader", ...  [0.73s]
step 2  answer  [1.61s, finish=stop]

Sam learned that edge cases are really specification questions, not model bugs. ...

stopped_by=answer  calls=['lookup_project']  cost=$0.000436  check=ok  [minimax/minimax-m3]
```

## What to look at

- **The schema is the contract.** `TOOLS` in `tools.py` is sent with every request. The description is what the model reads to decide when to call; write it as an instruction ("use this before saying anything about a project"), not a label.
- **The program decides.** `run_tool` parses the arguments, validates them against the schema in plain code, refuses unknown tools, and returns every problem as a JSON result so the model can correct itself. `request_intro` is in `SIDE_EFFECTS`: the loop records it as pending and nothing is sent. That is the same shape as Claude Code's permission prompt and the Week 5 PreToolUse hook.
- **The loop has a cap.** `max_steps` is the only thing standing between you and a model that asks for the same tool forever. When the cap trips, the answer is the program's sentence, not the model's.
- **The check is honest about its limits.** `check_answer` catches a project named without a lookup and a skill called shipped without a check. It cannot see a project that is not in the profile at all; the tool's not-found result is the evidence for that, and the eval reads the answer for it.
- **Two models, one loop.** `REASONING` turns hidden reasoning off for MiMo (it answers nothing otherwise) and leaves it on for M3. On November 2 both models called the right tool in all five cases; M3 made parallel calls and a second round on the invented project, MiMo asked for the skill check unprompted on the intro question.

## Costs (November 2, 2026)

| Question | `minimax/minimax-m3` | `xiaomi/mimo-v2.6-flash` |
|---|---|---|
| project (one lookup, then the answer) | $0.0004 | $0.0001 |
| invented project (four lookups, two skill checks on M3) | $0.0009 | $0.0001 |
| intro (side effect held) | $0.0004 | $0.0001 |

Every tool call costs a second chat call to deliver the result, so a question with a tool is at least twice a question without one.
