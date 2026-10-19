"""Generate an image set through OpenRouter's Image API and write a manifest.

    python3 generate.py prompts.json --out images            # needs OPENROUTER_API_KEY
    python3 generate.py prompts.json --model google/gemini-3.1-flash-lite-image --out images-nb

prompts.json is a list of {"name", "prompt", "seed", "requirements", ...}; see the
copy beside this file. One billed call per prompt (FLUX.2 klein: about $0.014 each
on October 19, 2026; the reply's usage.cost is what you actually paid). The manifest
records prompt, seed, model, media type, file and cost for every image, so the
critic and the checker never have to guess what was asked for.
"""
import argparse
import base64
import json
import os
import sys
import time
from pathlib import Path

DEFAULT_MODEL = "black-forest-labs/flux.2-klein-4b"
EXT = {"image/jpeg": "jpg", "image/png": "png", "image/webp": "webp"}


def generate_one(client, model: str, prompt: str, seed: int, aspect_ratio: str) -> dict:
    """One Image API call. Returns bytes, media type and cost. The SDK does the POST to /api/v1/images."""
    r = client.images.generate(model=model, prompt=prompt, aspect_ratio=aspect_ratio, seed=seed)
    item = r.data[0]
    return {"bytes": base64.b64decode(item.b64_json), "media_type": item.media_type,
            "cost": getattr(r.usage, "cost", None)}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("prompts", type=Path)
    ap.add_argument("--out", type=Path, default=Path("images"))
    ap.add_argument("--model", default=os.environ.get("IMAGE_MODEL", DEFAULT_MODEL))
    ap.add_argument("--aspect-ratio", default="1:1")
    args = ap.parse_args()

    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        sys.exit("OPENROUTER_API_KEY is not set; image generation is a billed call. Nothing generated.")
    # The one dependency, named in spec.md with its reason. Imported here so the
    # no-key path (and the tests) never need it.
    from openrouter import OpenRouter

    client = OpenRouter(api_key=key)
    prompts = json.loads(args.prompts.read_text())
    args.out.mkdir(parents=True, exist_ok=True)
    manifest, total = [], 0.0
    for p in prompts:
        t0 = time.time()
        g = generate_one(client, args.model, p["prompt"], p["seed"], args.aspect_ratio)
        ext = EXT.get(g["media_type"], "bin")
        path = args.out / f"{p['name']}.{ext}"
        path.write_bytes(g["bytes"])
        entry = {**p, "model": args.model, "aspect_ratio": args.aspect_ratio, "file": path.name,
                 "media_type": g["media_type"], "cost": g["cost"], "seconds": round(time.time() - t0, 1)}
        manifest.append(entry)
        total += g["cost"] or 0.0
        print(f"{path}  {g['media_type']}  seed={p['seed']}  ${g['cost']}  {entry['seconds']}s")
    (args.out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"{len(manifest)} images, ${total:.4f} total, manifest in {args.out / 'manifest.json'}")


if __name__ == "__main__":
    main()
