---

# 🧠 AI Agent SDK

A Python-based Software Development Kit (SDK) for creating AI agents that integrate seamlessly with **GitHub Actions** and support **local development** using `.env` files.

---

## ✨ Features

* 🔐 Secure handling of environment variables
* 📋 Support for required and optional config variables
* 🧱 Extensible base class for custom AI agents
* 🧾 Built-in logging with configurable log levels
* ✅ Compatible with GitHub Actions workflows
* 💻 Easy local development with `.env` support

---

## 🛠️ Prerequisites

* Python **3.9** or higher
* [`python-dotenv`](https://pypi.org/project/python-dotenv/) (for local development)
* GitHub repository (for CI/CD integration)

### Required Environment Variables

| Variable         | Description                             |
| ---------------- | --------------------------------------- |
| `OPENAI_API_KEY` | API key for the AI model (e.g., OpenAI) |
| `AGENT_NAME`     | Unique identifier for the AI agent      |
| `GITHUB_TOKEN`   | GitHub token for repository access      |

---

## 📦 Installation

```bash
git clone <repository-url>
cd <repository-directory>
pip install python-dotenv
```

### (Optional) Create a `.env` file for local development

```env
OPENAI_API_KEY=your_openai_key
AGENT_NAME=MyAIAgent
GITHUB_TOKEN=your_github_token
AGENT_LOG_LEVEL=DEBUG
MAX_RETRIES=3
TIMEOUT_SECONDS=30
```

---

## 🚀 Usage

### 🔧 Local Development

Ensure the `.env` file is properly configured. Then, run:

```bash
python ai_agent_sdk.py
```

### 🧪 Example Usage in Python

```python
from ai_agent_sdk import SampleAIAgent

agent = SampleAIAgent(config_path='.env')

task = {
    'input': 'Hello, AI Agent!'
}

result = agent.execute_task(task)
print(result)
```

#### ✅ Expected Output

```json
{
  "status": "success",
  "agent_name": "MyAIAgent",
  "processed_data": "Processed: Hello, AI Agent!",
  "github_token_used": true
}
```

---

## 🛠 GitHub Actions Integration

### 🧬 Example Workflow (`.github/workflows/ai-agent.yml`)

```yaml
name: AI Agent Workflow

on:
  push:
    branches:
      - main

jobs:
  run-ai-agent:
    runs-on: ubuntu-latest
    env:
      OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
      AGENT_NAME: MyAIAgent
      GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      AGENT_LOG_LEVEL: DEBUG

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: |
          pip install --upgrade pip
          pip install python-dotenv

      - name: Run AI Agent
        run: python ai_agent_sdk.py
```

### 🔐 Adding GitHub Secrets

1. Go to your repository on GitHub.
2. Navigate to: **Settings → Secrets and variables → Actions → Secrets**
3. Add the required secrets:

   * `OPENAI_API_KEY`
   * `GITHUB_TOKEN`

---

## ⚙️ Configuration

| Variable          | Required | Default | Description                            |
| ----------------- | -------- | ------- | -------------------------------------- |
| `OPENAI_API_KEY`  | ✅        | —       | API key for AI integration             |
| `AGENT_NAME`      | ✅        | —       | Unique agent name                      |
| `GITHUB_TOKEN`    | ✅        | —       | GitHub repository access token         |
| `AGENT_LOG_LEVEL` | ❌        | INFO    | Log level: DEBUG, INFO, WARNING, ERROR |
| `MAX_RETRIES`     | ❌        | 3       | Max retry attempts                     |
| `TIMEOUT_SECONDS` | ❌        | 30      | Timeout for tasks in seconds           |

---

## 🧩 Extending the SDK

Create your own custom AI agent by subclassing `AIAgentSDK`:

```python
from ai_agent_sdk import AIAgentSDK
from typing import Dict, Any

class CustomAIAgent(AIAgentSDK):
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'status': 'success',
            'result': f"Custom processing of {task.get('input')}"
        }
```

---

## 📋 Logging

Uses Python's built-in `logging` module. The log level is set via `AGENT_LOG_LEVEL`. All logs are printed to stdout and viewable in local terminal or GitHub Actions logs.

---

## ❗ Error Handling

* If any required environment variable is missing, the SDK raises an `EnvironmentError`.
* Task-related errors are caught and returned with:

```json
{
  "status": "error",
  "message": "Detailed error message here"
}
```

---

## 🤝 Contributing

Contributions are welcome!
Submit a pull request or open an issue for bugs or feature suggestions.

---

## 📄 License

MIT License © \[Your Name or Organization]

---
