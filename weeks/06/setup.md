# Week 6 setup additions

Two new things: the OpenRouter Python SDK, which the Week 6 examples use instead of hand-built `urllib` requests, and the GitHub CLI, which the Deploy stage uses for pull requests. The models for chat and vision are the same two as Week 5.

## 1. Pull the course repository

```bash
cd path/to/ai-integration-course
git pull
```

That gets you `examples/image-set/` (generator, critic, checker, tests) and `examples/pr-review/` (the reviewer script, its tests, and the release gate).

## 2. The SDK

In your project's virtual environment:

```bash
pip install openrouter
```

That installs the official `openrouter` package (version 1.3.68 at the time of writing). Everything Weeks 2–5 did with `urllib` is a method on one client object: `client.chat.send(...)`, `client.embeddings.generate(...)`, and this week `client.images.generate(...)`. It is a dependency, so it goes in `spec.md` under Dependencies with its reason, and the Week 5 guard will refuse the install until it is there.

**What the SDK hides.** The raw API turns MiMo's hidden reasoning off with `"reasoning": {"enabled": false}` (Week 5, section 2). The SDK's `reasoning` object has no `enabled` field, only `effort`, so `reasoning={"enabled": False}` is silently sent as `{}` and MiMo thinks through its whole budget again. The SDK form is `reasoning={"effort": "none"}` (or `reasoning_effort="none"`); the Week 6 examples use it. When an SDK call behaves differently from the raw request, look at what it actually sent.

## 3. One image

The Image API is a different endpoint from chat (`POST /api/v1/images`), with a different request shape: a prompt, an aspect ratio, a seed. This generates one image with the class image model and saves it:

```bash
python3 - <<'EOF2'
import base64, os
from openrouter import OpenRouter
client = OpenRouter(api_key=os.environ["OPENROUTER_API_KEY"])
r = client.images.generate(model="black-forest-labs/flux.2-klein-4b", aspect_ratio="1:1", seed=415,
    prompt='A hand-drawn poster for a college course called "AI Integration": a robot and a student '
           'at a whiteboard. The title "AI Integration" is large and legible at the top.')
item = r.data[0]
ext = {"image/jpeg": "jpg", "image/png": "png", "image/webp": "webp"}.get(item.media_type, "bin")
open(f"poster.{ext}", "wb").write(base64.b64decode(item.b64_json))
print(f"poster.{ext}", item.media_type, "cost:", r.usage.cost)
EOF2
```

**Checkpoint A:** a `poster.jpg` (or `.png`) you can open, showing a robot, a student, a whiteboard, and the title, and a cost line of about `0.014`. On October 19 and 20 this call took 3 to 4 seconds. If the title is misspelled, keep the image: text is where image models fail most, and the lab's critic-checker exists to catch exactly that (in rehearsal, three of five seeds misspelled "Integration"). The `usage.cost` in the reply is what you were actually charged; record it rather than estimating.

**Seeds.** The same model, prompt, and seed should give you the same image again, which is what makes an image set reproducible and a test repeatable. Change the seed and you get a different picture of the same thing. Not every model honors the seed exactly, and "the same image" may not mean the same file: on October 20, two FLUX calls with seed 415 gave the same picture and different JPEG bytes. Some models have no seed at all: on October 26, `black-forest-labs/flux-3-image-klein` refused the request with "FLUX 3 Image does not support: seed". If your comparison model does that, the finding is that reproducibility is not on offer, not a bug in your code. The lab asks you to check both ways.

**Other image models.** `client.images.list_models()` returns every model the Image API can call; `python3 -c "from openrouter import OpenRouter; import os; [print(m.id) for m in OpenRouter(api_key=os.environ['OPENROUTER_API_KEY']).images.list_models().data]"` lists their ids. The lab's comparison model is `google/gemini-3.1-flash-lite-image`, which is priced per image token ($0.034 for one 1:1 image on October 20; it accepted `seed` and `aspect_ratio`) and stamps its output with a SynthID watermark. Do not use `qwen/qwen-image-2.1-turbo`; in rehearsal it hung for forty minutes.

## 4. The GitHub CLI, for pull requests

`gh` opens and merges pull requests from the terminal, so the Deploy stage does not need the browser.

```bash
gh --version              # install from https://cli.github.com if this fails
gh auth login             # GitHub.com, HTTPS, log in with a web browser
cd path/to/your-team-repo
gh pr list                # empty is fine; an error means auth or the wrong folder
```

**Checkpoint B:** `gh pr list` runs without an error inside your team's repository. (`gh pr create` and `gh pr merge` are in the lab.)

## 5. The guard and the gate

The Week 5 guard stays installed in every repository you use the agent in, including the team repository. Check: `echo '{"tool_name":"Bash","tool_input":{"command":"git push --force"}}' | python3 .claude/hooks/guard.py` must print the "destructive" message. The release gate (`examples/pr-review/gate.sh`) is installed in the lab.

## If something goes wrong

| Symptom | Likely cause |
|---|---|
| `ModuleNotFoundError: openrouter` | Installed in a different virtual environment, or the guard refused the install because `spec.md` does not list it yet |
| `400` from the Image API naming `aspect_ratio` or `seed` | The model does not support that option; drop it or check the model's page |
| The generation takes minutes | Some models queue; try the class model, and never wait more than a minute or two in a test |
| `gh: command not found` on Windows | Open a new terminal after installing, or use the winget/scoop install from cli.github.com |
| `gh pr create` says "no commits between main and ..." | You are on `main`; make a branch first (lab step 6) |
| MiMo's reply is empty or cut off | Hidden reasoning spent the budget; through the SDK use `reasoning={"effort": "none"}` (section 2), not `{"enabled": False}` |
| The reviewer prints nothing and exits 2 | The model did not answer in the expected form; the gate fails closed. Run again or read the raw reply it printed |
