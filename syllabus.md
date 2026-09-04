# Trinity College

## *Department of Computer Science*

## CPSC 415-01: Special Topics — AI Integration, Fall 2026

*Current revision: September 4, 2026 (supersedes the April 17 draft)*

**Lectures:** Mondays, 1:30 PM – 4:10 PM\
**Room:** MC-225\
**Prerequisite:** C- or better in CPSC 215 (Data Structures). No prior AI, web, or systems experience is required, and the course assumes wide variation in programming background.\
**Distribution:** Meets the Numerical & Symbolic Reasoning requirement

---

## Contact Info

**Instructor:** [Ken Kousen](https://internet3.trincoll.edu/FacProfiles/Default.aspx?fid=1000576)\
**Email:** [kkousen@trincoll.edu](mailto:kkousen@trincoll.edu)\
**Office hours:** Thursdays, 10:00 AM – 12:00 PM, MECC 175

---

## Course Description

AI Integration is a project-based course on building software that uses commercial AI services as components. Students learn to access AI capabilities programmatically and integrate them into working applications across every modern modality: text generation, retrieval over documents, vision, image generation, and audio. The second half of the course moves into agentic patterns: tool use, the Model Context Protocol (MCP), autonomous agents, skills, subagents, and the coding-agent harnesses that professional developers now use every day.

Two ideas run through the whole semester.

**First, you will build everything with a coding agent.** From the first week, students work inside a coding agent (Claude Code, run against the model of their choice). The agent writes most of the code. Your job is to decide what gets built, steer the agent, verify the result, and be able to explain every choice. Because the agent handles syntax, you are free to build in any programming language, including ones you have never seen. Everyone arrives with Java from CPSC 215, so Java is the shared baseline and any other language counts as new. Choosing a language becomes a design decision you justify, not a limitation you work around.

**Second, you will work the way AI-native teams work.** Anthropic's *AI-Native SDLC Playbook* (August 2026) describes a software development life cycle in which every stage produces a short, version-controlled artifact: an intent file, a spec, a plan, tests, a reviewed pull request, and a maintenance loop that feeds back into new intent. This course adopts that artifact chain as its working method. Every assignment is submitted as a chain of artifacts plus the code, and grading looks at the chain as much as the code. The chain is how you prove you understood what the agent built.

Specific vendors and models will change during the semester as the field evolves. The emphasis is on transferable patterns.

---

## Course Objectives

By the end of the course, students should be able to:

1. Access modern AI models programmatically through REST APIs and vendor SDKs, in more than one language
2. Work productively inside a coding-agent harness: plan mode, context files, permissions, hooks, subagents, and skills
3. Run a feature from intent through spec, plan, build, test, and pull request using the AI-native SDLC artifact chain, and explain the human decision point at each stage
4. Design and evaluate prompts, including structured output and simple regression evals
5. Build a retrieval-augmented generation (RAG) pipeline over their own documents
6. Integrate vision, image-generation, video, and audio models into larger applications, and run local open-source models where they suffice
7. Implement tool use and build an MCP server that a coding agent can call
8. Design an agentic workflow and distinguish it from a simple chat integration
9. Read, verify, and critique code in a language they did not previously know
10. Choose among hundreds of available models on cost, capability, and openness, and defend the choice
11. Explain the cost, safety, provenance, and ethical trade-offs of AI-integrated software

---

## Required Texts and Online Courses

There is no required textbook. Readings (vendor documentation, blog posts, and papers) are posted on Moodle each week.

The course uses several free courses from [Claude Academy](https://anthropic.skilljar.com/). Each awards a completion certificate, and certificates are a graded component (see below). Required:

| Course | Assigned | Certificate due |
|---|---|---|
| Claude Code 101 | Week 1 | Week 2 |
| AI Fluency for Students | Week 1 | Week 3 |
| The AI-Native SDLC Playbook | Week 6 | Week 8 |
| Introduction to Model Context Protocol | Week 8 | Week 9 |
| Introduction to Subagents *or* Introduction to Agent Skills | Week 10 | Week 11 |

Recommended but not required: Claude Code in Action, Building with the Claude API, Model Context Protocol: Advanced Topics. Trinity's own non-credit [AI Literacy for All](https://www.trincoll.edu/academic-ai/students/) course, which awards a LinkedIn badge, may be submitted in place of the AI Fluency for Students certificate.

Reference for the working method: [The AI-Native SDLC Playbook](https://claude.com/blog/the-ai-native-sdlc-playbook) (Anthropic, August 2026).

---

## Computing Resources

Every student needs a laptop with a code editor (VS Code recommended), Git, and a coding agent. The course standardizes on the Claude Code harness because it is the reference implementation for skills, MCP, hooks, and subagents. You do not need a Claude subscription to run it.

**Model access.** Students access models through [OpenRouter](https://openrouter.ai/), a prepaid, pay-as-you-go gateway to models from Anthropic, OpenAI, Google, and others. Week 1 covers setup, including a launcher script that points Claude Code at any OpenRouter model. Key points:

- OpenRouter is prepaid, so you cannot spend more than you load. Load $20 to start and expect to spend roughly $50 over the semester. Set a spend limit on your API key.
- OpenRouter lists more than 500 models, including the major Chinese open-weight models (GLM, Kimi, DeepSeek, Qwen), many of which cost pennies per million tokens. Use one of these during the first two weeks while you learn the tool and make mistakes. Switch to Claude Sonnet for the artifact-chain work that starts in Week 3. Reserve Opus-class models for planning and review.
- Local open-source models (via Ollama or equivalent) are covered in Week 2 and are a legitimate zero-cost choice for any component where they are good enough.
- Model choice is a design decision, like language choice. Your `spec.md` states which model each component uses and why, and the course expects you to compare a cheap model against a frontier one on real tasks before deciding.
- Students who already have a Claude Pro or Max subscription can use it directly and skip OpenRouter.
- The instructor is pursuing Google Cloud credits for the class. If they come through, they supplement OpenRouter for the vision, image, and audio weeks. Nothing in the course depends on them.
- The college provides BoodleBox as its secure environment for everyday AI use, and it is a good choice for reading, brainstorming, and chat. This course also requires direct API access because building software on AI services is the subject of the course. That access runs through accounts you create and pay for yourself, and the only data that passes through them is code and content you choose to publish. Do not send college data, other people's personal information, or anything covered by Trinity's [AI and data privacy guidance](https://www.trincoll.edu/lits/technology/security/best-practices/ai-data-privacy/) through any external AI service.

All generated media and API usage must stay within the acceptable-use guidelines in the Responsible AI section below.

---

## Grading

| Component | Weight | Description |
|---|---|---|
| **Participation and labs** | 15% | Attendance, engagement, and in-class lab work. Most Mondays are roughly half lecture, half supervised lab. |
| **Claude Academy certificates** | 10% | Five required certificates, on time. |
| **Team Project 1: Multimodal Web App** | 15% | Teams of 2–3. A web app that generates, displays, and critiques images, with at least one other modality (vision or audio). |
| **Team Project 2: Agentic / MCP System** | 20% | Teams of 2–3. An agent or MCP server that performs a task beyond a single model call. |
| **Individual Portfolio: AI-Enabled Profile Site** | 25% | Individual. A personal site with a grounded chatbot, built through the artifact chain over the whole semester. |
| **Final: Comprehension Defense** | 15% | Individual oral exam during finals week. You walk the instructor through your portfolio and answer questions about every choice. |

### Notes on grading

**Everything is submitted as an artifact chain.** A submission is a Git repository containing, at minimum, `intent/`, `spec.md`, `plan.md`, tests, and a pull request history. The rubric for each assignment weights the chain and the code roughly equally. Working code with no chain, or a chain the student cannot explain, earns at most half credit.

**Teams.** With 10–11 students, expect four teams of 2–3. Teams are formed in Week 3 and may stay together for both team projects or re-form in Week 8. Every team member must be able to explain every part of the submission.

**The new-language requirement.** Your portfolio must include at least one component written in a programming language you had never used before this course, chosen and justified in its `spec.md`. Java does not qualify. Python is the obvious candidate, since the Claude Academy MCP course and most vendor examples use it, but TypeScript, Go, Kotlin, Rust, or anything else is welcome. The four-question annotation (below) for that component must include what you learned about reading unfamiliar code.

**The four-question annotation.** Every project in the portfolio, and every team project, is annotated with:

- *What is this?* A plain statement of what it does and does not do.
- *Why this choice?* What alternatives existed, including language and model, and what trade-offs were weighed.
- *What breaks?* Fragile points, assumptions, blast radius.
- *What did I learn?* Concretely, including places where the agent was confidently wrong and you caught it.

**The Comprehension Defense** replaces a written final exam. Each student gets a 20-minute slot during finals week. You bring your portfolio repo; the instructor picks components and asks the four questions plus follow-ups. The defense is graded on accuracy and depth of understanding, not on polish.

### Late Submission Policy

Programming assignments MUST be submitted electronically on or before the due date and time listed on the assignment. No late assignments are accepted except through "late days."

Each student is allocated **3 late days** per semester, usable at their discretion in 24-hour increments. Late days may be applied to any assignment and used individually or together. There is no bonus for unused late days. Late days do not apply to presentations or the Comprehension Defense.

Grade weights are subject to adjustment as the semester develops to ensure fair assignment of course grades.

---

## The Working Method: The AI-Native SDLC Artifact Chain

The course introduces one stage of the artifact chain roughly every week alongside that week's modality. By Week 6 you will have run the full loop at least once.

| Stage | Artifact | The agent does | You do |
|---|---|---|---|
| Plan | `intent/<name>.md` | Interviews you until it understands the goal, then drafts intent | Correct the draft; product owner approves |
| Design | `spec.md` | Turns approved intent into requirements and design, applying team skills and style guides | Validate the spec against the intent |
| Build | `plan.md` + code | Proposes files, order of work, risks, and success criteria; implements, often with subagents | Interrogate the plan ("what could break?"); approve before code |
| Test | tests, lint, CI | Writes and runs tests, lints, drives the browser | Verify the feedback loops actually ran |
| Deploy | pull request + review findings | A separate agent reviews against `REVIEW.md` policies; hooks gate anything risky | Code owner approves; release gate is a human decision |
| Maintain | new `intent/<name>.md` | An alert, ticket, or schedule triggers diagnosis and a proposed intent | Service owner triages |

Two files travel with every repo: `CLAUDE.md` (team conventions, commands, common mistakes) and `REVIEW.md` (review passes ranked by severity). Both are graded artifacts.

---

## Weekly Schedule

> Thirteen Monday meetings. October 12 is Trinity Days (no class). November 23 meets, the Monday before Thanksgiving. December 14 is the last day of classes.

### Week 1 — Monday, September 14
**The landscape, the toolchain, and your first agent session**

- Course overview, expectations, and why the course is structured around coding agents and the artifact chain
- Survey of frontier providers (Anthropic, OpenAI, Google) and what each is good at right now
- Responsible AI module: bias, provenance, safety filters, synthetic media, acceptable use of course credentials
- Setup lab: Git and GitHub, VS Code, OpenRouter account and key with a spend limit, Claude Code, the launcher script, a near-free model for practice
- First live session: have the agent write the same "hello, model" API call in Java and in two languages you have never used, then read all three
- **Assigned:** Claude Code 101 (certificate due Week 2), AI Fluency for Students (due Week 3), setup checklist

---

### Week 2 — Monday, September 21
**Working with a coding agent; text generation fundamentals**

- How a harness works: the loop around the model, tools, context, permissions
- `CLAUDE.md`, plan mode, context management, when to start a fresh session
- Chat APIs: system prompts, roles, parameters, streaming, token counting, cost
- Local open-source models: running one with Ollama, pointing the same client and the same coding agent at it, and seeing where it falls short
- *Chain stage: Plan.* The discovery interview. The agent asks you questions until it can write `intent.md`; you correct it
- **Lab:** write the intent for a small chat client, then have the agent build it in Java and port it to a language you have never used. Compare the two. Run the same build once on a pennies-per-million model and once on Claude Sonnet, and note what differed.
- **Due:** Claude Code 101 certificate

---

### Week 3 — Monday, September 28
**Prompting, structured output, and evaluation**

- Prompt patterns: few-shot, role, delimiters, chain-of-thought and when it hurts
- Structured output: JSON schemas and typed responses across providers
- Evaluating prompts: small regression suites, catching hallucination and refusal
- *Chain stage: Design.* From intent to `spec.md`. Encode team style and conventions as a skill the agent applies when writing the spec
- Teams formed
- **Lab:** build a structured-output client against two providers, with a five-case eval
- **Assigned: Team Project 1, Multimodal Web App** (due Week 7). **Assigned: Portfolio intent** (individual, due Week 4)
- **Due:** AI Fluency for Students certificate

---

### Week 4 — Monday, October 5
**Retrieval-Augmented Generation**

- Embeddings, vector stores, chunking, retrieval quality
- A RAG pipeline end to end; when RAG helps and when it hurts
- *Chain stage: Build.* `plan.md`: files, order, risks, proof. Interrogating the plan. Subagents and Git worktrees for parallel work. Permissions and blast radius.
- **Lab:** RAG over a provided document set, built from an approved plan
- **Due:** Portfolio `intent.md` and `spec.md` (the grounded profile and the "not yet" inventory)

---

*Monday, October 12 — Trinity Days, no class*

---

### Week 5 — Monday, October 19
**Vision models**

- Image understanding: description, extraction, structured output from images
- Multimodal prompts; vision as a front end to downstream logic
- *Chain stage: Test.* Agent-written tests, linting, and browser-driven testing (Playwright or equivalent). Verifying that the feedback loop ran.
- Hooks as guardrails: blocking folders, unapproved packages, and destructive commands
- **Lab:** extract structured data from real-world images, with agent-written tests

---

### Week 6 — Monday, October 26 *(mid-term)*
**Image generation; deploy and review**

- Text-to-image APIs; prompt design, style control, negative prompts
- Video generation APIs: current capabilities, cost, and provenance
- Provenance metadata and responsible use
- *Chain stage: Deploy.* Pull requests, a separate reviewing agent, `REVIEW.md` passes ranked by severity, hooks as release gates
- **Lab:** generate and critique an image set; wire it into Team Project 1 via a reviewed PR
- **Assigned:** The AI-Native SDLC Playbook course (certificate due Week 8). You have now lived every stage; the course names them.

---

### Week 7 — Monday, November 2
**Team Project 1 presentations; audio**

- Team presentations and peer critique of the Multimodal Web App
- Speech-to-text and text-to-speech APIs
- Combining audio, text, and image in one pipeline
- **Lab:** add a spoken interface to the portfolio chatbot
- **Due:** Team Project 1

---

### Week 8 — Monday, November 9
**Tool use and function calling**

- Tool schemas across providers; single-shot, loops, branching
- Failure modes: bad calls, infinite loops, tool hallucination
- Teams confirmed or re-formed
- **Lab:** give the portfolio chatbot one real tool and test its misuse cases
- **Assigned: Team Project 2, Agentic / MCP System** (due Week 12). **Assigned:** Introduction to MCP (certificate due Week 9)
- **Due:** SDLC Playbook certificate

---

### Week 9 — Monday, November 16
**The Model Context Protocol**

- Why MCP exists: standardized tools, resources, and prompts across hosts
- Servers, clients, transports
- **Lab:** build an MCP server in your team's language and connect it to Claude Code. Use it from a session.
- **Due:** Introduction to MCP certificate

---

### Week 10 — Monday, November 23 *(Monday before Thanksgiving)*
**Agents from scratch**

- What makes a system agentic; the plan, act, observe, revise loop
- Memory, context management, autonomy versus oversight
- **Lab day:** implement a small agent loop with no framework, in any language. Remote attendance available.
- **Assigned:** Introduction to Subagents or Introduction to Agent Skills (certificate due Week 11)

---

### Week 11 — Monday, November 30
**Skills, subagents, harnesses; closing the loop**

- Skills as packaged, versioned capabilities; subagents as delegation
- Comparing harnesses: Claude Code, Codex, Cursor, and what "harness" means architecturally
- *Chain stage: Maintain.* Triggers that generate new intent; continuous evals in CI when a model or skill changes; leading and lagging indicators
- **Lab:** package a skill your team has been reusing; add a five-task eval that runs in CI
- **Due:** Subagents or Skills certificate

---

### Week 12 — Monday, December 7
**Team Project 2 presentations; portfolio work**

- Team presentations and peer critique of the Agentic / MCP System
- Supervised portfolio work session; adversarial testing of each other's chatbots
- **Due:** Team Project 2

---

### Week 13 — Monday, December 14 *(last day of classes)*
**Portfolio walkthroughs and synthesis**

- Individual portfolio walkthroughs (lightning format)
- Course synthesis: how the modalities and the chain fit together; what to watch next
- Comprehension Defense preparation
- **Due:** Portfolio

---

### Finals Week (December 17–23)
**Comprehension Defense** — 20-minute individual slots, scheduled per the Registrar's exam period

---

## Policy on AI Tools

This entire course is about AI integration, so students are expected and encouraged to use AI tools in any way they can imagine, and are required to use a coding agent for all coursework. A monthly consumer subscription is **not** necessary; programmatic access is pay-as-you-go and generally less expensive for coursework usage.

Students must still:

- Understand and be able to explain their work. The Comprehension Defense tests exactly this.
- Distinguish useful output from wrong output
- Keep the artifact chain honest: intent and spec written before code, plans approved before implementation
- Not present unexamined AI output as if it were automatically correct

This policy is the course-specific statement that Trinity asks every instructor to provide. It sits inside the college's [AI and Academic Integrity guidelines](https://www.trincoll.edu/academic-ai/students/academic-integrity/) on the [Academic AI site](https://www.trincoll.edu/academic-ai/), which every student should read. Where this syllabus permits more AI use than another course does, that permission applies only here.

---

## Responsible AI and Ethics

All students complete a responsible-AI module in Week 1 and the AI Fluency for Students course covering:

- Bias in AI systems and downstream impact
- Social implications of AI-generated content, including synthetic media
- Data privacy and handling of user-supplied content
- The ethical responsibilities of AI application developers
- Acceptable-use guidelines for course API credentials

Students will not generate images of real individuals, create deceptive or misleading content, or use course resources for anything outside assigned coursework. All generated media should include provenance metadata indicating AI-generated content where practical. The portfolio chatbot must refuse to fabricate: an honest "not yet" beats a confident false claim, and the adversarial test set will check for this.

Assignments include reflection components where students evaluate their systems for potential bias, failure modes, and misuse scenarios.

---

## Class Meetings in Unusual Circumstances

Due to bad weather or other unusual circumstances, there may be occasions when the class needs to meet virtually. In such a case, you will receive an email at least 30 minutes before class indicating that it will be virtual, using our regular Zoom link.

---

## Academic Dishonesty

Cases of academic dishonesty will be handled in accordance with the rules of Trinity College. Incidents of academic dishonesty void the grading policy and, in such cases, the final grade assigned for the term is at the discretion of the instructor.

---

## Policy on Class Conduct

You are expected to be polite and respectful toward the instructor and other students at all times. For details, see the Community Standards document at [https://www.trincoll.edu/dean-of-students/community-standards/](https://www.trincoll.edu/dean-of-students/community-standards/).

Signs of non-engagement, such as using cell phones or laptops for non-class purposes, will significantly impact your class participation grade, as engagement is the cornerstone of participation.

---

## Accommodations

Trinity College is committed to creating an inclusive and accessible learning environment consistent with the Americans with Disabilities Act. Students with disabilities who may need accommodations in order to fully participate in this class are urged to contact the Student Accessibility Resource Center (SARC) as soon as possible to explore what arrangements need to be made to assure access.

**If you have approval for academic accommodations, please notify me by the end of week two of classes.** For students with accommodations approved after the start of the semester, a minimum of 10 days' notice is required. Please meet with me privately to discuss implementation. SARC can be reached at [SARC@trincoll.edu](mailto:SARC@trincoll.edu).

---

## Academic Honesty Pledge

All students must sign the following declaration at the first meeting of every course:

> In accordance with Article II of the Trinity College Student Integrity Contract, I hereby pledge that the papers, exams, and other academic exercises I submit for this course will represent my own work; that I will properly acknowledge and attribute any and all information and ideas that I have used from other sources; and that no collaboration unauthorized by the instructor of the course will occur in the course of its completion.
>
> I have read and understood the class policy statement, especially as it pertains to grading, academic dishonesty, classroom policies and required meetings outside of class time.

Name: _______________________   Phone (optional): _______________________

Dropping this policy statement in the designated drop box will act as a signature for acknowledging that you have read and understood this statement. Please type your phone number into the comments on Moodle when dropping the document (if you are comfortable providing your phone number).

---

*The information in this syllabus may be updated during the course. Check Moodle regularly for the most current version.*
