# Hosting the portfolio: where the key lives, and the proof

The portfolio's November 30 milestone says "site deployed." Since Week 4 the rule has been that the key stays on a server you control, because a browser cannot keep a secret. Hosting is the same rule with someone else's server. This page is the decision you write into `spec.md` and the check you run before you call it deployed. The Deploy stage of the chain is still the reviewed merge from Week 6; hosting is what happens to `main` afterwards.

## One rule, three hosts

Each host gives you a place to run a small function next to your static pages and a secret store the function can read. The function is your `/api/ask` (and `/api/voice`) from the labs, with the key read from the host's store instead of your shell.

| Host | The function | Where the key lives | Local run |
|---|---|---|---|
| **Cloudflare Pages** (the course default; Prof. Kousen's site) | `functions/api/ask.js` is served at `/api/ask`; `env.OPENROUTER_API_KEY` inside it | `wrangler pages secret put OPENROUTER_API_KEY`, or Settings → Environment variables in the dashboard, marked **encrypted** | `wrangler pages dev` with a `.dev.vars` file that is in `.gitignore` |
| **Vercel** | `api/ask.js` (or `.py`) is served at `/api/ask`; `process.env.OPENROUTER_API_KEY` | Project → Settings → Environment Variables, marked **sensitive** | `vercel dev` with `vercel env pull` writing `.env.local`, in `.gitignore` |
| **here.now** | No function: a **proxy route** in `.herenow/proxy.json` maps `/api/ask` to the provider's URL | A **service variable** on your account, injected into the proxied request's header; restrict it to the upstream host | A published site from a signed-in account (proxy routes need one) |
| Your own server (Railway, Render, a VM) | The Week 4 server as it is, in a container | The host's environment variables or secret store | What you already run |

Free tiers exist on all four at this course's traffic. Pick one in `spec.md` with the alternative you rejected and the reason; the choice is a **language** decision in disguise (Pages Functions and Vercel functions are JavaScript or Python; here.now is configuration; your own server is anything).

## What the deployed site must also have

- **Its own key**, with a credit limit, created on the OpenRouter keys page for this site only. When it leaks, you rotate one key, not the one your coursework uses. The Week 7 voice turn costs about half a cent on the class models, most of it the spoken answer, and a typed question about a tenth of that; a $5 limit is a thousand voice questions.
- **A cap on the route:** a maximum message length (the Week 4 server had one), a rate limit per IP where the host offers one (here.now's default is 100 requests an hour per IP; Cloudflare has a Rate Limiting rule on the free plan), and no loop: one model call per request.
- **CORS to your own origin.** The function should answer only pages from your site; Prof. Kousen's `_lib.js` has a four-line example.
- **The vector store, if any:** the portfolio chatbot does not need one (one profile fits in the prompt). If a project of yours does, the host decides: Vectorize on Cloudflare, Postgres with pgvector on Vercel, Chroma or Redis on a server you run.

## The proof

A site that "works" can still leak the key. Four checks, the first three from Week 4 and the last from Week 5:

1. **View the page source** of the deployed site: no key, no model name.
2. **Open the network tab,** ask a question: the only request leaving the browser goes to your own `/api/ask`, and it carries no `Authorization` header. The call to the provider never appears, because the browser did not make it.
3. **Search what you deployed:** `grep -r "sk-or" .` over the build output and the repository finds nothing; `git log -p | grep "sk-or"` finds nothing either (a key in any commit is treated as compromised, so rotate it).
4. **Run the browser check against the live URL:** `URL=https://your-site python3 -m pytest test_browser.py` with the Week 5 test's `URL` made configurable. Its last three assertions are the deployment's acceptance test. Record the run in `CHECKS.md`.

A site that passes all four and answers one question from the test set is deployed. The decision, the alternative, the key's limit, and the four results go in `spec.md` and `CHECKS.md`; the Comprehension Defense asks about them.
