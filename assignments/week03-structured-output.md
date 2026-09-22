# Week 3: Structured output with a five-case eval

**Due:** Monday, October 5, 2026, 1:30 PM, on Moodle.

**Category:** Participation and labs.

Complete the [Week 3 lab](../weeks/03/lab.md). Submit your repository URL and the tag **`week03-submitted`** in the Moodle Week 3 assignment.

## At the submitted tag

- `intent/classifier.md`, approved by you.
- `spec.md` from the template, with both design decisions filled in for the one component and five numbered behaviors. At least one correction of yours in the commit history or described in the README.
- The classifier program and an eval runner, standard library only (Java may add one JSON library).
- `cases.json` or equivalent with five cases: three clear, one ambiguous that accepts two answers, one that must produce `unknown`.
- `CHECKS.md` with the eval results for at least two hosted models and the `max_tokens` 400 run, including which cases failed and how.
- `README.md` as the lab describes.
- `CLAUDE.md` with the Week 3 lines and your team's conventions.

No API key in the repository.

## What Prof. Kousen will look for

| Evidence | Satisfactory for Week 3 |
|---|---|
| Spec | Follows from the intent; language and model decisions each name an alternative and a reason; behaviors are checkable. |
| Eval | Five cases with a stated purpose each; the `unknown` case is present; a non-JSON reply fails a case without crashing the runner. |
| Comparison | Two models run on the same cases; differences recorded as observations; failures classified as judgment calls or real. |
| Understanding | You can explain the line that extracts JSON from a reply and why the spec says what it says. |

## This week's chain stage

Design is stage 2. Week 4 adds `plan.md`, Week 5 automated tests, Week 6 reviewed pull requests.

Tests are not required this week. If you add them, use any framework you like; they cannot lower your grade.
