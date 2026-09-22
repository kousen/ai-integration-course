# Week 3: Structured output, evaluation, and the specification

**Monday, September 28, 2026 · 1:30–4:10 PM · MC-225**

Last week your program asked a model a question and printed a sentence. This week it asks for data, checks the data against five known cases, and does that against two models so the comparison is written down. You also write the second artifact in the chain, `spec.md`, and teams form.

By the end of the session, you should be able to:

- Ask a model for JSON and handle the reply when it is not JSON.
- Write a five-case regression eval and say what each case is there to catch, including a case that should produce "unknown."
- Compare two models on the same eval and record the result as an observation.
- Turn an approved intent into a `spec.md` with a language decision and a model decision per component.
- Name your team and your team's working conventions.

## Today's materials

1. [Setup additions](setup.md): nothing new to install; one check
2. [Lab: A structured-output client with a five-case eval](lab.md)
3. [Week 3 slides (PDF)](../../slides/week03.pdf) · [Slide source](../../slides/week03.md)
4. [Week 3 submission requirements](../../assignments/week03-structured-output.md)
5. Assigned today: [Team Project 1](../../assignments/team-project-1.md) and the [Individual Portfolio](../../assignments/portfolio.md)
6. [Spec template](https://github.com/kousen/artifact-chain-template/blob/main/spec.md) from the artifact-chain template

## Our afternoon

| Time | Activity |
|---|---|
| 1:30–1:40 | Where we are: Week 2 results; Enterprise seats status |
| 1:40–1:50 | Carried over: the same client against a local model |
| 1:50–2:10 | Prompt patterns and structured output |
| 2:10–2:25 | Evaluation: five cases, hallucination, refusal |
| 2:25–2:45 | Chain stage 2: from intent to `spec.md` |
| 2:55–3:10 | Teams form; Team Project 1 and the Portfolio |
| 3:10–3:55 | Lab: spec, client, eval, second model |
| 3:55–4:10 | Save, tag, what is due |

Prof. Kousen will choose the break time based on how the class is progressing.

## Due today at 1:30 PM

The Week 2 submission (repository URL and `week02-submitted` tag) and the AI Fluency for Students certificate, on Moodle.

## After class

**Due Monday, October 5, at 1:30 PM:** the [Week 3 submission](../../assignments/week03-structured-output.md) and the individual portfolio's `intent/` and `spec.md` ([portfolio sheet](../../assignments/portfolio.md)).

**Due Monday, November 2:** [Team Project 1](../../assignments/team-project-1.md), with a team intent due October 5.

### Reading to support the work

- [The AI-Native SDLC Playbook](https://claude.com/blog/the-ai-native-sdlc-playbook): the Design stage is this week's chain stage.
- [OpenRouter: structured outputs](https://openrouter.ai/docs/features/structured-outputs): the optional `response_format` parameter, and which models honor it.
- Prof. Kousen will share the structured-output and evaluation chapters of his draft book through Moodle.

## What comes next

Week 4 is retrieval-augmented generation and the third chain artifact, `plan.md`. Bring your team's intent.
