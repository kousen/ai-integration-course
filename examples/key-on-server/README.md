# Keeping the API key on the server

A web page cannot hold an API key. Anyone can open the page source or the browser's network tab and copy it, then spend your credit. So a web app that calls a model needs a server of its own, even when it only runs on your laptop: the browser talks to your server, and your server adds the key and calls the provider.

These two programs do exactly that and nothing else. They use only their standard library so the whole mechanism is visible; in your project, a web framework (Flask or FastAPI in Python, Spring Boot in Java, and so on) does the same job with less code.

| File | What it is |
|---|---|
| `index.html` | A page with one text box. It sends the question to `/api/ask` as plain text. It never sees the key or the model name. |
| `server.py` | Python 3 (`http.server`, `urllib`). Serves the page; on `POST /api/ask` it adds the key and the model and forwards the request. |
| `Server.java` | Java 21+ (`com.sun.net.httpserver`, `java.net.http`). The same contract. It builds one small JSON body by hand, so it needs no JSON library. |

## Run it

```bash
export OPENROUTER_API_KEY=...            # the server reads it; the browser never does
export CHAT_MODEL=minimax/minimax-m3     # the server decides which model is paid for
python3 server.py                         # or: java Server.java
```

Open http://localhost:8000 and ask something. Run it from this folder so the server finds `index.html`.

## Check that the key really stays on the server

- **View the page source** in the browser: no key, no model name.
- **Open the network tab:** the request to `/api/ask` carries only your question. The call to OpenRouter never appears, because the browser didn't make it.
- **Search what you would deploy:** `grep -r "sk-or" .` finds nothing.

## What these deliberately leave out

A deployed version also needs a limit on who can call `/api/ask`, or anyone who finds the URL spends your credit: a password, a rate limit, or both. Give it its own OpenRouter key with a small credit limit. Hosting options (Cloudflare Pages Functions, Vercel, here.now proxy routes) are covered later in the semester; each keeps the key in a secret store for the same reason.
