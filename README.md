# CPSC 415-01: AI Integration
## Trinity College, Fall 2026

Course materials for Ken Kousen's Fall 2026 section. Mondays 1:30 to 4:10 PM, MC-225.

**Start with the [syllabus](syllabus.md).** It has the schedule, the grading, and the working method.

Moodle holds announcements, submissions, and grades. Everything else lives here, and this repository is the current version of anything.

## What the course is

A project-based course on building software that uses commercial AI services as components: text generation, retrieval over documents, vision, image generation, and audio in the first half; tool use, the Model Context Protocol, agents, skills, and subagents in the second.

Two ideas run through the semester:

1. **You build everything with a coding agent**, in any language you choose. Python and Java are the shared starting background. Justify project language choices; one guided exercise explores an unfamiliar language.
2. **You work the way AI-native teams work.** Major projects are submitted as a chain of artifacts (intent, spec, plan, tests, pull request) alongside the code, following Anthropic's [AI-Native SDLC Playbook](https://claude.com/blog/the-ai-native-sdlc-playbook). The chain is graded as much as the code. Early labs introduce the stages gradually.

## Repository layout

| Path | What it is |
|---|---|
| `syllabus.md` | The syllabus. Source of truth for dates, grading, and policies. |
| `scripts/` | The `orclaude` launcher that points Claude Code at any OpenRouter model, plus the Windows version, a smoke test, and a settings example. Copied from the [book examples](https://github.com/kousen/claude-code-up-and-running-examples/tree/main/scripts). |
| `weeks/` | Weekly lab handouts and readings, added as the semester goes. |
| `assignments/` | Assignment sheets. The Week 1 sheet is available; project rubrics follow. |
| `slides/` | Weekly Slidev sources and PDF exports. |

## Submitting work

Major project submissions are Git repositories you own, created from the [artifact-chain template](https://github.com/kousen/artifact-chain-template). On Moodle you submit the repository URL and a git tag. Certificates from Claude Academy are uploaded as PDFs.

## Setup

**[Week 1: Start here](weeks/01/README.md)** — in-class setup, first build, behavior checks, slides, and submission instructions. No preparation beyond a laptop is assumed. Week 1 uses a minimal repository rather than the full artifact template.

[Setup guide](weeks/01/setup.md) · [Lab](weeks/01/lab.md) · [Current slides](slides/week01.md) · [Slides (PDF)](slides/week01.pdf) · [Submission](assignments/week01-first-agent-session.md)
