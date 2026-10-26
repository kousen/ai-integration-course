# Lab: Generate, critique, check, review

**Time:** about 60 minutes of your own work, plus the pull-request review, which waits on a teammate. This lab is homework; the last ten minutes of class walk through it.

You will generate a set of five images from one prompt family, have a vision model critique each one against the prompt's requirements, and check the critique in plain code. Then you catch the critic being wrong. Then the sixth stage of the chain: the work goes into Team Project 1 through a branch, a pull request, a second model reviewing the diff against `REVIEW.md`, and a merge that a person approves. The Week 5 guard stays installed throughout.

Python with the OpenRouter SDK is the path the examples take. Java (or anything else) is still allowed; if you choose it, say why in `spec.md` and expect to write the two HTTP requests yourself.

## 0. Repository, SDK, and working rules (5 minutes)

Work in your Week 5 repository (`cpsc415-week05`), in a new `week06/` folder. From the root of the clone:

```bash
git pull
mkdir -p week06/tests
pip install openrouter                   # in your virtual environment; the agent may not, until spec.md names it
pip install pytest ruff                  # if not already there
echo '{"tool_name":"Bash","tool_input":{"command":"pip install openrouter"}}' | python3 .claude/hooks/guard.py
```

The last line must print "openrouter is not in spec.md"; that is the guard working, and step 1 fixes it. In `CLAUDE.md`, under **Working rules**, add:

```markdown
- Week 6: the image-set lab lives in week06/. Stages assigned: intent, spec,
  plan, tests, and (in the team repository only) a reviewed pull request.
  Commit to main here; branches and PRs are for the team repository.
- Image generation and vision calls are billed. One generation per prompt,
  one critique per image, fixed seeds. Never loop over the model inside a test.
- The critique is model output. The code compares it with the requirements;
  it does not trust it.
```

Commit (`git commit -am "Week 6 working rules"`) and start `orclaude` with the model announced in class.

## 1. Intent and spec (10 minutes)

Pick a **prompt family** your team's project needs: five prompts that vary one thing (the scene, the subject, the style) and keep the rest fixed, in the subject of Team Project 1. For each prompt, write three or four **requirements** a person could answer yes or no to by looking ("there is a robot", "the title is at the top", "no text other than the title"), and, if the prompt asks for text, the exact text expected. Then:

```text
Interview me until you can write intent/image-set.md, one question at a
time. I will generate five images from one prompt family with an image
model, send each image to a vision model with a yes/no checklist made
from that prompt's requirements, and check the answers in code. The
critique is model output and may be wrong; the program must make that
visible. Do not write code or a spec yet.
```

Correct the draft, fill in **Approved by**, commit. Then:

```text
Read intent/image-set.md and add two components to spec.md under a
"Week 6: image set" heading, each with a language decision and a model
decision. The generator calls the OpenRouter Image API through the
openrouter SDK (name it under Dependencies with the reason) with
black-forest-labs/flux.2-klein-4b as the default and one comparison
image model, and writes images/manifest.json with prompt, seed, model,
media type, and cost per image. The critic-checker sends each image and
its checklist to a vision model (name the model and the second model
used to check it), parses JSON, and compares the checklist with the
requirements in code. Number the behaviors, including: a critique that
is not JSON is a failed critique, not a crash; a requirement the critic
did not answer counts as a problem; a requirement the critic invented
counts as a problem; expected text is compared in code, not by the
critic. Do not write code.
```

Check it against the intent, correct one thing, commit `Approve spec (week 6)`. Now `pip install openrouter` passes the guard.

## 2. The plan (5 minutes)

```text
Read the Week 6 section of spec.md and add a "Week 6" section to plan.md:
files under week06/, order of work, risks, and Proof. In Proof, separate
the tests that run without an API key (the checker, the JSON extraction,
the text comparison, the comparison of two critiques) from the billed
eval (five generations and five critiques with fixed seeds), and say what
each proves and what it costs. Do not write code.
```

Ask at least two questions and correct the plan from the answers:

- "If the critic says a requirement is unmet and it is actually met, which test notices?"
- "What does one run of the eval cost, and what happens if I run it in a loop by mistake?"
- "What does the same seed guarantee, and how would I check that?"

Fill in **Approved by**, commit `Approve plan (week 6)`.

## 3. Tests first, then the code (15 minutes)

```text
Implement the Week 6 plan one step at a time. For each step write the
tests first, run them so I see them fail, then write the code and run
them again, showing me the output. You may read
../ai-integration-course/examples/image-set/ for the request shapes, but
the tests come from spec.md. Stop after each step.
```

The no-key tests cover the checker on hand-written critiques: all met; one unmet, named; one requirement missing from the reply; one requirement the critic invented; a reply that is not JSON; JSON inside prose; the text comparison (`"AI Integration"` against `"AI Integratlon"` is a mismatch). The reference tests in `examples/image-set/tests/test_checker.py` are the shape to aim for. Run `ruff check .` and record what it found.

Commit after the first green run: `git commit -m "Image set: checker with tests"`.

## 4. Generate and critique (10 minutes, about $0.15 in total)

Put your five prompts, seeds, and requirements in `week06/prompts.json` (the format is in `examples/image-set/prompts.json`). Then, with the key in your environment:

```bash
cd week06
python3 generate.py prompts.json --out images          # five FLUX images, about $0.07
python3 critique.py images/manifest.json               # five vision critiques on minimax/minimax-m3
```

Look at all five images yourself before reading the critiques, and read the titles letter by letter: image models get text wrong, and the narrow title read is there to catch it. Then read the critiques. For each image, `CHECKS.md` gets one line: cost, seconds, what the checker said (ok, or which requirement unmet, missing, or invented), and whether the title read matched. Then two more runs:

- Generate one prompt again with the same seed. Is the image identical? Look at both, then compare the files (`cmp a.jpg b.jpg`); the two answers can differ. Record both; that is what "seed" means for this model.
- Generate the same prompt with the comparison model: `--model google/gemini-3.1-flash-lite-image --out images-nb` (about $0.03–0.04, priced per image token). Record the cost from `usage.cost`, and whether it met the same requirements.

Commit: `git commit -m "Image set: five images, critiques, two image models"`. The images are small; commit them.

## 5. The critic was wrong (10 minutes)

On October 19, Prof. Kousen generated the course poster with FLUX; the title came out as "AI Integration", correctly spelled. MiniMax M3's critique said the title was misspelled "Integratlon". The generator was right and the critic was wrong, and nothing in the program would have noticed. On October 20 the same question about the same poster got "Integertion" and a complaint about a robot-human handshake that is in a different poster. The hallucination changes from run to run; the habit does not. Your job in this step is to build the thing that notices.

1. Run the critic a second time with the other class model, and compare in code:

   ```bash
   python3 critique.py images/manifest.json --model xiaomi/mimo-v2.6-flash --out critique-mimo.json
   python3 critique.py --compare critique.json critique-mimo.json
   ```

   For every disagreement, open the image and decide who was right. Record each one in `CHECKS.md`: the requirement, what each model said, what you saw.

2. Ask one model for an open-ended critique of one image, the way the October 19 demo did (in your own terminal, not through the agent, so the hook and the spec stay out of it): *"Critique this poster. What is wrong with it?"* Compare what it claims with the checklist verdicts, the narrow title read, and your eyes. Record what it claimed and which claims were true.

3. Write three sentences in `CHECKS.md`: which of the three checks (second model, narrow question compared in code, a person looking) caught something the others did not, and which one you would put in Team Project 1's critique path.

If both models agreed on everything and the open-ended critique was entirely right, say so; that is a result too, and the question in part 3 still has an answer.

Commit: `git commit -m "Image set: the critic checked"`.

## 6. The Deploy stage: a reviewed pull request (20–30 minutes, plus waiting for a teammate)

"Deploy" in the chain means a reviewed merge, not hosting; hosting is Week 7. In the **team repository**, on a branch of your own, add the piece of this lab that Team Project 1 needs: your image set and manifest, and the change that wires the generator or the checklist critique into the app (your team's `plan.md` says which piece is yours; if a teammate's PR already merged the generator, build on it, don't add a second copy). The Week 5 guard must be installed there too. The team repository also needs a `requirements.txt` with `openrouter` in it (and whatever else the team's `spec.md` names): the spec is where a dependency is justified, the requirements file is where the machine reads it, and `gate.yml` installs from that file, so a repository without one fails its first pull request.

```bash
cd path/to/team-repo
git checkout main && git pull
git checkout -b week06-<yourname>
cp path/to/ai-integration-course/examples/pr-review/gate.sh .git/hooks/pre-push && chmod +x .git/hooks/pre-push
# ... the work, through the agent, tests first, as in step 3 ...
git add . && git commit -m "Image set for <feature>, with checklist critique"
git push -u origin week06-<yourname>        # the gate runs first: ruff and the no-key tests
gh pr create --base main --fill
```

If the push stops at the gate, fix what it found; do not delete the hook. Then the reviewing agent, from the team repository's root, where `REVIEW.md` and `spec.md` live:

```bash
python3 path/to/ai-integration-course/examples/pr-review/review.py > review.txt; echo "exit $?"
cat review.txt
gh pr comment --body-file review.txt
```

Exit 1 means a pass-1 or pass-2 finding. Read each finding against the code, because the reviewer is a second model and can be wrong the way the critic was in step 5. Fix the real ones, through the agent, commit, push, run the reviewer again until it exits 0. A finding you disagree with gets a reply on the PR saying why. A teammate reads the PR (the diff, the findings, your replies) and approves it on GitHub; then:

```bash
gh pr merge --merge
```

In your Week 5 repository, `week06/CHECKS.md` gets a **Review** section: the PR URL, the reviewer's findings grouped by pass, what you fixed, what you pushed back on, the exit code of the last run, and who approved. Then:

```bash
cd path/to/cpsc415-week05
git add . && git commit -m "Image set: reviewed PR into Team Project 1"
git tag week06-submitted
git push origin main week06-submitted
```

## If you finish early

- Before opening the PR, plant a pass-1 problem on purpose (a fake key string in a comment, or a test marked `skip`), run the reviewer, and see whether it finds it. Remove it before you push. Record the result.
- Copy `examples/pr-review/gate.yml` to `.github/workflows/gate.yml` in the team repository and make it a required check on `main`.
- Try the comparison image model through the chat endpoint instead of the Image API (`client.chat.send(..., modalities=["image", "text"])`) and note what differs in the reply.

## If you are blocked

Say so early. The usual problems: the guard refusing `pip install openrouter` (step 1 fixes that: the spec names it first), a critique that is prose with JSON inside (the extractor handles it; a critique with no JSON at all is a failed critique and is counted), a reviewer that exits 2 (it did not answer in the required form; run it again and read the raw reply it printed), and `gh pr create` on `main` (make the branch first). A teammate who is not available to approve is a reason to open the PR now and merge later; the submission is the PR URL, and the merge can follow.
