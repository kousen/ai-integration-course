# Week 1 setup: start with a laptop

We will do this together in class. Stop at a checkpoint if something fails and show Ken the error. You do not need to buy a monthly Claude subscription. This guide uses your own OpenRouter account and the course's existing `orclaude` launcher.

**What you need today:** a browser, a terminal, Git, a GitHub account, Claude Code, and working model access. VS Code is useful but optional today. No Node.js, Python, JDK, Docker, WSL, or local model download is needed for the browser lab. Students who already use another supported environment should keep it; ask Ken for the matching commands.

## 1. Accounts and a small budget

Open [GitHub](https://github.com/) and sign in or create an account. Keep a browser tab signed in. Your source code will be shared; use the supplied public-domain poem rather than personal information.

Open [OpenRouter](https://openrouter.ai/) and create or sign in to your own account. The classroom candidate is [`minimax/minimax-m3`](https://openrouter.ai/minimax/minimax-m3), which uses pay-as-you-go API billing. It completed a plan/build/change rehearsal through `orclaude`, and the resulting trainer passed browser behavior checks; use the model he announces in class, with the spending cap below.

- For paid access, the syllabus budgets an initial **$20 credit purchase** and roughly **$50 for the semester**, both planning estimates rather than promises of actual cost. Confirm the checkout total before buying; fees may apply.
- Create a course key at [API keys](https://openrouter.ai/settings/keys). Give it a recognizable name such as `cpsc415`. Set a **$5 spending limit for the initial lab** and no recurring reset if the interface offers that choice. The cap belongs to this key; your account balance is separate. Review usage before deciding whether to raise it for later work.
- If payment or account access is a problem, tell Ken privately. Pair for the activity while he helps resolve access. Do not exchange API keys or buy a subscription as a troubleshooting step.
- Free models may be usable, but have request and availability limits. A single agent task can make many requests. Ken will select the day's default and fallback; do not silently switch to a more expensive model.

**Instructor fallback:** `xiaomi/mimo-v2.5` also completed a trainer build and browser checks during preparation. Both routes are API-billed; use the fallback only when directed, with your spending cap in place. One successful rehearsal does not guarantee service availability during class.

Copy your API key only into the hidden terminal prompt in Step 4. Never put it in a chat prompt, source file, screenshot, or Git commit. This guide keeps it in the current terminal session rather than writing it to a file.

## 2. Install Git and Claude Code

### macOS: Terminal

Open **Terminal** using Spotlight. Run these commands one at a time:

```bash
git --version
```

If macOS asks to install Command Line Developer Tools, accept the installation and let it finish. If installation stalls, show Ken rather than repeating it. If no installation prompt appears and Git is missing, run `xcode-select --install`. Reopen Terminal afterward and repeat `git --version`.

Install Claude Code using the official native installer:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

Open a new Terminal window and check:

```bash
claude --version
```

If the command cannot be found, follow the installer's PATH instructions. A temporary fix for this terminal is:

```bash
export PATH="$HOME/.local/bin:$PATH"
claude --version
```

### Windows: PowerShell

Open **PowerShell** from Start. These instructions are for PowerShell, whose prompt typically begins with `PS`. They are not Command Prompt or Git Bash commands.

Install [Git for Windows](https://git-scm.com/download/win), including its Git Bash component. Use the normal installer defaults. This supplies both version control and a Bash shell the agent can use. Close and reopen PowerShell, then check:

```powershell
git --version
```

Install Claude Code using the official native installer:

```powershell
irm https://claude.ai/install.ps1 | iex
```

Close and reopen PowerShell, then check:

```powershell
claude --version
```

If the launcher is not on PATH, follow the installer's directions. For the current session only, you can try:

```powershell
$env:Path = "$env:USERPROFILE\.local\bin;" + $env:Path
claude --version
```

**Checkpoint A:** both version commands print a version. Installation alone does not establish that billing or model access is configured.

## 3. Download the course and create your own project

Use a folder owned by you, outside a cloud-synced Desktop/Documents folder if possible. The commands below create `cpsc415` inside your home directory. If a directory already exists, use it rather than deleting work.

### macOS

```bash
mkdir -p ~/cpsc415
cd ~/cpsc415
git clone https://github.com/kousen/ai-integration-course.git
mkdir lyrics-trainer
cd lyrics-trainer
git init -b main
cp ../ai-integration-course/weeks/01/sonnet18.txt lyrics.txt
printf '.env\n.env.*\n!.env.example\n.claude/settings.local.json\n.DS_Store\n' > .gitignore
```

### Windows PowerShell

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\cpsc415"
Set-Location "$env:USERPROFILE\cpsc415"
git clone https://github.com/kousen/ai-integration-course.git
New-Item -ItemType Directory lyrics-trainer
Set-Location lyrics-trainer
git init -b main
Copy-Item ..\ai-integration-course\weeks\01\sonnet18.txt lyrics.txt
@('.env', '.env.*', '!.env.example', '.claude/settings.local.json', '.DS_Store') | Set-Content .gitignore
```

The supplied source remains `sonnet18.txt` in the course repository; your application reads its local copy named `lyrics.txt`.

If you already cloned the course, skip `git clone`. Run `git pull` **inside the course folder** to get updates, then return to your `lyrics-trainer` folder. Your work belongs in `lyrics-trainer`, not in the instructor's course repository.

Both platforms: configure an identity for this repository, replacing the example values. You can use the GitHub-provided noreply address from your GitHub email settings.

```bash
git config user.name "Your Name"
git config user.email "YOUR_GITHUB_EMAIL"
git add .gitignore lyrics.txt
git commit -m "Start Week 1 exercise"
git switch -c first-build
```

**Checkpoint B:** `git branch --show-current` says `first-build`; the folder contains `lyrics.txt` and `.gitignore`. You do not need the full artifact-chain template for this first exercise.

## 4. Launch with your OpenRouter key

Use the same terminal for entering the key and starting the agent. The hidden prompt will not show the key as you type or paste. Press Enter when finished.

### macOS (the default zsh shell)

```zsh
read -s "OPENROUTER_API_KEY?Paste your OpenRouter key (hidden): "
export OPENROUTER_API_KEY
printf '\n'
bash ../ai-integration-course/scripts/orclaude "minimax/minimax-m3"
```

### Windows PowerShell

```powershell
$courseKey = Read-Host "Paste your OpenRouter key" -AsSecureString
$env:OPENROUTER_API_KEY = [System.Net.NetworkCredential]::new('', $courseKey).Password
Remove-Variable courseKey
& ..\ai-integration-course\scripts\orclaude.bat "minimax/minimax-m3"
```

The commands use the API-billed MiniMax M3 candidate. If Ken selects another model, substitute its exact slug and keep the quotes. On the initial launch, complete any onboarding and trust **your exercise folder**. Keep normal permission prompts; do not enable bypass mode for this lab.

Inside the session, run `/status`. Check the model and that the API destination is OpenRouter. Ask:

```text
Read lyrics.txt. Tell me how many nonblank lines it contains.
Do not change any files yet.
```

There are 14 lines. In your browser, open [OpenRouter Activity](https://openrouter.ai/activity) and confirm a request appeared for the chosen model. Do not use the model's answer to “Who are you?” as proof of routing. Avoid sharing your account screen with other students.

**Checkpoint C:** the agent read the file, the result is correct, and the usage record identifies the intended model. Continue to the [lab](lab.md).

### Starting again later

Open your `lyrics-trainer` folder in a terminal. In a new terminal, repeat the hidden key-entry commands above. Use the same launcher with the selected model; add `--continue` if you want to resume the most recent session in that folder. Typing plain `claude` does not apply this wrapper's settings.

### Unknown-model context warning

Claude Code may say an OpenRouter model is not described by its built-in catalog and assume a 200,000-token context window. That metadata warning alone does not mean the connection failed. Keep the default for this small lab. For a model whose published window supports it, the launcher also passes a quoted `[1m]` suffix through unchanged, for example `orclaude "deepseek/deepseek-v4-pro-0813[1m]"`. Keep the quotes in zsh. Ask Ken before changing context limits; do not disable enforcement as a troubleshooting shortcut.

## If something goes wrong

| Symptom | Next action |
|---|---|
| `git` or `claude` not found | Reopen the terminal, check PATH, and show Ken the installer output. |
| “Set OPENROUTER_API_KEY” | Repeat hidden key entry in this terminal; never print the variable to check it. |
| It asks for a paid Claude plan | Stop and check that you launched through `orclaude`, not plain `claude`. Ask Ken to inspect conflicting settings before changing account configuration. |
| Model not found | Compare the exact slug with the catalog and ask Ken to check routing. |
| 401 / authentication failure | Check that the key is valid and that the wrapper ran; do not paste the key into the agent. |
| 402 / insufficient credits | Check account balance and the course key's limit. Ask before buying more or raising a cap. |
| 429 / rate limit | Pause; use the instructor's fallback when directed. Creating more keys is not a solution to an account limit. |
| Git Bash not found on Windows | Verify Git for Windows is installed. Ken can check its installation path against the official setup guide. |
| Browser sign-in/Git push fails | Keep the local commits; show Ken the error. You can complete the build without a working push. |
| Managed laptop, unsupported OS, or no install permissions | Pair for the activity and arrange a supported environment with Ken. Do not disable institutional protections. |

An existing Claude subscription or a confirmed Enterprise seat can be an alternative with Ken's help. A free Claude chat account alone is not this guide's access route. The optional instructor `/design` demonstration uses Anthropic access and is not required on OpenRouter.

## Sources

Installation and routing documentation checked September 9, 2026. Commands and service interfaces can change; Ken will rehearse the classroom setup before the session.

- [Claude Code installation](https://code.claude.com/docs/en/setup) and [terminal guide](https://code.claude.com/docs/en/terminal-guide)
- [OpenRouter with Claude Code](https://openrouter.ai/docs/cookbook/coding-agents/claude-code-integration)
- [OpenRouter credit and rate limits](https://openrouter.ai/docs/api_reference/limits)
- [Ken's companion launcher scripts](https://github.com/kousen/claude-code-up-and-running-examples/tree/main/scripts)
