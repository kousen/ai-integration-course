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

## 3. Your Claude Enterprise seat

Trinity has added everyone enrolled to its Claude organization. The invitation email goes to your trincoll address; if you have not received one, tell Prof. Kousen today. Prof. Kousen tested his own seat on September 22; this is what to expect.

**Signing in.** Run plain `claude` (not `orclaude`) and use `/login`. Type your **trincoll.edu email address first**; the single-sign-on option appears only after that, and it takes you to Trinity's usual login page. If the browser is already signed in to a personal Microsoft account, Trinity's login may reject you; clear the site data for live.com, microsoftonline.com, microsoft.com, and trincoll.edu, then try again.

**What the seat gives you.** `/model` offers Opus 5 (the organization default), Opus 5 with a 1M-token context, Sonnet 5, and Haiku 4.5. `/usage` shows a **$50 monthly credit** that resets on the first of the month. A five-minute test session on Opus 5 cost about $0.24, so the credit covers a month of coursework if you do not leave Opus running with a 1M context all day. Sonnet 5 costs less per token and handles the labs well; consider making it your default.

**First launch.** The permission mode starts as manual, which asks before every edit and command. Press Shift+Tab to switch to auto; the choice persists. If you also have a personal Claude account, keep it separate: `CLAUDE_CONFIG_DIR=~/.claude-trinity claude` runs the seat with its own settings and login. That directory starts empty, so it has none of your MCP servers or skills until you add them.

**What the seat does not give you.** It signs the coding agent in; it does not give your own program an API key. The chat client and today's classifier still read `OPENROUTER_API_KEY`. For today's lab, run the agent whichever way you prefer, but the program's calls go through OpenRouter so you can verify them on the Activity page.

## If something goes wrong

| Symptom | Next action |
|---|---|
| Reply is not JSON, or has text around it | Expected sometimes. The eval counts it as a failure; the lab's step 4 asks you to handle it |
| Empty reply, `finish_reason` is `length` | The model spent the output budget on reasoning; raise `max_tokens` |
| One model passes, the other fails a case | That is the comparison. Record it; do not change the case to make it pass |
| `402` or a credit message | OpenRouter balance or spend cap exhausted; tell Prof. Kousen |
