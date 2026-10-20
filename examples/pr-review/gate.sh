#!/bin/sh
# Release gate: the no-key tests and the linter must pass before a push leaves this machine.
#
# Install as a pre-push hook (runs on every `git push`, in the repository root):
#   cp path/to/ai-integration-course/examples/pr-review/gate.sh .git/hooks/pre-push
#   chmod +x .git/hooks/pre-push
# Run by hand:  sh gate.sh
#
# The key is removed from the environment so tests that call a model are skipped,
# not billed. A gate that depends on a paid call will be turned off the first time
# someone is in a hurry; keep it fast and free. The same two commands run in CI
# (see gate.yml). Exit non-zero stops the push.
set -e
cd "$(git rev-parse --show-toplevel)"

echo "gate: ruff"
ruff check .

echo "gate: tests without a key"
env -u OPENROUTER_API_KEY python3 -m pytest -q

echo "gate: passed"
