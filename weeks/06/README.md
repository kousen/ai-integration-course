# Week 6: Image generation, and the review

**Monday, October 26, 2026 · 1:30–4:10 PM · MC-225**

This week your program makes pictures. An image model takes a prompt and returns an image, through a different endpoint with a different request shape from chat, the way embeddings had their own endpoint in Week 4. Then the Week 5 pattern runs the other way: a vision model critiques the image your program generated, and the code checks the critique against what the prompt asked for, because a critique is model output too and can be confidently wrong. You also reach the fifth stage of the chain, Deploy, which in the chain means a reviewed merge: a branch, a pull request, a separate model reviewing the diff against `REVIEW.md`, and a gate that blocks a push when the tests fail. The lab is homework this week; class is teaching and demonstrations.

By the end of the session, you should be able to:

- Generate an image through OpenRouter's Image API, say what one image costs, and say what a seed does.
- Show the same call as a raw HTTP request and as an SDK call, and say what the SDK adds and what it hides.
- Say what prompt and style controls an image model gives you, and what provenance a generated image carries.
- Build the loop: the model generates, a model critiques against a checklist, the code checks the critique, and a second model or a person checks the critic.
- Explain why a pull request is still needed when an agent wrote the code.
- Run a reviewing model against `REVIEW.md`, read its findings by pass, and tell a real finding from a wrong one.
- Install a release gate (a pre-push hook or a CI workflow) and say what it does that `REVIEW.md` cannot.

## Today's materials

1. [Setup additions](setup.md): the `openrouter` SDK, one image, the GitHub CLI
2. [Lab: Generate, critique, check, review](lab.md) (homework, due November 2)
3. [Week 6 slides (PDF)](../../slides/week06.pdf) · [Slide source](../../slides/week06.md)
4. [Week 6 submission requirements](../../assignments/week06-image-review.md)
5. [The image-set example](../../examples/image-set/): `generate.py`, `critique.py`, the checker tests, a prompt file
6. [The reviewer and the gate](../../examples/pr-review/): `review.py`, `gate.sh`, `gate.yml`, how to test them
7. [`REVIEW.md` in the template](https://github.com/kousen/artifact-chain-template/blob/main/REVIEW.md): the four passes the reviewer implements

## Our afternoon

| Time | Activity |
|---|---|
| 1:30–1:40 | Where we are: Week 5 results, Team Project 1's Test milestone, what is due November 2 |
| 1:40–2:20 | Image generation: the Image API, SDK beside raw HTTP, cost and seeds, prompt and style control, provenance |
| 2:20–2:45 | Generate, critique, check: the loop, and the day the critic was wrong |
| 2:45–3:00 | Break |
| 3:00–3:30 | Chain stage 5, Deploy: why a PR, the four passes, the reviewer as a second model |
| 3:30–3:50 | Release gates: hooks, pre-push, CI; Team Project 1 presentation logistics |
| 3:50–4:00 | Lab sheet walkthrough |
| 4:00–4:10 | What is due, questions |

Prof. Kousen may move the break depending on how the demonstrations go.

## Due today at 1:30 PM

- The [Week 5 submission](../../assignments/week05-vision-tests.md) (repository URL and `week05-submitted` tag).
- Team Project 1, Test stage: agent-written tests that run and a browser-driven check of the front end ([TP1 sheet](../../assignments/team-project-1.md)). Feedback only.

## After class

**Due Monday, November 2, at 1:30 PM:**

- The [Week 6 submission](../../assignments/week06-image-review.md): the lab, the PR URL in the team repository, and the `week06-submitted` tag.
- **Team Project 1**, complete, with presentations in class ([TP1 sheet](../../assignments/team-project-1.md)).

**Assigned today:** the [AI-Native SDLC Playbook](https://academy.claude.com/courses/ai-native-sdlc-playbook) course on Claude Academy. Certificate due **Monday, November 9**, uploaded to Moodle. You have now worked every stage it describes; the course gives them their names.

### Reading and viewing to support the work

- [OpenRouter: image generation](https://openrouter.ai/docs/features/multimodal/image-generation): the Image API the lab calls, and the chat-completions form with `modalities`.
- [OpenRouter Python SDK on PyPI](https://pypi.org/project/openrouter/): `pip install openrouter`; the class examples use `client.images.generate` and `client.chat.send`.
- [GitHub CLI manual: `gh pr`](https://cli.github.com/manual/gh_pr): create, comment, merge.
- [Claude Code hooks](https://code.claude.com/docs/en/hooks) and [Git hooks](https://git-scm.com/docs/githooks): the two kinds of hook in this week's gate; Chapter 6 of *Claude Code: Up and Running* covers the first.
- [The AI-Native SDLC Playbook](https://claude.com/blog/the-ai-native-sdlc-playbook): the Deploy stage, and the course assigned today.

## What comes next

Week 7 (November 2) is Team Project 1 presentations, then audio: speech-to-text and text-to-speech, and a spoken interface for the portfolio chatbot.
