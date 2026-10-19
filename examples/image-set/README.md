# An image set: generate, critique, check

Three small programs for the Week 6 lab and for Team Project 1's critique path. Standard library plus the `openrouter` SDK; no framework.

| File | What it is |
|---|---|
| `generate.py` | Calls OpenRouter's **Image API** (`POST /api/v1/images`) once per prompt through `client.images.generate`, saves each image, and writes `manifest.json`: prompt, seed, model, media type, file, and the cost from the reply. |
| `critique.py` | Sends each image to a **vision model** through the chat endpoint (Week 5's request) with a yes/no checklist made from the prompt's requirements, parses the JSON, and then, in plain code, compares the checklist with the requirements. With `--compare`, shows where two critique files disagree. No key needed for that part. |
| `prompts.json` | Five prompts from one family (the course poster), each with a seed, three or four requirements, and the title text expected. Replace it with your own family. |
| `tests/test_checker.py` | No-key tests for the checker: all met, one unmet, one unanswered, one invented, not JSON, JSON in prose, the text comparison, two critics disagreeing. |

## Run it

```bash
pip install openrouter pytest
python3 -m pytest tests -v                                # no key, under a second
export OPENROUTER_API_KEY=...
python3 generate.py prompts.json --out images             # five images; about $0.014 each on FLUX.2 klein
python3 critique.py images/manifest.json                  # five critiques on minimax/minimax-m3, writes critique.json
python3 critique.py images/manifest.json --model xiaomi/mimo-v2.6-flash --out critique-mimo.json
python3 critique.py --compare critique.json critique-mimo.json
```

Without a key, `generate.py` and `critique.py` stop with one line saying so and exit 1; nothing is billed by accident.

## What the checker can and cannot say

The critic is a model. The code does not know whether there is a robot in the picture; it knows whether the critic **answered every requirement, answered only those, and said each was met**, and whether the title the model read back matches the title the prompt asked for. That is enough to catch a critic that drifts from the checklist, invents a requirement, returns prose instead of JSON, or misreads text, which is what happened on October 19, 2026: FLUX spelled "AI Integration" correctly and the critic reported "Integratlon". A critic that says "met" when it is not is caught only by a second model (`--compare`) or by a person looking. Use both.

## Two request shapes

Image generation has its own endpoint and body (`model`, `prompt`, `aspect_ratio`, `seed`), and its reply carries `data[0].b64_json`, `data[0].media_type`, and `usage.cost`. The critique uses the chat endpoint with an image content part, as in Week 5. Some image models can also be called through chat completions with `modalities=["image", "text"]`; the Image API is the one the lab uses because it is the same shape for every image model.

## Settings that matter

- **Seed.** Same model, prompt, and seed should give the same image; the lab asks you to check. Change the seed for a different picture of the same thing.
- **Reasoning.** `xiaomi/mimo-v2.6-flash` needs `reasoning={"enabled": False}` or its reply is empty; `minimax/minimax-m3` needs reasoning on. `critique.py` keeps a per-model table; see [Week 5 setup, section 2](../../weeks/05/setup.md).
- **Cost.** One generation per prompt, one critique per image, never a model call inside a loop of tests. The manifest and the critique file record what each call cost so `CHECKS.md` can quote it.
