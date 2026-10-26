# Week 7: Team Project 1 presentations, then audio

**Monday, November 2, 2026 · 1:30–4:10 PM · MC-225**

The first hour is yours: four teams present Team Project 1, ten minutes each plus five of questions, while the other teams write notes in the peer form. After the break, the program listens and speaks. Speech-to-text and text-to-speech are two more request shapes on the OpenRouter key you already have, and the lab adds a spoken interface to your portfolio chatbot. The class ends with ten minutes on hosting, because the portfolio's November 30 milestone says "deployed" and the key has to live somewhere that is not the browser.

By the end of the session, you should be able to:

- Present a working use case of your team's app, show one artifact from the chain, and answer a question about a part you did not write.
- Transcribe a clip through OpenRouter's transcription endpoint and say what it cost and what the reply contains.
- Generate speech through the speech endpoint, say what it cost, and say why the reply carries no usage object.
- Check a transcript in code: word error rate against what was said, the words that must survive, the empty reply.
- Build the loop: the browser records, the server transcribes, answers from the profile, and speaks, with the key on the server.
- Say where the key lives on Cloudflare Pages, Vercel, and here.now, and how to prove it is not in the page.

## Today's materials

1. [Setup additions](setup.md): pull the repository, one speech call, one transcription, the microphone
2. [Lab: Hear, think, speak](lab.md) (homework, due November 9)
3. [Hosting the portfolio](hosting.md): where the key lives on each host, and the proof
4. [Week 7 slides (PDF)](../../slides/week07.pdf) · [Slide source](../../slides/week07.md)
5. [Week 7 submission requirements](../../assignments/week07-voice.md)
6. [The voice-loop example](../../examples/voice-loop/): `transcribe.py`, `speak.py`, `check.py`, the fixture clips, the server and page, the tests
7. [Peer notes form](https://docs.google.com/forms/d/e/1FAIpQLSfNKbChCap-3fGF5U-2mELJmqkGJPybHt7KplK3F__zngARNA/viewform): one submission per presenting team, during that team's question time

## Our afternoon

| Time | Activity |
|---|---|
| 1:30–1:35 | Order drawn; the form open on every laptop |
| 1:35–2:35 | Four presentations: 10 minutes each, 5 of questions, the form filled during the questions |
| 2:35–2:45 | What the room saw: patterns across the four projects |
| 2:45–3:00 | Break |
| 3:00–3:40 | Audio: the two request shapes, cost per second and per character, voices and languages, the transcript checked in code, the loop |
| 3:40–3:50 | Hosting: three hosts, one rule, one proof |
| 3:50–4:00 | Lab sheet walkthrough |
| 4:00–4:10 | What is due, questions |

Prof. Kousen may move the break depending on how the presentations run.

## Due today at 1:30 PM

- **Team Project 1**, complete: one member submits the repository URL and the tag `tp1-submitted` in the TP1 assignment ([TP1 sheet](../../assignments/team-project-1.md)). Presentations in class.
- The [Week 6 submission](../../assignments/week06-image-review.md): the PR URL in the team repository and the `week06-submitted` tag on your Week 5 repository.
- Portfolio milestone, feedback only: the chatbot answering from the profile ([portfolio sheet](../../assignments/portfolio.md)). Prof. Kousen reads it in your repository.

## After class

**Due Monday, November 9, at 1:30 PM:**

- The [Week 7 submission](../../assignments/week07-voice.md): the lab, in your portfolio repository, tag `week07-submitted`.
- The [AI-Native SDLC Playbook](https://academy.claude.com/courses/ai-native-sdlc-playbook) certificate, uploaded to Moodle (assigned October 26).

### Reading and viewing to support the work

- [OpenRouter: audio APIs](https://openrouter.ai/blog/announcements/announcing-audio-apis/): the announcement of the two endpoints; the [transcription guide](https://openrouter.ai/blog/tutorials/transcription-on-openrouter/) and the [text-to-speech tutorial](https://openrouter.ai/blog/tutorials/text-to-speech/) have the field-by-field contracts.
- [OpenRouter models with speech output](https://openrouter.ai/api/v1/models?output_modalities=speech) and [with transcription output](https://openrouter.ai/api/v1/models?output_modalities=transcription): the live catalogs with prices and, for speech models, the voice ids.
- [MediaRecorder on MDN](https://developer.mozilla.org/en-US/docs/Web/API/MediaRecorder): how the page records the microphone.
- [Cloudflare Pages Functions](https://developers.cloudflare.com/pages/functions/), [Vercel environment variables](https://vercel.com/docs/environment-variables), [here.now proxy routes](https://here.now/docs): where the key lives on each host.

## What comes next

Week 8 (November 9) is tool use and function calling: the model asks your program to run something, and your program decides whether to. Team Project 2 (an agentic / MCP system) is assigned that day.
