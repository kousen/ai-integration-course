# Week 2 setup additions

Week 1 setup still applies: Git, Claude Code, your OpenRouter key entered with the hidden prompt, and the `orclaude` launcher. This week adds one language runtime and, optionally, a local model.

## 1. Pick a language and confirm its runtime

Your chat client will be written in **Python or Java**, standard library only. Choose the one you would rather read, since you will explain the code. Check that the runtime is present before the lab.

**Python**

```bash
python3 --version        # macOS
py --version             # Windows PowerShell
```

Any Python 3.9 or later works. On Windows, install from [python.org](https://www.python.org/downloads/) if the command is missing, and tick "Add python.exe to PATH".

**Java**

```bash
java --version
```

You need JDK 21 or later so the program can run directly with `java Chat.java`. If the command is missing, install a current JDK from [Adoptium](https://adoptium.net/). IntelliJ IDEA's [educational license](https://www.jetbrains.com/community/education/) is free for students and can install a JDK for you, but it is not required.

**Checkpoint D:** one of the commands prints a version of 3.9+ (Python) or 21+ (Java).

## 2. The key stays in the environment

Your program reads the API key from the `OPENROUTER_API_KEY` environment variable you set in Week 1. Use the same hidden-prompt commands from the [Week 1 guide](../01/setup.md#4-launch-with-your-openrouter-key) in the terminal where you run the client. The key never goes in a source file, a `README`, or a prompt.

## 3. Optional: a local model

A local model is not required. It needs a machine with at least 16 GB of memory for the smaller models, and the first download is several gigabytes. Ken will demonstrate one in class. If you want to try it, any of these serve the same style of chat endpoint on your own machine, so your client needs only a different base URL:

| Tool | What it is | Endpoint to try |
|---|---|---|
| [Ollama](https://ollama.com) | Command-line tool and background service; `ollama pull` then `ollama run` | `http://localhost:11434/v1` |
| [LM Studio](https://lmstudio.ai) | Desktop app with a model browser and a chat window; can also run a local server | Shown in the app's Developer tab |
| [llama.cpp](https://github.com/ggml-org/llama.cpp) | The inference engine many tools are built on; you load model files directly | Its `llama-server` prints the address it serves |

Check each tool's current documentation for the exact port and flags; they change. A model that fits in memory will still be slower and weaker than a hosted frontier model. Seeing where it falls short is part of the exercise, not a failure.

## If something goes wrong

| Symptom | Next action |
|---|---|
| `python3` or `java` not found after install | Open a new terminal so the PATH change applies |
| `401` or `Unauthorized` from OpenRouter | The key variable is not set in this terminal; repeat the hidden prompt |
| `402` or a credit message | Your OpenRouter balance or spend cap is exhausted; tell Ken |
| Empty answer but tokens were used | The model spent its output budget on hidden reasoning; raise `max_tokens` or ask a shorter question |
| Local model: connection refused | The server is not running; start the tool and retry |
