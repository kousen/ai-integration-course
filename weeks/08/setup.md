# Week 8 setup additions

Nothing new to install: tool calling is a field on the chat request you have used since Week 2, and the `openrouter` SDK already carries it. One checkpoint that costs nothing, one that costs a fraction of a cent.

## 1. Pull the course repository

```bash
cd path/to/ai-integration-course
git pull
```

That gets you `examples/tool-loop/` (the tools, the loop, the GitHub tool, the no-key tests, the billed eval).

## 2. The no-key tests

```bash
cd examples/tool-loop
python3 -m pytest tests/test_loop.py -v
```

**Checkpoint A:** 19 passed in under a second, no key set. Read two of them before class: `test_endless_caller_stops_at_the_cap` and `test_bad_call_goes_back_to_the_model_as_an_error`. Each one scripts what the model "did" with a fake client and checks what the program did about it. That is how you test a loop without paying for it, and how you test the cases a real model only produces now and then.

## 3. One tool call

```bash
export OPENROUTER_API_KEY=...
python3 loop.py "What did Sam learn from the receipt reader project?"
```

**Checkpoint B:** a trace with two steps, like this (November 2, `minimax/minimax-m3`):

```
step 1  lookup_project({"name":"receipt reader"})  →  {"found": true, "project": {...  [0.73s]
step 2  answer  [1.61s, finish=stop]

Sam learned that edge cases are really specification questions, not model bugs. ...

stopped_by=answer  calls=['lookup_project']  cost=$0.000436  check=ok  [minimax/minimax-m3]
```

Step 1 is the model **asking** for a tool; nothing in the model ran `lookup_project`. The program did, and sent the result back as a message with `role: tool`. Step 2 is the model answering from it. Two chat calls, about four hundredths of a cent.

Now ask about something that is not there:

```bash
python3 loop.py "Tell me about Sam's blockchain voting project."
```

The tool returns `found: false` with the projects that do exist, and the answer should say so. If it describes a blockchain project anyway, you have met the third failure mode before class.

## 4. Which models can do this

```bash
curl -s "https://openrouter.ai/api/v1/models" | python3 -c "import sys,json; print([m['id'] for m in json.load(sys.stdin)['data'] if 'tools' in m.get('supported_parameters',[])][:20])"
```

Both class models are in that list. A model that is not will ignore `tools` or reject the request; the error message says which.

## If something goes wrong

| Symptom | Likely cause |
|---|---|
| `tool_calls` is always empty and the model answers in prose that it "would look that up" | The model does not support tools (section 4), or the description does not say when to call it. Compare with the example's descriptions: they are instructions, not labels |
| The answer is empty on `xiaomi/mimo-v2.6-flash` | Hidden reasoning; `loop.py` already sets `reasoning: {enabled: false}` for that model through `REASONING`. Add yours to the table if it behaves the same way |
| `arguments` is a string, not a dict | It always is: the model writes JSON text and your program parses it. `run_tool` does, and returns an error result when the text is not JSON |
| The loop runs to the cap on a simple question | Read the trace: usually the model is retrying a call that keeps erroring. The error message you return is what it reads; make it say what to do |
| GitHub answers 403 | The unauthenticated limit is 60 requests an hour per address; set `GITHUB_TOKEN` or wait |
