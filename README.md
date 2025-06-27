# 🤖 AI Agent Action

[![GitHub release (latest Agent SDK)](https://img.shields.io/github/v/release/nhedger/agent-sdk?label=latest&logo=github&labelColor=374151&color=60a5fa)](https://github.com/marketplace/actions/ai-agent-action)
[![AI Agent Workflow](https://github.com/Algenix-Org/agent-sdk/actions/workflows/ai-agent.yml/badge.svg)](https://github.com/Algenix-Org/agent-sdk/actions/workflows/ai-agent.yml)


A **GitHub Action** for running AI-powered task automation within your workflows.

* ✅ **Free** for public repositories
* 💼 **Premium** plan coming for private repositories

---

## ✨ Features

* ⚙️ AI-driven task execution via OpenAI or custom models
* 🔐 Secure environment variable handling (`OPENAI_API_KEY`, `GITHUB_TOKEN`)
* 🆓 Free tier for public repositories
* 🚀 Extensible with custom agents via built-in SDK
* 🔧 Supports JSON input directly or via file
* 📈 Ideal for automating repetitive workflows with intelligence

---

## 💰 Pricing

| Plan             | Description                                     | Cost                          |
| ---------------- | ----------------------------------------------- | ----------------------------- |
| **Free Tier**    | Unlimited use in public repositories            | **Free**                      |
| **Premium Tier** | Use in private repositories + advanced features | **\$5/month** *(Coming Soon)* |

> 💡 *Premium version will be available on GitHub Marketplace.*

---

## 🔧 Installation

Add the action to your GitHub Actions workflow (see below).

---

## 🧱 Prerequisites

* A GitHub repository with Actions enabled
* GitHub Secret: `OPENAI_API_KEY`

---

## 🚀 Usage

### 📂 Example Workflow: `.github/workflows/ai-agent.yml`

```yaml
name: Run AI Agent

on:
  push:
    branches:
      - main

jobs:
  ai-agent:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run AI Agent Action
        uses: your-username/your-repo@v1
        with:
          task-input: '{"input": "Hello, AI Agent!"}'
          openai-api-key: ${{ secrets.OPENAI_API_KEY }}
          agent-name: MyAIAgent
          log-level: DEBUG
        id: ai-agent

      - name: Print Result
        run: echo "Result: ${{ steps.ai-agent.outputs.result }}"
```

---

## ⚙️ Configuration

### 🔐 Required Inputs

| Input            | Description                        |
| ---------------- | ---------------------------------- |
| `openai-api-key` | Your OpenAI API key (`secrets`)    |
| `agent-name`     | Unique name for the agent instance |

### 🧩 Optional Inputs

| Input        | Description                                             | Default |
| ------------ | ------------------------------------------------------- | ------- |
| `task-input` | JSON-formatted task input                               | `{}`    |
| `task-file`  | Path to a JSON file containing the task definition      | —       |
| `log-level`  | Logging verbosity (`DEBUG`, `INFO`, `WARNING`, `ERROR`) | `INFO`  |

---

## 🧠 Extending the SDK

Want to go further?
Build custom agents by subclassing `AIAgentSDK` — full source available in this repository.

Example:

```python
from ai_agent_sdk import AIAgentSDK

class MyCustomAgent(AIAgentSDK):
    def execute_task(self, task):
        return {
            'status': 'success',
            'result': f"Custom result for input: {task.get('input')}"
        }
```

---

## 🛍️ GitHub Marketplace

**Coming Soon**

* Free for public repositories
* \$5/month per private repo

---

## 🤝 Contributing

Bug reports, ideas, or pull requests are welcome!
Submit an issue or PR on GitHub.

---

## 📄 License

MIT License

---

## Roadmap

- [ ] Deploy on Web
- [x] FOSS
- [ ] Release for Github Marketplace
