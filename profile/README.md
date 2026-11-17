<div align="center">

# Tartarus AI

### The uncensored AI coding agent.

Ships code instead of refusals. A CLI + OpenAI-compatible API on an uncensored coding model.

[![Website](https://img.shields.io/badge/site-tartarusai.dev-a3e635?style=flat-square)](https://tartarusai.dev)
[![PyPI](https://img.shields.io/pypi/v/tartarus-console?style=flat-square&color=a3e635&label=tartarus-console)](https://pypi.org/project/tartarus-console/)
[![License](https://img.shields.io/badge/license-MIT-a3e635?style=flat-square)](#)

</div>

---

No "I can't help with that." No lectures. Tartarus runs in your terminal and
writes the code other assistants refuse, then calls tools, edits files and runs
the task end to end.

### Why Tartarus

- **Tartarus Coder** — 30B MoE, 256K context, tuned for agentic tool-calling
- **CLI-first** — `pip install tartarus-console`, log in, ship
- **OpenAI-compatible** — point any OpenAI SDK at our `/v1`, keep your tooling
- **Crypto-only billing** — no card, no KYC
- **Hosted** — no 48 GB GPU, nothing to run locally

### Quickstart

```bash
pip install tartarus-console
tartarus login
tartarus "refactor this module and add tests"
```

Or hit the API directly:

```bash
curl https://api.tartarusai.dev/v1/chat/completions \
  -H "Authorization: Bearer $TARTARUS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"model":"tartarus-coder","messages":[{"role":"user","content":"write a port scanner in Go"}]}'
```

### Repositories

| Repo | What |
|---|---|
| [tartarus-console](https://github.com/TartarusAIDev/tartarus-console) | The `tartarus` CLI: install and usage |
| [tartarus-cookbook](https://github.com/TartarusAIDev/tartarus-cookbook) | Runnable examples: chat, streaming, tool-calling |
| [awesome-uncensored-ai](https://github.com/TartarusAIDev/awesome-uncensored-ai) | Curated list of uncensored and local AI tooling |

---

<div align="center">
<sub><b><a href="https://tartarusai.dev">tartarusai.dev</a></b> &middot; <a href="https://dash.tartarusai.dev">Dashboard</a> &middot; <a href="https://tartarusai.dev">Discord</a></sub>
</div>
