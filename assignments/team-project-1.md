# Team Project 1: Multimodal Web App

**Assigned:** Monday, September 28, 2026. **Due:** Monday, November 2, 2026, 1:30 PM, on Moodle (group submission). Presentations in class that day.

**Weight:** 15% of the course grade. Teams of 2–3.

## What to build

A web application that **generates images, displays them, and critiques them**, with **at least one other modality**: vision (the app reads images) or audio (the app listens or speaks). The subject is your choice. Examples that fit: a study-card generator that draws a diagram for a concept and has a second model check the diagram against the concept; a product-mockup tool that generates variations and scores them against a brief; a "describe, draw, compare" loop where the app photographs an object, generates a version from the description, and reports the differences.

Every team member must be able to explain every part of the submission. That is checked in the presentation and again in the Comprehension Defense.

## The chain is the submission

This project is submitted as a full artifact chain. Working code with no chain, or a chain the team cannot explain, earns at most half credit.

| Stage | Artifact | Due |
|---|---|---|
| Plan | `intent/*.md`, one per major feature, each approved by a named team member | Team intent: **October 5** (feedback only) |
| Design | `spec.md` with two decisions per component: **language** and **model**, each with the alternative considered | October 19 (Week 5), with the plan |
| Build | `plan.md`: files, order, risks, proof | October 19 |
| Test | Agent-written tests that run; a browser-driven check for the web front end | October 26 |
| Deploy | At least one reviewed pull request per team member, with a `REVIEW.md` pass from a separate reviewing agent | October 26 (Week 6 lab wires the image set in via a reviewed PR) |
| Maintain | `CLAUDE.md` current; `ANNOTATION.md` with the four questions for each component | November 2 |

Milestones before November 2 are checked in class and get feedback, not grades.

## The four-question annotation

For each component, `ANNOTATION.md` answers: What is this? Why this choice? What breaks? What did I learn? Plain statements, not marketing copy. "What did I learn" includes at least one place the agent gave confidently wrong output that you corrected.

## Rules

- Languages are your choice and are justified in `spec.md`. Java and Python are both fine; so are others if the team can explain the code.
- Models are your choice and are justified in `spec.md`, with a cheap model compared against a stronger one on a real task from the project.
- No images of real people. Generated media carries provenance metadata where the API supports it. Everything in the syllabus's Responsible AI section applies.
- API keys stay in the environment. A key in any commit is treated as compromised.
- Cost: keep a running total from your providers' usage pages in `README.md`. There is no fixed cap, but a project that costs more than about $20 in total should say why.

## Presentation (Week 7)

Ten minutes per team: the app running live, one artifact from the chain shown on screen, one thing that broke and what you did about it. Followed by peer critique.

## What Prof. Kousen will look for

| Evidence | Weight |
|---|---|
| The chain: intent, spec, plan, tests, PR history, annotation, all consistent with each other and with the code | about half |
| The app: generates, displays, critiques, plus one more modality; runs during the presentation | about half |
| Every member can explain every part | required |
