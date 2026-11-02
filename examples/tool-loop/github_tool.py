"""A real tool for the lab: the last few commits of a public GitHub repository, from GitHub's REST API.

No key is needed for public repositories (60 requests an hour per address; set GITHUB_TOKEN for
more). Everything that can go wrong comes back as a result the model can read, never an exception:
a repository that does not exist (404), the rate limit (403), a name that is not owner/name.

    python3 github_tool.py kousen/ai-integration-course
    python3 github_tool.py nobody/no-such-repo

To use it in the loop: add GITHUB_TOOL to TOOLS and recent_commits to FUNCTIONS in tools.py
(or in your own tools module), and the schema's description tells the model when to call it.
"""
import json
import os
import re
import sys
import urllib.error
import urllib.request

GITHUB_TOOL = {"type": "function", "function": {
    "name": "recent_commits",
    "description": "The most recent commits in one of the person's public GitHub repositories. "
                   "Use this before saying anything about what they have worked on lately.",
    "parameters": {"type": "object",
                   "properties": {"repo": {"type": "string", "description": "owner/name, for example kousen/ai-integration-course"},
                                  "count": {"type": "integer", "description": "How many commits, 1 to 10", "minimum": 1, "maximum": 10}},
                   "required": ["repo"]}}}


def recent_commits(repo: str, count: int = 5) -> dict:
    if not re.fullmatch(r"[\w.-]+/[\w.-]+", repo or ""):
        return {"error": f"repo must be owner/name, got {repo!r}"}
    count = max(1, min(int(count), 10))
    req = urllib.request.Request(f"https://api.github.com/repos/{repo}/commits?per_page={count}",
                                 headers={"Accept": "application/vnd.github+json", "User-Agent": "cpsc415-tool-loop"})
    if os.environ.get("GITHUB_TOKEN"):
        req.add_header("Authorization", f"Bearer {os.environ['GITHUB_TOKEN']}")
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.load(resp)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {"error": f"no public repository named {repo!r}", "repo": repo}
        if e.code == 403:
            return {"error": "GitHub rate limit reached; try again in an hour or set GITHUB_TOKEN"}
        return {"error": f"GitHub answered {e.code}"}
    except (urllib.error.URLError, TimeoutError) as e:
        return {"error": f"could not reach GitHub: {e}"}
    return {"repo": repo, "commits": [{"sha": c["sha"][:7], "date": c["commit"]["author"]["date"][:10],
                                      "message": c["commit"]["message"].splitlines()[0][:100]} for c in data]}


if __name__ == "__main__":
    print(json.dumps(recent_commits(sys.argv[1] if len(sys.argv) > 1 else "kousen/ai-integration-course"), indent=1))
