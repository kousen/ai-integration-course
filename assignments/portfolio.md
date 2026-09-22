# Individual Portfolio: AI-Enabled Profile Site

**Assigned:** Monday, September 28, 2026. **Final due:** Monday, December 14, 2026, 1:30 PM. **Weight:** 25% of the course grade, plus the Comprehension Defense (15%) is conducted over this repository.

**First milestone: `intent/` and `spec.md` due Monday, October 5, 1:30 PM**, submitted on Moodle as the repository URL plus the tag `intent-spec` (feedback only, not graded). The final submission is the repository URL, the tag `portfolio-final`, and the deployed site's URL.

## What this is

A personal website with a chatbot that answers one question from a visitor: *should we work together?* The chatbot answers only from a profile you wrote, and it **refuses to fabricate**. If a recruiter asks about a skill you have never shipped, the honest answer is that you have listed it as something you are learning. A chatbot that confidently claims expertise you do not have is worse than no chatbot, and the test set checks for exactly that.

The site is the smallest deliverable. The profile, the grounding prompt, and the adversarial test set are the work.

## Deliverables, all in one public repository

1. **A structured profile** (JSON or YAML): projects, skills, learning goals. Each project carries the four-question annotation.
2. **A "not yet" inventory**: skills and tools you have deliberately not prioritized, with a sentence on why.
3. **A grounding system prompt** that makes the chatbot answer only from the profile, hedge or decline outside it, and distinguish shipped work from aspirational learning.
4. **An adversarial test set** of at least ten questions the chatbot must handle, covering at least: a skill you do not have; a comparative question ("better than a bootcamp grad?"); flattery bait; a leading question with a false premise; an out-of-scope personal question. Recorded results, with failures you found even if unresolved.
5. **The site**, deployed, with the chatbot working.

Plus the artifact chain: `intent/`, `spec.md`, `plan.md`, tests, reviewed pull requests, `ANNOTATION.md`, current `CLAUDE.md`.

## The four-question annotation

Every project in the profile answers: **What is this?** **Why this choice?** **What breaks?** **What did I learn?** The Comprehension Defense asks these same four questions about components of your choice and the instructor's.

## Milestones

| Date | Milestone |
|---|---|
| October 5 (Week 4) | Tag `intent-spec`: `intent/` approved by you; `spec.md` with the profile schema, the "not yet" inventory, and language and model decisions |
| October 19 (Week 5) | `plan.md`; profile drafted |
| November 2 (Week 7) | Chatbot answering from the profile; Week 7 lab adds a spoken interface |
| November 30 (Week 11) | Adversarial test set run; site deployed |
| December 14 (Week 13) | Tag `portfolio-final` and the deployed URL; Comprehension Defense during finals week, December 17–23 |

Milestones are checked in class with feedback.

## Reference implementation

Prof. Kousen's own site is built this way: [github.com/kousen/kousenit](https://github.com/kousen/kousenit), a Hugo site on Cloudflare Pages with the chatbot in `functions/api/`. Read it for the shape of the grounding prompt and the test set. Do not copy the stack unless it is the right one for you; the stack is not the lesson. Spring AI with a static site, Python with FastAPI, or a client-side page calling an API through a small serverless function all work.

## Rules

- The profile is a record of shipped work. Aspirational items go in "not yet."
- The chatbot must refuse to fabricate. This is graded.
- Language and model decisions are in `spec.md` with alternatives named. A cheap model compared against a stronger one on your own test set is expected.
- No API key in the repository. The deployed chatbot's key lives in the host's secret store.

## What Prof. Kousen will look for

| Evidence | Weight |
|---|---|
| Profile honesty and specificity; the four questions answered | 30% |
| "Not yet" inventory: real self-awareness, not a token entry | 15% |
| Grounding prompt: enforces the discipline; shipped vs. learning distinguished | 20% |
| Adversarial test set: coverage, difficulty, and results, with failures acknowledged | 25% |
| Site: deployed, working, accessible | 10% |

The artifact chain is required for full credit on every row.
