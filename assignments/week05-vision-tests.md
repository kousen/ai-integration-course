# Week 5: Receipts to data, with tests

**Due:** Monday, October 26, 2026, 1:30 PM, on Moodle.

**Category:** Participation and labs.

Complete the [Week 5 lab](../weeks/05/lab.md). Submit your repository URL and the tag **`week05-submitted`** in the Moodle Week 5 assignment.

## At the submitted tag

Your repository, created from the artifact-chain template, should contain:

- `intent/receipts.md`, approved by you.
- `spec.md` with two components, reader and checker; the reader has a language decision and a model decision naming the two models compared; numbered behaviors including the non-JSON reply, the inconsistent receipt, and the missing year; every dependency named with its reason.
- `plan.md` approved before the first code commit, with Proof split into tests that need no key and the eval that does.
- The program, the tests, and the eval, in any language. Tests that call a model are skipped when no key is set.
- `images/` and `images/expected.json` unchanged from the course copy, plus `my-receipts/` with at least two of your own photographs (no card numbers or names) and your hand-written expected values.
- `.claude/hooks/guard.py` and `.claude/settings.json`, the guard installed and committed.
- `CHECKS.md` with both models' results on the five receipts, the linter's findings, the step-4 record, and the results on your own receipts.
- `README.md` as the lab describes.

**No API key in the repository.**

## What Prof. Kousen will look for

| Evidence | Satisfactory for Week 5 |
|---|---|
| Tests | Two kinds exist and run: checker and parser tests that need no key, and an eval against `expected.json` that does. The commit history shows tests before the code they test. |
| The loop | `CHECKS.md` holds real output: the five receipts on both models with tokens, the linter's findings, and the first red-then-green run. |
| Vision | The program returns JSON from an image and the checker reports arithmetic problems instead of trusting the model. Failures on either model are explained as model misread or spec ambiguity. |
| Guardrail | The hook is installed and committed, and the step-4 record says what the agent did when a test disagreed with the key. |
| Understanding | You can explain the arithmetic check and the rule in the hook that fired, and say what a browser-driven check sees that a unit test cannot. |

## This week's chain stage

Tests are stage 4 of the artifact chain: the agent writes them, runs them, and you confirm the loop ran rather than taking "all tests pass" on faith. Week 6 adds reviewed pull requests. Team Project 1's Test milestone, agent-written tests plus a browser-driven check of the front end, is due the same day as this lab.
