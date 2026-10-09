# Week 5: Vision models, and the tests

**Monday, October 19, 2026 · 1:30–4:10 PM · MC-225**

The models you have been calling since Week 2 can also read images. This week your program sends a photograph of a receipt and gets back JSON, the same structured output as Week 3 with an image in the prompt. The model reads; your code checks that the numbers add up, because a vision model returns plausible numbers, not guaranteed ones. You also reach the fourth stage of the chain: the agent writes the tests, runs them, and you confirm the loop actually ran. A hook, a program Claude Code runs before every tool call, keeps the agent from "fixing" a failing test by editing the answer key. For Team Project 1, the same stage needs a browser-driven check of the web front end.

By the end of the session, you should be able to:

- Send an image to a model through the same chat endpoint, and say what it costs.
- Say what vision models read well, where they guess, and why the code has to check the arithmetic.
- Get structured JSON from an image and validate it before anything downstream uses it.
- Ask the agent for tests before code, and tell a test that proves something from one that passes for the wrong reason.
- Show that the feedback loop ran: the failing run, the fix, the passing run, in the output and in the commit history.
- Install a hook that blocks destructive commands, unapproved packages, and edits to protected files, and test it.
- Describe what a browser-driven check (Playwright) sees that a unit test cannot.

## Today's materials

1. [Setup additions](setup.md): pull the course repo, one vision check, Playwright for Team Project 1
2. [Lab: Receipts to data](lab.md)
3. [Week 5 slides (PDF)](../../slides/week05.pdf) · [Slide source](../../slides/week05.md)
4. [Week 5 submission requirements](../../assignments/week05-vision-tests.md)
5. [The receipt images and answer key](images/) used in the lab
6. [The guardrail hook](../../examples/guardrail-hook/): `guard.py`, `settings.json`, how to test it
7. [The browser check](../../examples/key-on-server/test_browser.py) for the key-on-server page, which Team Project 1 adapts

## Our afternoon

| Time | Activity |
|---|---|
| 1:30–1:40 | Where we are: Week 4, team specs and plans, what is due |
| 1:40–2:15 | Vision models: how an image goes in, what comes back, what to trust |
| 2:15–2:40 | Chain stage 4: the tests, and proving the loop ran |
| 2:55–3:10 | Hooks as guardrails |
| 3:10–3:20 | A browser-driven check |
| 3:20–4:00 | Lab: receipts to data |
| 4:00–4:10 | Save, tag, what is due |

Prof. Kousen will choose the break time based on how the class is progressing.

## Due today at 1:30 PM

- The [Week 4 submission](../../assignments/week04-rag-plan.md) (repository URL and `week04-submitted` tag).
- Team Project 1: `spec.md` and `plan.md` in the team repository, the plan naming the deployment target ([TP1 sheet](../../assignments/team-project-1.md)). Feedback only.
- Your portfolio `plan.md` with the profile drafted ([portfolio sheet](../../assignments/portfolio.md)). Feedback only.

## After class

**Due Monday, October 26, at 1:30 PM:**

- The [Week 5 submission](../../assignments/week05-vision-tests.md).
- Team Project 1, Test stage: agent-written tests that run, and a browser-driven check of the front end.

### Reading and viewing to support the work

- [OpenRouter: images and multimodal requests](https://openrouter.ai/docs/features/multimodal/images): the `image_url` content part the lab uses, with your existing key.
- [Playwright for Python](https://playwright.dev/python/docs/intro) or [for Node](https://playwright.dev/docs/intro): the browser check for Team Project 1.
- [Claude Code hooks](https://code.claude.com/docs/en/hooks): the mechanism behind the guard. Chapter 6 of *Claude Code: Up and Running* covers the same ground.
- [The AI-Native SDLC Playbook](https://claude.com/blog/the-ai-native-sdlc-playbook): the Test stage is this week's chain stage.

## What comes next

Week 6 (October 26, mid-term) is image generation and the Deploy stage: pull requests reviewed by a separate agent against `REVIEW.md`.
