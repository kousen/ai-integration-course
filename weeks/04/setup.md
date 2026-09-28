# Week 4 setup additions

The lab reads this course's own Markdown pages, so you need an up-to-date clone of the course repository, and it calls one new OpenRouter endpoint with the key you already have.

**New this week: libraries and build tools are allowed.** Weeks 2 and 3 used only the standard library so you could see the raw requests. From now on, use a package manager and a build tool: `pip` in a virtual environment or `uv` for Python, Gradle or Maven for Java. Record each library in your `spec.md` under **Dependencies**, with the reason for it.

## 1. Pull the course repository

If you cloned `ai-integration-course` for the `orclaude` script, update it. That also gets you the September 28 fix to `orclaude`.

```bash
cd path/to/ai-integration-course
git pull
```

If you never cloned it: `git clone https://github.com/kousen/ai-integration-course.git` beside your other course folders. The lab indexes `syllabus.md`, `assignments/`, and `weeks/01` through `weeks/03` from this folder.

## 2. One embeddings check

An embedding turns a piece of text into a list of numbers. Texts with similar meaning get lists that point in similar directions. OpenRouter serves embedding models on the same key and the same kind of request as chat, at a different path:

```bash
curl -s https://openrouter.ai/api/v1/embeddings \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "openai/text-embedding-3-small", "input": ["The Week 3 lab is due October 5."]}' \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print(len(d['data'][0]['embedding']), 'numbers,', d['usage'])"
```

**Checkpoint A:** it prints `1536 numbers,` and a usage line with a cost around $0.0000002. Indexing every course page for the lab costs well under a cent.

Other embedding models work the same way; `curl -s https://openrouter.ai/api/v1/embeddings/models` lists them. Some are free, such as `nvidia/nemotron-3-embed-1b:free`. If you use a local model through Ollama, pull an embedding model (for example `ollama pull nomic-embed-text`) and point the base URL at `http://localhost:11434/v1`.

## 3. Watch the RAG video

[Retrieval-Augmented Generation](https://youtu.be/3kMwv7Kraxk), about 20 minutes. Prof. Kousen walks through the same six steps in three frameworks. In class Prof. Kousen builds the same steps by hand, so you can see what a framework does for you and where RAG can go wrong. In the lab, use a framework or build it yourself; either way the program must show which chunks it retrieved. The words differ between frameworks: what the lab calls a **chunk** is a *segment* in LangChain4j, and the **vector store** is an *embedding store*. Some frameworks report **similarity** (higher is closer); Spring AI reports **distance** (lower is closer).

## If something goes wrong

| Symptom | Likely cause |
|---|---|
| `401` from `/embeddings` | The key is not set in this terminal |
| `404` from `/embeddings` | A typo in the path or the model name |
| Every answer is "I can't find that" | The index is empty or points at the wrong folder; check the chunk count the indexer prints |
| `index.json` is several megabytes | Expected: about 135 chunks × 1,536 numbers, stored as text |
