# Week 3 setup additions

Nothing new to install. Week 1 and Week 2 setup still apply: Git, Claude Code, your OpenRouter key in the environment, `orclaude`, and a Python or Java runtime.

## 1. Confirm last week's client still runs

In a terminal where the key is set:

```bash
export CHAT_BASE_URL=https://openrouter.ai/api/v1
export CHAT_MODEL=minimax/minimax-m3
python3 chat.py "Reply with the single word OK."      # or: java Chat.java "..."
```

**Checkpoint E:** you get an answer and a usage line. If you get `401`, the key is not set in this terminal; if you get an empty answer with tokens billed, that is the hidden-reasoning case from Week 2 and it comes up again today.

## 2. Java and JSON

Java's standard library has no JSON parser. For today's lab, Java students may either let the agent write a small parser for the three fields the eval checks, or add one JSON library (Jackson or Gson) as a single jar on the classpath. Either choice belongs in `spec.md` under the language decision, with the trade-off stated. Python's `json` module needs nothing.

## 3. Claude Enterprise seats

Trinity has issued Claude Enterprise seats to everyone enrolled. If you received the invitation email at your trincoll address, you may sign in, but keep using `orclaude` for today's lab so that your calls appear on the OpenRouter Activity page you verify against. Prof. Kousen will walk through the seat setup once he has tested it. If you did not receive an email, say so today.

## If something goes wrong

| Symptom | Next action |
|---|---|
| Reply is not JSON, or has text around it | Expected sometimes. The eval counts it as a failure; the lab's step 4 asks you to handle it |
| Empty reply, `finish_reason` is `length` | The model spent the output budget on reasoning; raise `max_tokens` |
| One model passes, the other fails a case | That is the comparison. Record it; do not change the case to make it pass |
| `402` or a credit message | OpenRouter balance or spend cap exhausted; tell Prof. Kousen |
