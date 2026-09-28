# Lab: Ask the course

**Time:** about 45 minutes. Start when Prof. Kousen finishes the server demonstration.

You will build a program that answers questions about this course from the course's own pages, cites the pages it used, and says so when the pages don't contain the answer. The agent writes the code. You approve the intent and the spec, and this week, for the first time, you approve a **plan** before any code is written.

## 0. Repository and conventions (5 minutes)

Create `cpsc415-week04` from [kousen/artifact-chain-template](https://github.com/kousen/artifact-chain-template) with **Use this template**, make it public, and clone it beside last week's folder. In `CLAUDE.md`, under **Working rules**, add:

```markdown
- This is the Week 4 introductory lab. Stages assigned: intent, spec, and plan.
  No branches or pull requests yet. Commit to main.
- Libraries and build tools are allowed (pip or uv, Gradle or Maven). Name
  each dependency in spec.md with the reason for it. A RAG framework such as
  LangChain, LangChain4j, or Spring AI is fine, but the program must print
  the chunks it retrieved and their scores for every answer.
- The documents are the course repository at ../ai-integration-course:
  syllabus.md, assignments/, and weeks/01 through weeks/03 (the course as it
  stood before this lab). Skip weeks/04. Never copy the pages into this repo.
```

Start `orclaude` in this folder with the model announced in class.

## 1. Intent and spec, briefly (10 minutes)

The task is given, so the interview is short:

```text
Interview me until you can write intent/ask-the-course.md, one question
at a time. The program answers a question about CPSC 415 using only the
course's Markdown pages, cites which pages it used, and replies "I can't
find that in the course documents" when they don't contain the answer.
Do not write code or a spec yet.
```

Correct the draft, fill in **Approved by**, commit. Then:

```text
Read intent/ask-the-course.md and write spec.md from the template. Two
components: an indexer (split pages into chunks, embed them, save a JSON
index) and an asker (embed the question, find the closest chunks, answer
from them with citations). Each component needs its language and model
decisions; the indexer's model is an embedding model. List the
libraries under Dependencies with the reason for each. Number the
behaviors, including the "can't find that" case and printing the
retrieved chunks with their scores. Do not write code.
```

Check it against the intent, correct one thing, commit `Approve spec`.

## 2. The plan (10 minutes)

This is the new chain stage.

```text
Read spec.md and write plan.md from the template: the files you will
create, the order you will build them in, the risks, and the proof that
each step worked. Do not write code.
```

Then question it before you approve it. Ask at least two of these and correct `plan.md` from the answers:

- "What could break in step N, and how would I notice?"
- "How big is one chunk, and why that size?"
- "What does the proof step actually run, and what output means it worked?"
- "What happens when two pages disagree?"
- "Why this library, and what does it do that we'd otherwise write ourselves?"

The **Proof** section must include the five-question eval from step 3. Fill in **Approved by** and commit: `git commit -m "Approve plan"`.

## 3. Build from the plan (15 minutes)

```text
Implement plan.md, step by step. Stop after each step and show me its
proof before starting the next.
```

Write five questions in `questions.json` yourself:

1. Three with a clear answer in one place, such as a due date, a grade weight, and a lab step.
2. One whose answer is spread across two pages, such as the late-day policy.
3. One the course pages cannot answer. The expected answer is "I can't find that in the course documents."

Run the eval with retrieval, then without it (no excerpts in the prompt). Record both in `CHECKS.md`: questions passed, which failed and why, and the chunk sources printed for any failure.

## 4. A stale page (5 minutes)

Ask your program:

```text
Which Xiaomi MiMo model does this course use as the fallback or second model?
```

Two of the pages you indexed give different answers, because the model changed on September 28 and the older page was not edited. Record what your program answered, which chunks it cited, and one way a RAG system could prefer the current page. You do not need to implement the fix.

## 5. Explain and save (5 minutes)

`README.md` should have:

- How to build the index and ask a question, with the environment variables.
- Your five questions and what each is there to catch.
- The with-retrieval and without-retrieval results, and one sentence on the difference.
- Your stale-page finding.
- One line of code you can explain: where the chunks are ranked, or where the model is told to refuse.

```bash
git add .
git commit -m "Ask-the-course bot with five-question eval"
git tag week04-submitted
git push -u origin main
git push origin week04-submitted
```

## If you finish early

- Try a free embedding model and see whether the same questions pass.
- Add the file's last-changed date to each chunk and tell the model to prefer the newest when excerpts disagree. Does step 4's answer change?
- If you used a framework, build the retrieval step by hand (cosine similarity is four lines) and compare the chunks it picks. If you built it by hand, try a framework from [RAGDEMO](https://github.com/kousen/ragdemo).

## If you are blocked

Say so early. The usual problems are an index built from the wrong folder (the chunk count will be tiny) and a spec that tries to put every page in the prompt, which is exactly what RAG avoids.
