# Week 1: First agent session

**Due:** Monday, September 21, 2026, 1:30 PM, on Moodle.

**Category:** Participation and labs. This replaces the earlier three-language “hello-model” setup task.

Complete the [Week 1 lab](../weeks/01/lab.md). Submit your own repository URL and the tag **`week01-submitted`** in the existing Moodle Week 1 setup assignment. The assignment may still be titled “Week 1 setup smoke test.”

## At the submitted tag

Your repository should contain:

- `index.html`: the initial trainer with one deliberate improvement.
- `lyrics.txt`: the supplied text.
- `CHECKS.md`: the seven checks from the lab, with expected and observed results; include failures and corrections when they occurred.
- `README.md`: how to run it, harness/model used, your improvement, one code explanation, one example of steering or checking, usage evidence if available, and any remaining blocker.
- `.gitignore` and a history that includes a baseline commit and your subsequent work.

**No API key, password, or personal account screenshot belongs in the repository.** The trainer runs directly in a browser. It does not need a deployed site or an AI API call.

## Publish your repository

On GitHub, create a **new empty repository** named `cpsc415-week01` under your account. Choose public visibility for this supplied-text exercise. Do not initialize it with a README, license, or .gitignore; those files already exist locally. If public sharing presents a concern, speak with Ken about access before uploading.

GitHub displays the repository's HTTPS URL. In your local `lyrics-trainer` directory, use it in place of the example:

```bash
git remote add origin https://github.com/YOUR_USERNAME/cpsc415-week01.git
git push -u origin main
git push origin week01-submitted
```

Complete Git's browser sign-in if offered. A GitHub account password is not a Git HTTPS credential; ask Ken for help if Git prompts for a password rather than a supported authentication flow. Do not put a token in the repository URL. If `origin` already exists, inspect `git remote -v` before changing anything.

Open the repository in a browser. Confirm the files and `week01-submitted` tag are visible. On Moodle, submit:

```text
Repository: https://github.com/YOUR_USERNAME/cpsc415-week01
Tag: week01-submitted
```

If you discover a problem after tagging, ask Ken how to identify the corrected submission; do not silently move a tag already submitted.

## What Ken will look for

| Evidence | Satisfactory for Week 1 |
|---|---|
| Agent use | You directed a build or an honestly identified fallback, then made a change. |
| Verification | Expected and actual observations are recorded; unresolved failures are identified. |
| Understanding | You can explain your change, a relevant piece of code, and the model/harness/app distinction. |
| Submission | The files and tag can be located, with no credentials included. |

Polished graphics are not the goal. Honest evidence of a small working process matters more. This checklist guides participation feedback; it does not create a new grade category or alter the syllabus weights. Tell Ken about installation or payment blockers promptly so you can arrange a completion path.

## This week's artifact exception

Week 1 uses a minimal repository rather than the full artifact-chain template. Formal intent begins in Week 2, spec in Week 3, a written implementation plan in Week 4, automated checks in Week 5, and reviewed pull requests in Week 6. Later assignment sheets state which artifacts must be complete at submission. The team projects and final portfolio use the full chain.

Certificates and the Academic Honesty Pledge are separate Moodle submissions.
