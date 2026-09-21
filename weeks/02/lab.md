# Lab: Interview, intent, and a chat client

**Time:** about 50 minutes after the interview demonstration. Start when you reach Checkpoint D in the [setup additions](setup.md).

You will build a command-line program that sends one question to a model and prints the answer and the token usage. The agent writes the code. You write the intent first, by letting the agent interview you, and you verify the call afterward with evidence the program did not produce itself.

## 0. Create this week's repository (5 minutes)

This week starts the artifact chain, so use the course template. On GitHub, open [kousen/artifact-chain-template](https://github.com/kousen/artifact-chain-template), click **Use this template → Create a new repository**, name it `cpsc415-week02`, and make it public. Then clone it beside last week's folder:

```bash
cd ~/cpsc415
git clone https://github.com/YOUR_USERNAME/cpsc415-week02.git
cd cpsc415-week02
```

Leave `spec.md`, `plan.md`, and the other files alone. Only the `intent/` folder is required this week.

The template's `CLAUDE.md` describes the full chain for major projects, and the agent reads it at the start of every session. Tell it which rules apply this week. Open `CLAUDE.md` and add these two lines under **Working rules**:

```markdown
- This is the Week 2 introductory lab. Only the intent stage is assigned:
  no spec.md, no plan.md, no branches or pull requests. Commit to main.
- Standard library only. No packages, no pip install, no Maven or Gradle.
```

Then start the agent here with `orclaude` and the model announced in class.

## 1. The discovery interview (10 minutes)

Do not describe the program yet. Ask the agent to interview you:

```text
I want to build a small chat client. Before writing anything, interview me.
Ask one question at a time until you can fill in every section of
intent/TEMPLATE.md. Then write your draft to intent/chat-client.md
and stop. Do not write code yet.
```

Answer honestly, including "I don't know." Useful facts to have ready:

- **Language:** Python or Java, standard library only, no packages.
- **Behavior:** one question from the command line, one answer printed, then the model name and input/output token counts printed on a final line.
- **Configuration:** base URL and model name come from environment variables; the key comes from `OPENROUTER_API_KEY`. Nothing secret in the code.
- **Not in scope:** streaming, chat history, a web page, retries, more than one provider at a time.
- **Success:** it answers a question through OpenRouter; changing one environment variable points it at a different model; the token counts match the provider's usage record.

Read the draft. Correct at least two things the agent got wrong or made up, in the file, in your own words. Fill in **Approved by** with your name and today's date. Commit it:

```bash
git add intent/chat-client.md
git commit -m "Approve intent for the chat client"
```

## 2. Build from the intent (15 minutes)

```text
Read intent/chat-client.md. Tell me your short plan: which file you will
create and what it will contain. Wait for my approval before writing.
```

Approve the plan if it matches the intent. Then run the program. In the terminal where you entered your key:

**Python**

```bash
export CHAT_BASE_URL=https://openrouter.ai/api/v1
export CHAT_MODEL="the model announced in class"
python3 chat.py "In one sentence, what is a context window?"
```

**Java**

```bash
export CHAT_BASE_URL=https://openrouter.ai/api/v1
export CHAT_MODEL="the model announced in class"
java Chat.java "In one sentence, what is a context window?"
```

On Windows PowerShell, set variables with `$env:CHAT_MODEL = "..."`. Save a baseline commit once it runs.

## 3. Verify the call (10 minutes)

The program prints what the response said about itself. That is not evidence. Check:

1. **The usage record.** Open [OpenRouter Activity](https://openrouter.ai/activity). Find the request. Do the model name and token counts match what your program printed?
2. **The request.** Ask the agent to show you the exact JSON it sends. Identify the `messages` array, the two roles, and `max_tokens`. Change the system message and run again. Did the answer change in the way you expected?
3. **A parameter.** Set `max_tokens` very low (try 20). What happens to the answer? Some models spend output tokens on hidden reasoning before the visible answer; if you get an empty answer with tokens billed, that is what happened. Note it.

Record all of this in `CHECKS.md`:

| Check | Expected | Observed | Pass/fail |
|---|---|---|---|
| Question through OpenRouter | An answer and a usage line | | |
| Usage record matches | Same model; same or close token counts | | |
| System prompt changed | Answer style changes accordingly | | |
| `max_tokens` = 20 | Truncated or empty answer; tokens still billed | | |
| Model swapped (step 4) | Different model name in usage; answer may differ | | |
| Local model (optional) | Answer from localhost; no OpenRouter entry | | |

## 4. Swap the model (10 minutes)

Change only `CHAT_MODEL` to a second model Prof. Kousen names in class, and ask the same question. Write down both answers and both costs from the Activity page. Then, if you have a local model running, change `CHAT_BASE_URL` to its address and set `CHAT_API_KEY` to any string (Ollama ignores it). Same code, different destination.

You are comparing what you observed for one question. That is not a benchmark, and you should not describe it as one in your README.

## 5. Explain and save (10 minutes)

Write a short `README.md` with:

- What the program does and how to run it, including the environment variables.
- Which two things you corrected in the intent draft and why.
- One line of your code you can explain: where the request is built, or where the usage is read.
- The two models you compared, one sentence on how the answers differed, and the observed cost of each from the Activity page, or "unavailable" and why.
- Anything a local model did differently, if you tried one.

Commit and tag:

```bash
git add .
git commit -m "Chat client with checks and README"
git tag week02-submitted
git push -u origin main
git push origin week02-submitted
```

Publish following the [submission sheet](../../assignments/week02-chat-client.md).

## If you finish early

Ask the agent, without letting it edit, "What would you change about this program if it had to keep a conversation going across several questions?" Summarize the answer in your README. Do not build it; that is a spec question for Week 3.

## If you are blocked

Pair with a classmate and take turns interviewing and checking. Record whose environment you used. If OpenRouter access is the problem, tell Prof. Kousen today so a path can be arranged before Week 3.
