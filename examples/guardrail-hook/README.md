# A guardrail hook

A hook is a program Claude Code runs at a fixed point in its own loop, whether or not the agent remembers a rule. This one runs **before every Edit, Write, and Bash call** and says no to three things:

| Rule | Why |
|---|---|
| No edits to `images/` or `expected.json` | They are the answer key. A test that passes because the agent changed the expected value proves nothing. |
| No `rm -r`, `git push --force`, `git reset --hard`, `git checkout --`, `git clean` | Destructive. If one is really needed, a person runs it. |
| No `pip install` / `uv add` / `npm install` of a package that `spec.md` does not mention | The course rule: every dependency is named in the spec, with a reason, before it is installed. |

Everything else is allowed. The hook exits with code 2 to block a call and prints the reason to standard error, which Claude Code shows the agent. Exit 0 lets the call through. Exit 1 would mean "the hook itself failed" and would **not** block, so a bug in the guard fails open. Test it before you rely on it.

## Install

From the root of your project:

```bash
mkdir -p .claude/hooks
cp path/to/ai-integration-course/examples/guardrail-hook/guard.py .claude/hooks/guard.py
cp path/to/ai-integration-course/examples/guardrail-hook/settings.json .claude/settings.json
git add .claude/hooks/guard.py .claude/settings.json
```

`settings.json` is shared project configuration and is committed; `.claude/settings.local.json` (your key and model) stays ignored. If your repository already has a `.claude/settings.json`, merge the `hooks` block into it. Restart Claude Code after adding or changing a hook.

The command is `python3 .claude/hooks/guard.py`, run from the project folder. On Windows, if `python3` is not on your path, change it to `python`. If you have no Python at all, ask the agent to port `guard.py` to your language with the same three rules, and check it with the tests below.

## Test it without the agent

Claude Code sends the hook one JSON object on standard input describing the pending call. You can send one yourself:

```bash
echo '{"tool_name":"Edit","tool_input":{"file_path":"images/expected.json"}}' | python3 .claude/hooks/guard.py; echo "exit $?"
# ... is the answer key. Fix the code, not the expected values. ...   exit 2
echo '{"tool_name":"Bash","tool_input":{"command":"pip install requests"}}' | python3 .claude/hooks/guard.py; echo "exit $?"
# requests is not in spec.md. Add it under Dependencies ...            exit 2
echo '{"tool_name":"Bash","tool_input":{"command":"python3 -m pytest"}}' | python3 .claude/hooks/guard.py; echo "exit $?"
#                                                                       exit 0
```

Then test it with the agent: ask it to change a number in `expected.json` and watch it get refused.

## What this is not

It is a tripwire, not a wall. The agent can still write to the answer key through a command the patterns do not match, and a hook that crashes fails open. Permissions (what the agent may run at all) and the repository's history (what actually changed) are the other two layers. Use all three.

Hooks are described in Chapter 6 of Prof. Kousen's *Claude Code: Up and Running* and in the [Claude Code hooks documentation](https://code.claude.com/docs/en/hooks).
