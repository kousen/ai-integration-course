# CPSC 415-01: AI Integration
## Trinity College, Fall 2026

Course materials for Ken Kousen's Fall 2026 section. Mondays 1:30 to 4:10 PM, MC-225.

**Start with the [syllabus](syllabus.md).** It has the schedule, the grading, and the working method.

Moodle holds announcements, submissions, and grades. Everything else lives here, and this repository is the current version of anything.

## What the course is

A project-based course on building software that uses commercial AI services as components: text generation, retrieval over documents, vision, image generation, and audio in the first half; tool use, the Model Context Protocol, agents, skills, and subagents in the second.

Two ideas run through the semester:

1. **You build everything with a coding agent**, in any language you choose. Java is the shared baseline from CPSC 215; anything else counts as new, and your portfolio must include at least one component in a language you had never used.
2. **You work the way AI-native teams work.** Every assignment is submitted as a chain of artifacts (intent, spec, plan, tests, pull request) alongside the code, following Anthropic's [AI-Native SDLC Playbook](https://claude.com/blog/the-ai-native-sdlc-playbook). The chain is graded as much as the code.

## Repository layout

| Path | What it is |
|---|---|
| `syllabus.md` | The syllabus. Source of truth for dates, grading, and policies. |
| `scripts/` | The `orclaude` launcher that points Claude Code at any OpenRouter model, plus the Windows version, a smoke test, and a settings example. Copied from the [book examples](https://github.com/kousen/claude-code-up-and-running-examples/tree/main/scripts). |
| `weeks/` | Weekly lab handouts and readings, added as the semester goes. |
| `assignments/` | Assignment sheets and the artifact-chain rubric. |

## Submitting work

Every submission is a Git repository you own, created from the [artifact-chain template](https://github.com/kousen/artifact-chain-template). On Moodle you submit the repository URL and a git tag. Certificates from Claude Academy are uploaded as PDFs.

## Setup

The Week 1 setup checklist will live in `weeks/01/`. Short version: Git and GitHub, VS Code, an OpenRouter account with a spend limit on the key, Claude Code, and the launcher in `scripts/`.
