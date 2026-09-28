# Week 4: Ask the course (RAG) and the plan

**Due:** Monday, October 19, 2026, 1:30 PM, on Moodle. (No class October 12, Trinity Days.)

**Category:** Participation and labs.

Complete the [Week 4 lab](../weeks/04/lab.md). Submit your repository URL and the tag **`week04-submitted`** in the Moodle Week 4 assignment.

## At the submitted tag

Your repository, created from the artifact-chain template, should contain:

- `intent/ask-the-course.md`, approved by you.
- `spec.md` with two components, indexer and asker, each with a language decision and a model decision (the indexer's is an embedding model), and numbered behaviors including the "can't find that" case.
- `plan.md` with files, order, risks, and proof, approved by you **before** the first code commit. The commit history should show it.
- The indexer and the asker, in any language, with libraries and build tools as you choose. Each dependency is named in `spec.md` with its reason. The program prints the retrieved chunks and their scores. The course pages are read from your clone of the course repository, not copied in.
- `questions.json` with five questions: three with one clear answer, one spread across pages, one the pages cannot answer.
- `CHECKS.md` with the eval run with retrieval and without it, and the stale-page finding from step 4.
- `README.md` as the lab describes.

**No API key in the repository.** The index file may be large; commit it or add it to `.gitignore` and say in the README how to rebuild it.

## What Prof. Kousen will look for

| Evidence | Satisfactory for Week 4 |
|---|---|
| Plan | `plan.md` was approved before code, shows at least two questions you asked of it, and its Proof section names the eval. |
| Retrieval | Answers come from retrieved chunks, which the program prints with their scores; the unanswerable question gets "I can't find that." |
| Evaluation | Five questions run with and without retrieval; the difference is recorded as an observation. |
| Judgment | The stale-page finding says what the program answered, which chunks misled it, and one way to prefer the current page. |
| Understanding | You can explain how chunks are ranked and why the model is told to refuse. |

## This week's chain stage

The plan is stage 3 of the artifact chain: the agent proposes files, order, risks, and proof, and you question it before any code exists. Week 5 adds automated tests, Week 6 reviewed pull requests. Team Project 1's `spec.md` and `plan.md` are due the same day as this lab.
