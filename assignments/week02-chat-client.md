# Week 2: Interview, intent, and a chat client

**Due:** Monday, September 28, 2026, 1:30 PM, on Moodle.

**Category:** Participation and labs.

Complete the [Week 2 lab](../weeks/02/lab.md). Submit your repository URL and the tag **`week02-submitted`** in the Moodle Week 2 assignment.

## At the submitted tag

Your repository, created from the artifact-chain template, should contain:

- `intent/chat-client.md`: the agent's draft, corrected by you, with your name and date under **Approved by**. The commit history should show the draft and your corrections as separate steps, or your README should describe what you changed.
- `chat.py` or `Chat.java`: a standard-library program that reads `CHAT_BASE_URL`, `CHAT_MODEL`, and the key from the environment, sends one question, and prints the answer plus the model name and token counts.
- `CHECKS.md`: the six checks from the lab with expected and observed results.
- `README.md`: how to run it, your two intent corrections, one code explanation, the two-model comparison with observed costs, and any local-model note.
- The template's other files, untouched or lightly edited. `spec.md` and `plan.md` are not required this week.

**No API key belongs in the repository.** If a key appears in any commit, treat it as compromised, revoke it at OpenRouter, and tell Prof. Kousen.

## What Prof. Kousen will look for

| Evidence | Satisfactory for Week 2 |
|---|---|
| Intent | The agent interviewed you; you corrected the draft; the file is approved and specific. |
| The call | The program works, configuration is in the environment, and the request shape is one you can describe. |
| Verification | Token counts and model names were checked against the provider's record, not the program's own output. |
| Comparison | Two models were tried with observed cost recorded as observation, not as a ranking claim. |
| Understanding | You can explain one line of the code and why the intent says what it says. |

## This week's chain stage

Intent is stage 1 of the artifact chain. Week 3 adds the specification, Week 4 the written plan, Week 5 automated checks, and Week 6 reviewed pull requests. The team projects and the portfolio use the full chain.

The AI Fluency for Students certificate is a separate Moodle submission, also due September 28.
