# Lab: Build, change, and check

**Build time:** about 55 minutes after setup. Start when you reach Checkpoint C in the [setup guide](setup.md).

We will build a memorization trainer: one line of Shakespeare's Sonnet 18 at a time, with a Next button. The text is public domain. The agent will write the code. You will supply the behavior, choose a change, and check the result.

## 1. Define success and build (15 minutes)

In your `lyrics-trainer` folder, start the agent using `orclaude`. Use this prompt:

```text
Build a small memorization trainer using the text in lyrics.txt.
Show one nonblank line at a time, starting with the first line.
Show a counter such as "Line 1 of 14" and a Next button.
After the final line, Next returns to the first line.

Use one index.html containing plain HTML, CSS, and JavaScript.
Embed the poem from lyrics.txt so the app opens directly from disk.
No frameworks, packages, build step, external services, or API calls.
Make the text readable and the button usable with a keyboard.

Tell me your short plan before editing, then wait for my approval.
Do not commit or push anything yet.
```

Read the plan. Does it describe the requested behavior? Correct scope drift before approving. Let the agent create the file, then open `index.html` in a browser from Finder or File Explorer. No web server is needed for this version.

Try the Next button. Ask the agent to explain an unfamiliar piece of the implementation by pointing to the actual code. You do not need to master JavaScript syntax today.

Save a baseline in the terminal after leaving the agent session, or ask the agent to run these exact commands:

```bash
git status --short
git diff
git add index.html
git commit -m "Build the initial memorization trainer"
```

Untracked new files do not appear in plain `git diff`; open `index.html` to inspect it before adding it. Never add a key file.

## 2. Choose one change (15 minutes)

Pick **one**: a Previous button, a Restart button, keyboard shortcuts, or a visual improvement such as larger text and stronger contrast. Agree on boundary behavior before the agent edits. For example: should Previous on line 1 stay there or wrap to line 14?

Write the request in your own words. Include the behavior you want to preserve. A starting pattern:

```text
Add [my chosen change]. It should behave like this: [specific behavior].
Keep Next, the line counter, and wraparound working.
Keep the app in one file, with no new dependencies or API calls.
Explain the change before making it. Wait for my approval.
```

Review and approve the proposal, then try the result. If it misses your intention, refine the request. Record one example of how your instructions affected the outcome.

## 3. Check behavior (15 minutes)

Create a file named `CHECKS.md`. Copy this table and fill in **actual observations**, not what the agent predicts will happen.

| Check | Expected | Observed | Pass/fail |
|---|---|---|---|
| Open or refresh the page | First line; counter 1 of 14 | | |
| Click Next once | Second line; counter 2 of 14 | | |
| Continue to the last line | Last line; counter 14 of 14 | | |
| Click Next at the last line | First line; counter 1 of 14 | | |
| Tab to Next, then press Enter | Button advances one line | | |
| My change: ordinary case | Write the expected result first | | |
| My change: boundary case | Write the expected result first | | |

If a check fails, tell the agent the action, expected result, and observed result. Have it diagnose and propose a correction, then rerun that check and any earlier check the change could affect. Preserve a note of the initial failure. If everything passes, do not invent a bug: propose an additional edge case and check it.

These are repeatable **manual checks**, not an automated test suite or proof that the program has no bugs. We will automate appropriate checks as the course develops.

## 4. Explain and save (10 minutes)

Write a short `README.md` with:

- What the app does and how to open it.
- Which harness and model you used; distinguish the coding agent from the local app, which makes no model calls.
- Your chosen change and why you wanted it.
- One correction, clarification, or additional check you made.
- One thing you can explain in the code, pointing to the relevant function or lines.
- Usage evidence: approximate lab cost from the provider's activity page, or “unavailable” and why. Do not include keys, account screenshots, or a made-up estimate.
- Any remaining problem or setup blocker; identify pairing help or use of the book's fallback example.

Review the changed files, then commit:

```bash
git status --short
git diff
git add index.html CHECKS.md README.md
git commit -m "Add my improvement and record behavior checks"
git switch main
git merge first-build
git tag week01-submitted
```

Publish following the [submission sheet](../../assignments/week01-first-agent-session.md). A pull request, formal spec, and formal plan document are **not required this week**. Keep the initial and later commits; they show the progression.

## If you finish early

Choose a second small change, or ask for three **descriptions** of alternative interfaces and evaluate their readability and usability. Implement only one if time allows, then repeat the behavior checks. This uses an ordinary prompt; it does not require Anthropic's `/design` capability.

Do not add accounts, cloud deployment, databases, or an AI chatbot yet. Keep this first app small enough to understand.

## If setup is still blocked

Work alongside a classmate and take turns directing and checking. Record whose environment you used. For an example to inspect, Ken can provide the [book's initial trainer](https://github.com/kousen/claude-code-up-and-running-examples/blob/main/lyrics-trainer/ch02-first-doghouse/index.html). Label that starting point honestly; do not claim the example was generated in your session. Contact Ken to resolve individual access before the next class.

## Sources

Adapted from Ken Kousen's [Claude Code Lab 0](https://github.com/kousen/claude-code-training/blob/main/lab_handout.md), [book examples](https://github.com/kousen/claude-code-up-and-running-examples/tree/main/lyrics-trainer), and [Codex planning and steering warm-up](https://github.com/kousen/codex-training/tree/main/exercises/plan-mode-warmup). William Shakespeare, Sonnet 18, is supplied as public-domain text.
