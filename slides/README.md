# Weekly slides

Slidev Markdown sources and exported PDFs. The shared light theme follows the blue/amber palette used in Senior Seminar, with locally available fonts for projection.

- [Week 1 Slidev source](week01.md)
- [Week 1 PDF](week01.pdf)

The PDF matches the reviewed 28-slide source, including API-billed MiniMax M3, discretionary break timing, and `lyrics.txt` in student projects.

With Slidev and the Seriph theme installed, run from this directory:

```bash
slidev week01.md
```

Build a preview outside this repository and export the student PDF:

```bash
slidev build week01.md --out /tmp/cpsc415-week01-preview
slidev export week01.md --output week01.pdf
```

The existing instructor environment has Slidev installed globally, as in Senior Seminar. Students do not need Slidev to complete the lab. PDF export requires a working Chromium runtime. Keep the PDF in the course repository and post a copy to Moodle after instructor review. Presenter cues are in Markdown comments; they are not rendered into the student PDF.

## Reused assets

- `images/project-scales.png`: Ken Kousen's *Claude Code: Up and Running*, Chapter 1 illustration, reused with the author's course authorization.
- `images/tokenizer-input.png`, `images/tokenizer-tokens.png`: Ken's `practical-ai-literacy` orientation material, September 2026. Counts apply to the depicted text and tokenizer.

These are existing source assets. No new image generation was used for Week 1.
