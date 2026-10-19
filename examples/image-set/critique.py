"""Critique a generated image set with a vision model, then check the critique in code.

    python3 critique.py images/manifest.json                          # needs OPENROUTER_API_KEY
    python3 critique.py images/manifest.json --model xiaomi/mimo-v2.6-flash --out critique-mimo.json
    python3 critique.py --compare critique.json critique-mimo.json    # no key: where the two critics disagree

For every image the model gets the requirements from the manifest as a yes/no
checklist and must answer in JSON. The code then compares that checklist with the
requirements: every requirement answered, none invented, each one met. If the
manifest names an expected_text, the model is asked a second, narrower question
("write the title exactly as printed") and the code compares the answer to the
expected text. A critique that is not JSON is a failed critique, not a crash.

The critique is model output too. Two models disagreeing, or the narrow question
disagreeing with the checklist, is the signal to look at the image yourself.
"""
import argparse
import base64
import json
import os
import re
import sys
from pathlib import Path

DEFAULT_MODEL = "minimax/minimax-m3"
# Hidden reasoning is a per-model setting: see weeks/05/setup.md, section 2.
REASONING = {"xiaomi/mimo-v2.6-flash": {"enabled": False}}

CHECKLIST_PROMPT = """You are checking a generated image against the prompt that produced it.
Prompt: {prompt}

Answer every item below with true or false, strictly from what is visible in the image.
Reply with one JSON object and nothing else:
{{"checks": [{{"requirement": "<item text, copied exactly>", "met": true, "evidence": "<one short sentence>"}}, ...]}}

Items:
{items}"""

TEXT_PROMPT = "Write the largest piece of text in this image exactly as printed, character for character. Reply with that text only."


# ---------- plain code: no model, no key ----------

def extract_json(text: str) -> dict | None:
    """The JSON object inside a reply, or None. Models wrap JSON in fences or prose (Week 3)."""
    if text is None:
        return None
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if not m:
        return None
    try:
        obj = json.loads(m.group(0))
    except json.JSONDecodeError:
        return None
    return obj if isinstance(obj, dict) else None


def check(requirements: list[str], critique: dict | None) -> dict:
    """Compare the critic's checklist with the requirements. Returns what the code can say for sure."""
    if critique is None or not isinstance(critique.get("checks"), list):
        return {"ok": False, "problems": ["critique was not the JSON checklist that was asked for"],
                "unmet": [], "missing": list(requirements), "extra": []}
    answered = {}
    for c in critique["checks"]:
        if isinstance(c, dict) and isinstance(c.get("requirement"), str):
            answered[_norm(c["requirement"])] = c
    wanted = {_norm(r): r for r in requirements}
    missing = [r for k, r in wanted.items() if k not in answered]
    extra = [c["requirement"] for k, c in answered.items() if k not in wanted]
    unmet = [r for k, r in wanted.items() if k in answered and answered[k].get("met") is not True]
    problems = []
    if missing:
        problems.append(f"critic did not answer {len(missing)} requirement(s)")
    if extra:
        problems.append(f"critic answered {len(extra)} item(s) that were not asked")
    if unmet:
        problems.append(f"{len(unmet)} requirement(s) reported unmet")
    return {"ok": not problems, "problems": problems, "unmet": unmet, "missing": missing, "extra": extra}


def text_matches(expected: str, read: str | None) -> bool:
    """Case- and punctuation-insensitive comparison of the title the model read with the one asked for."""
    if read is None:
        return False
    return _norm(expected) == _norm(read)


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def disagreements(a: list[dict], b: list[dict]) -> list[dict]:
    """Images where two critique files reach different verdicts on any requirement or on the text."""
    out = []
    by_name = {e["name"]: e for e in b}
    for ea in a:
        eb = by_name.get(ea["name"])
        if eb is None:
            continue
        diffs = []
        va, vb = _verdicts(ea), _verdicts(eb)
        for req in sorted(set(va) | set(vb)):
            if va.get(req) != vb.get(req):
                diffs.append({"requirement": req, "a": va.get(req), "b": vb.get(req)})
        if ea.get("text_read") != eb.get("text_read"):
            diffs.append({"requirement": "<text read>", "a": ea.get("text_read"), "b": eb.get("text_read")})
        if diffs:
            out.append({"name": ea["name"], "diffs": diffs})
    return out


def _verdicts(entry: dict) -> dict:
    checks = (entry.get("critique") or {}).get("checks") or []
    return {c.get("requirement"): c.get("met") for c in checks if isinstance(c, dict)}


# ---------- the billed part ----------

def ask(client, model: str, image_path: Path, media_type: str, question: str, max_tokens: int = 800) -> tuple[str | None, dict]:
    """One vision call: text plus the image as a data URL, through the chat endpoint (Week 5's request)."""
    data = base64.b64encode(image_path.read_bytes()).decode()
    kwargs = {"reasoning": REASONING[model]} if model in REASONING else {}
    c = client.chat.send(model=model, max_tokens=max_tokens, messages=[{"role": "user", "content": [
        {"type": "text", "text": question},
        {"type": "image_url", "image_url": {"url": f"data:{media_type};base64,{data}"}}]}], **kwargs)
    usage = {"in": c.usage.prompt_tokens, "out": c.usage.completion_tokens} if c.usage else {}
    return c.choices[0].message.content, usage


def critique_set(client, model: str, manifest_path: Path) -> list[dict]:
    manifest = json.loads(manifest_path.read_text())
    results = []
    for entry in manifest:
        image = manifest_path.parent / entry["file"]
        items = "\n".join(f"- {r}" for r in entry["requirements"])
        raw, usage = ask(client, model, image, entry["media_type"],
                         CHECKLIST_PROMPT.format(prompt=entry["prompt"], items=items))
        critique = extract_json(raw)
        result = {"name": entry["name"], "model": model, "critique": critique, "raw": raw,
                  "usage": usage, "check": check(entry["requirements"], critique)}
        if entry.get("expected_text"):
            read, usage2 = ask(client, model, image, entry["media_type"], TEXT_PROMPT, max_tokens=100)
            result["text_read"] = (read or "").strip()
            result["text_matches"] = text_matches(entry["expected_text"], read)
            result["usage_text"] = usage2
        results.append(result)
        verdict = "ok" if result["check"]["ok"] else "; ".join(result["check"]["problems"])
        text = "" if "text_read" not in result else f"  title read: {result['text_read']!r} ({'match' if result['text_matches'] else 'MISMATCH'})"
        print(f"{entry['name']}: {verdict}  [{usage.get('in')} in / {usage.get('out')} out]{text}")
    return results


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("manifest", nargs="?", type=Path)
    ap.add_argument("--model", default=os.environ.get("CHAT_MODEL", DEFAULT_MODEL))
    ap.add_argument("--out", type=Path, default=Path("critique.json"))
    ap.add_argument("--compare", nargs=2, type=Path, metavar=("A.json", "B.json"))
    args = ap.parse_args()

    if args.compare:
        a, b = (json.loads(p.read_text()) for p in args.compare)
        diffs = disagreements(a, b)
        for d in diffs:
            print(d["name"])
            for x in d["diffs"]:
                print(f"  {x['requirement']}: {x['a']!r} vs {x['b']!r}")
        print(f"{len(diffs)} image(s) where the two critics disagree. Look at those yourself.")
        return
    if args.manifest is None:
        ap.error("manifest.json is required (or use --compare)")
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        sys.exit("OPENROUTER_API_KEY is not set; the critique is a billed vision call per image. Nothing checked.")
    from openrouter import OpenRouter

    results = critique_set(OpenRouter(api_key=key), args.model, args.manifest)
    args.out.write_text(json.dumps(results, indent=2) + "\n")
    bad = [r["name"] for r in results if not r["check"]["ok"] or r.get("text_matches") is False]
    print(f"{len(results) - len(bad)}/{len(results)} images pass the code's check; written to {args.out}")


if __name__ == "__main__":
    main()
