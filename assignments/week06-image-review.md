# Week 6: Image set, critique checked, reviewed PR

**Due:** Monday, November 2, 2026, 1:30 PM, on Moodle.

**Category:** Participation and labs.

Complete the [Week 6 lab](../weeks/06/lab.md). Submit **two things** in the Moodle Week 6 assignment: the URL of your pull request in the team repository, and your Week 5 repository URL with the tag **`week06-submitted`**.

## At the submitted tag, in your Week 5 repository

- `intent/image-set.md`, approved by you.
- `spec.md` with a "Week 6: image set" section: a generator component (language decision; model decision naming `black-forest-labs/flux.2-klein-4b` and the comparison image model; the `openrouter` SDK under Dependencies with its reason) and a critic-checker component (model decision naming the vision model and the second model used to check it); numbered behaviors including the non-JSON critique, the unanswered requirement, the invented requirement, and expected text compared in code.
- `plan.md` with a Week 6 section approved before the first code commit, Proof split into no-key tests and the billed eval, with the eval's cost.
- `week06/`: the program, the tests, `prompts.json` (five prompts from one family, with seeds and requirements), the five images with `manifest.json`, and the critique files from both vision models. Tests that call a model are skipped when no key is set.
- `week06/CHECKS.md`: per image, the cost and the checker's verdict; the seed check; the comparison image model's cost and verdict; the step-5 record (the disagreements, the open-ended critique's claims, which check caught what); the linter's findings; and the **Review** section (PR URL, findings by pass, what was fixed, what was pushed back on, the last exit code, who approved).
- `.claude/hooks/guard.py` and `.claude/settings.json`, still installed.

## In the team repository

- A branch `week06-<yourname>` merged into `main` through a pull request that carries your image set and your piece of the wiring, with the reviewer's findings as a comment, your replies to any you disagreed with, and a teammate's approval. The commit history on the branch shows tests before the code they test.

**No API key in either repository.**

## What Prof. Kousen will look for

| Evidence | Satisfactory for Week 6 |
|---|---|
| Images and cost | Five images from one prompt family with fixed seeds, `manifest.json` recording prompt, seed, model, media type, and the cost from the reply for each; the seed check and the comparison model's cost recorded in `CHECKS.md`. |
| Critique checked by code | The critic answers a checklist derived from the prompt's requirements, and the code reports unmet, unanswered, and invented requirements and compares expected text itself; a non-JSON critique is a failed critique. No-key tests cover each case. |
| The critic checked | `CHECKS.md` records the second model's disagreements, what you saw in the image for each, what the open-ended critique claimed and which claims were true, and which check you would keep. |
| Reviewed PR with findings addressed | The PR exists, the reviewer's findings are on it grouped by pass, every pass-1 and pass-2 finding was fixed or answered, the gate ran before the push, and a teammate approved before the merge. |
| Understanding | You can say what a seed does, why the critique has to be checked by something other than the critic, why a PR is needed when an agent wrote the code, and what the gate catches that `REVIEW.md` cannot. |

## This week's chain stage

Deploy is stage 5 of the artifact chain, and in the chain it means a reviewed merge, not hosting. A separate reviewing agent reads the diff against `REVIEW.md`; its findings are a list for a person to check, not a verdict; the code owner approves. Team Project 1 is due the same day as this lab, with at least one reviewed pull request per team member, so this lab's PR is one of them.
