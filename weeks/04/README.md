# Week 4: Retrieval-augmented generation, and the plan

**Monday, October 5, 2026 · 1:30–4:10 PM · MC-225**

A model can only answer from what it was trained on or what you put in the prompt. This week you build the second option: split documents into chunks, turn each chunk into an embedding, and at question time send the model only the few chunks closest to the question. The documents are this course's own pages, so every answer can be checked. You also write the third artifact in the chain, `plan.md`, and see how a web app keeps its API key off the browser, which Team Project 1 needs.

By the end of the session, you should be able to:

- Explain what an embedding is and how similarity search picks the chunks sent to the model.
- Build a small RAG program, by hand or with a framework: index, retrieve, answer with citations, or say it can't find the answer.
- Evaluate it with five questions, including one the documents cannot answer, and compare it with no retrieval at all.
- Use a package manager and a build tool, and justify each dependency in the spec.
- Say when RAG helps and when it hurts, including stale or conflicting documents.
- Write and question a `plan.md` before any code is written.
- Describe how a server holds an API key so the browser never sees it.

## Today's materials

1. [Setup additions](setup.md): pull the course repo, one embeddings check, and a video to watch
2. [Lab: Ask the course](lab.md)
3. [REST in one page](rest.md): the handout promised on September 28
4. [Week 4 slides (PDF)](../../slides/week04.pdf) · [Slide source](../../slides/week04.md)
5. [Week 4 submission requirements](../../assignments/week04-rag-plan.md)
6. [Keeping the key on the server](../../examples/key-on-server/): Python and Java examples for Team Project 1
7. [Plan template](https://github.com/kousen/artifact-chain-template/blob/main/plan.md) from the artifact-chain template

## Our afternoon

| Time | Activity |
|---|---|
| 1:30–1:40 | Where we are: Week 3 results, teams, a worked spec example |
| 1:40–1:55 | REST in one page |
| 1:55–2:25 | Retrieval-augmented generation: embeddings, retrieval, evaluation, stale documents |
| 2:25–2:45 | Chain stage 3: `plan.md` |
| 2:55–3:10 | Keeping the key on the server |
| 3:10–3:55 | Lab: ask the course |
| 3:55–4:10 | Save, tag, what is due |

Prof. Kousen will choose the break time based on how the class is progressing.

## Due today at 1:30 PM

- The [Week 3 submission](../../assignments/week03-structured-output.md) (repository URL and `week03-submitted` tag).
- Your portfolio `intent/` and `spec.md`, tagged `intent-spec` ([portfolio sheet](../../assignments/portfolio.md)). Feedback only.
- Your team's Team Project 1 intent, committed in the team repository ([TP1 sheet](../../assignments/team-project-1.md)). Feedback only.

## After class

**Due Monday, October 19, at 1:30 PM** (there is no class October 12, Trinity Days):

- The [Week 4 submission](../../assignments/week04-rag-plan.md).
- Team Project 1: `spec.md` and `plan.md` in the team repository.

### Reading and viewing to support the work

- Prof. Kousen's video [Retrieval-Augmented Generation](https://youtu.be/3kMwv7Kraxk): the same flow in LangChain (Python), LangChain4j, and Spring AI, with code at [github.com/kousen/RAGDEMO](https://github.com/kousen/RAGDEMO). Watch it before class if you can.
- [OpenRouter embeddings](https://openrouter.ai/docs/api/reference/embeddings): the endpoint the lab uses, with your existing key.
- [The AI-Native SDLC Playbook](https://claude.com/blog/the-ai-native-sdlc-playbook): the Build stage is this week's chain stage.

## What comes next

Week 5 (October 19) is vision models and the Test stage: agent-written tests and browser-driven checks.
