# Week 2: Working with a coding agent; text generation fundamentals

**Monday, September 21, 2026 · 1:30–4:10 PM · MC-225**

Last week the coding agent called a model and your app did not. This week your own program makes the call. You will also write the first artifact in the chain, an intent file, before the agent builds anything.

By the end of the session, you should be able to:

- Describe what the harness sends to a model on each turn and why later turns cost more.
- Use `CLAUDE.md`, plan mode, and a fresh session deliberately.
- Read a chat API request and response: roles, system prompt, parameters, token usage.
- Point the same client at a hosted model and at a local one, and say what changed.
- Run a discovery interview that ends in an intent file you approved.

## Today's materials

1. [Setup additions: a language runtime and an optional local model](setup.md)
2. [Lab: Interview, intent, and a chat client](lab.md)
3. [Week 2 slides (PDF)](../../slides/week02.pdf) · [Slide source](../../slides/week02.md)
4. [Submission requirements](../../assignments/week02-chat-client.md)
5. [Intent template](https://github.com/kousen/artifact-chain-template/blob/main/intent/TEMPLATE.md) from the artifact-chain template

## Our afternoon

| Time | Activity |
|---|---|
| 1:30–1:40 | Where we are: a look at Week 1 results |
| 1:40–2:05 | Inside the harness: loop, tools, permissions, context, `CLAUDE.md`, plan mode |
| 2:05–2:25 | Vocabulary from last week: parameters, open weights, context window |
| 2:25–2:45 | The API call itself: request, response, usage |
| 2:55–3:10 | Chain stage 1: the discovery interview and `intent.md` |
| 3:10–3:45 | Lab: interview, intent, build |
| 3:45–4:00 | Lab: verify the call, swap the model |
| 4:00–4:10 | Save, tag, and preview Week 3 |

Prof. Kousen will choose the break time based on how the class is progressing.

## Due today at 1:30 PM

The Week 1 submission (repository URL and `week01-submitted` tag), the Claude Code 101 certificate, and the Academic Honesty Pledge, all on Moodle.

## After class

**Due Monday, September 28, at 1:30 PM:** the [Week 2 submission](../../assignments/week02-chat-client.md) and the **[AI Fluency for Students](https://academy.claude.com/courses/ai-fluency-for-students)** certificate (the syllabus also accepts Trinity's AI Literacy for All badge).

### Reading to support the work

- [OpenRouter quickstart](https://openrouter.ai/docs/quickstart): the request shape your client sends.
- [Ollama's OpenAI compatibility](https://docs.ollama.com/openai): the same request shape at a local address.
- [The AI-Native SDLC Playbook](https://claude.com/blog/the-ai-native-sdlc-playbook): the Plan stage is this week's chain stage.
- Prof. Kousen will share the harness and context chapters of his draft book through Moodle.

## What comes next

Week 3 turns an approved intent into a specification, adds structured output and a small evaluation suite, and forms teams. Team Project 1 and the individual portfolio intent are assigned then.
