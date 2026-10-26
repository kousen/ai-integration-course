# Weekly slides

Slidev Markdown sources and exported PDFs. The shared light theme follows the blue/amber palette used in Senior Seminar, with locally available fonts for projection.

- [Week 1 Slidev source](week01.md)
- [Week 1 PDF](week01.pdf)
- [Week 2 Slidev source](week02.md)
- [Week 2 PDF](week02.pdf)
- [Week 3 Slidev source](week03.md)
- [Week 3 PDF](week03.pdf)
- [Week 4 Slidev source](week04.md)
- [Week 4 PDF](week04.pdf)
- [Week 5 Slidev source](week05.md)
- [Week 5 PDF](week05.pdf)
- [Week 6 Slidev source](week06.md)
- [Week 6 PDF](week06.pdf)
- [Week 7 Slidev source](week07.md)
- [Week 7 PDF](week07.pdf)

The PDF matches the reviewed 28-slide source, including API-billed MiniMax M3, discretionary break timing, and `lyrics.txt` in student projects.

With Slidev and the Seriph theme installed, run from this directory:

```bash
slidev week02.md
```

Build a preview outside this repository and export the student PDF:

```bash
slidev build week02.md --out /tmp/cpsc415-week02-preview
slidev export week02.md --output week02.pdf
```

If the exported PDF has fewer pages than the deck (Week 6 lost its last four with Slidev 53), export slide by slide: `slidev export week06.md --per-slide --output week06.pdf`.

The existing instructor environment has Slidev installed globally, as in Senior Seminar. Students do not need Slidev to complete the lab. PDF export requires a working Chromium runtime. Keep the PDF in the course repository and post a copy to Moodle after instructor review. Presenter cues are in Markdown comments; they are not rendered into the student PDF.

## Reused assets

- `images/project-scales.png`: Ken Kousen's *Claude Code: Up and Running*, Chapter 1 illustration, reused with the author's course authorization.
- `images/tokenizer-input.png`, `images/tokenizer-tokens.png`: Ken's `practical-ai-literacy` orientation material, September 2026. Counts apply to the depicted text and tokenizer.

These are existing source assets. No new image generation was used for Week 1.
