# A reviewing agent, and a release gate

The Deploy stage of the chain: a **separate** model reads the pull request's diff against `REVIEW.md` and reports findings by pass; a gate runs the tests and the linter before anything leaves the machine; a person approves the merge. Standard library plus the `openrouter` SDK.

| File | What it is |
|---|---|
| `review.py` | Takes the diff of the current branch against `main` (or a saved diff), `REVIEW.md`, and `spec.md`; asks a model for findings in the one-per-line form `REVIEW.md` specifies; prints them grouped by pass; exits 1 if any pass-1 or pass-2 finding exists. |
| `gate.sh` | Runs `ruff check .` and the no-key tests. Install it as a `pre-push` hook and a failing test stops the push. |
| `gate.yml` | The same two commands as a GitHub Actions workflow, for `.github/workflows/`. Make it a required check and a red build cannot merge. |
| `tests/test_review.py` | No-key tests for the parsing and the exit codes, including the fail-closed case. |

## The reviewer

```bash
pip install openrouter
cd path/to/your-repo                      # where REVIEW.md and spec.md are
git checkout week06-yourname
export OPENROUTER_API_KEY=...
python3 path/to/examples/pr-review/review.py; echo "exit $?"
```

```text
Pass 1: Must not merge (1)
  server.py:12: OPENROUTER_API_KEY is hard-coded -> read it from the environment
Pass 3: Should fix (1)
  critique.py:40: duplicated JSON extraction -> reuse extract_json
[minimax/minimax-m3 · <tokens in> in / <tokens out> out · cost <from the reply>]
exit 1
```

Options: `--diff file.patch` to review a saved diff, `--base` for a branch other than `main`, `--review` and `--spec` for the policy and spec paths, `--model` or `REVIEW_MODEL=...` for the reviewer (default `minimax/minimax-m3`; `xiaomi/mimo-v2.6-flash` gets its reasoning setting from a per-model table, see [Week 5 setup, section 2](../../weeks/05/setup.md)). `--findings saved.txt` re-parses a saved reply without a key, for tests and demonstrations.

**Exit codes.** 0: nothing in pass 1 or 2. 1: something must be fixed. 2: the reviewer did not answer in the required form, or there is no key, or the diff is over 60,000 characters (split the PR). An empty diff exits 0 with a message; there was nothing to review. A gate treats 2 as a failure: the Week 5 hook fails *open* because a broken guard should not stop the agent working, but a gate fails *closed*, because silence from the reviewer is not approval.

**Cost.** One call per run: the policy, the spec, and the diff go in; a few lines come out. A few-hundred-line diff is a few thousand tokens in. The script prints the tokens and `usage.cost` from the reply after the findings; quote that in `CHECKS.md` rather than estimating.

**The reviewer is a model.** It reads the diff you give it, not the running program, and it can be wrong in both directions: a finding that is not real, and a real problem it did not mention. Its output is a list to check, one finding at a time, against the code. A finding you disagree with gets a reply on the PR saying why; a person, not the exit code, approves the merge. That is why `REVIEW.md` is written for a reader who will point at a line, and why the four passes are ranked: pass 1 and 2 stop the merge, pass 3 and 4 are advice.

Put the findings on the PR so the reviewer who approves can see them:

```bash
python3 path/to/examples/pr-review/review.py > review.txt
gh pr comment --body-file review.txt
```

## The gate

```bash
cp path/to/examples/pr-review/gate.sh .git/hooks/pre-push && chmod +x .git/hooks/pre-push
git push            # runs ruff and the no-key tests first; a failure stops the push
```

`.git/hooks/` is not committed, so each teammate installs it (one line in `CLAUDE.md` under Commands). `gate.yml` runs the same two commands on GitHub for every pull request and is committed; copy it to `.github/workflows/gate.yml`, adjust the `pip install` line to your project, and in the repository's settings make `gate` a required status check on `main`.

The gate removes `OPENROUTER_API_KEY` from the environment before running the tests, so tests that call a model are skipped there, not billed. The billed eval is run by a person and its output goes in `CHECKS.md`. A gate that costs money or takes minutes gets turned off the first time someone is in a hurry; keep it free and fast.

## Test it without a key

```bash
python3 -m pytest tests -v
printf 'PASS 1 | a.py:3 | key in source | read from env\n' > /tmp/r.txt
python3 review.py --findings /tmp/r.txt; echo "exit $?"      # exit 1
printf 'NONE\n' > /tmp/r.txt
python3 review.py --findings /tmp/r.txt; echo "exit $?"      # exit 0
printf 'Looks fine!\n' > /tmp/r.txt
python3 review.py --findings /tmp/r.txt; echo "exit $?"      # exit 2: no findings and no NONE
```
