# Week 5 setup additions

Nothing new to install for the lab itself. The vision call goes through the same chat endpoint, with the same key, to the same two models as Week 3. Team Project 1 teams need Playwright by October 26.

## 1. Pull the course repository

```bash
cd path/to/ai-integration-course
git pull
```

That gets you `weeks/05/images/` (five receipts and their answer key), `examples/guardrail-hook/` (the hook the lab installs), and `examples/key-on-server/test_browser.py` (the browser check).

## 2. One vision check

An image goes into a chat request as a content part next to the text: a data URL with the image's bytes in base64. This sends `receipt-01.png` and asks for one sentence:

```bash
python3 - <<'EOF2'
import base64, json, os, urllib.request
img = base64.b64encode(open("weeks/05/images/receipt-01.png", "rb").read()).decode()
body = {"model": "minimax/minimax-m3", "max_tokens": 200, "messages": [{"role": "user", "content": [
    {"type": "text", "text": "In one sentence, what is this and what was the total?"},
    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img}"}}]}]}
req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=json.dumps(body).encode(),
    headers={"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}", "Content-Type": "application/json"})
d = json.load(urllib.request.urlopen(req))
print(d["choices"][0]["message"]["content"], "\n", d["usage"])
EOF2
```

**Checkpoint A:** a sentence naming Mather Dining Hall and $13.66, and a usage line of roughly 700–800 tokens in. An image costs tokens like text does; a receipt-sized PNG is a few hundred to a thousand tokens depending on the model, well under a cent.

Both class models accept images: `minimax/minimax-m3` and `xiaomi/mimo-v2.6-flash`. `curl -s https://openrouter.ai/api/v1/models` lists `input_modalities` for every model if you want another; some free ones also take images. A local model through Ollama works if it is a vision model (for example `ollama pull gemma3:4b`).

## 3. A test runner

Python: `pip install pytest` in your project's virtual environment. Java: JUnit 5 through Gradle or Maven, which the agent will set up; make sure `./gradlew test` or `mvn test` runs once before the lab.

## 4. Playwright, for Team Project 1 (by October 26)

```bash
pip install playwright pytest
playwright install chromium
```

or, in a JavaScript project, `npm init playwright@latest`. The first install downloads a browser (about 150 MB). Check it against the Week 4 server:

```bash
cd examples/key-on-server
python3 server.py &                      # needs OPENROUTER_API_KEY and CHAT_MODEL
python3 -m pytest test_browser.py -v
```

**Checkpoint B:** `1 passed`. If you want to see the browser, add `headless=False` to the `launch()` call.

## If something goes wrong

| Symptom | Likely cause |
|---|---|
| `400` with a message about `image_url` or modality | The model does not accept images; check `input_modalities` |
| The reply describes the image but every number is slightly off | Normal for a faded or tilted photo; that is what the checker is for |
| The reply is prose with JSON inside it | Expected from some models; your parser takes the `{...}` out, as in Week 3 |
| The hook never fires | Claude Code was started in a different folder, or was not restarted after adding `settings.json` |
| `playwright install` is slow | It downloads a browser; do it before class |
