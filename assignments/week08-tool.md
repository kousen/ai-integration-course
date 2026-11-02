# Week 8: One real tool for the portfolio chatbot

**Due:** Monday, November 16, 2026, 1:30 PM, on Moodle.

**Category:** Participation and labs.

Complete the [Week 8 lab](../weeks/08/lab.md). Submit your **portfolio repository** URL and the tag **`week08-submitted`** in the Moodle Week 8 assignment.

## At the submitted tag

- `intent/tools.md`, approved by you.
- `spec.md` with a "Week 8: one tool" section: the tool as a component (language decision; model decision naming the class model and a comparison model, both with tool support); numbered behaviors including the schema, validation in code with error results, the unknown tool, the step cap and whose answer it is, the side-effect rule, the claim check, and the cost per question.
- `plan.md` with a Week 8 section approved before the first code commit, Proof split into no-key tests and the billed eval.
- `tools/`: the schema and the function, the loop with its cap, the checker, and the no-key tests with a scripted model covering the six misuse cases. Tests that call a model are skipped when no key is set.
- The tool wired into the chatbot's answer function, with the trace returned alongside the answer.
- `tools/CHECKS.md`: the eval table (five questions, two models: tools called, steps, pass or fail, cost, seconds); the three totals; the Misuse cases, What the check cannot catch, and The cost of a tool sections; the linter's findings.

**No API key in the repository.**

## What Prof. Kousen will look for

| Evidence | Satisfactory for Week 8 |
|---|---|
| The model asks, the program decides | The schema is sent with the request; the program parses and validates every call in code; errors go back as results; the loop has a cap and the capped answer is the program's. |
| Misuse cases tested without a key | Six no-key tests with a scripted model: single shot, bad arguments, unknown tool, endless caller, side effect held, unsupported claim. They fail before the code and pass after it, in the commit history. |
| One real tool in the chatbot | The chatbot answers a question only the tool can answer, through the same answer function the typed and voice paths use; the trace shows the call and the result. |
| The eval, with the bill | Five questions on two models in `CHECKS.md`, with the tools called, steps, verdicts, and cost per question; the cost of a question with and without a tool. |
| Understanding | You can say what the model can and cannot do with a schema, why `arguments` is a string, what stops an endless loop and what the visitor sees, why a side-effect tool waits for a person, and what plain code cannot catch. |

## This week's chain stage

No new stage: intent, spec, plan, tests, and a commit history that shows the tests before the code. The cost of a tool call joins the per-turn cost in the hosting decision (`spec.md`, before November 30).
