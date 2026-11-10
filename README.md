# Strands Agents: Getting Started Labs

Hands-on Jupyter labs for setting up and learning [Strands Agents](https://strandsagents.com). They follow
[aws-samples/sample-building-with-strands-course](https://github.com/aws-samples/sample-building-with-strands-course)
and pin the same baseline, `strands-agents==1.59.0`.

| Lab | Topic | Course module |
|---|---|---|
| [00-setup](labs/00-setup.ipynb) | Environment, provider choice, credentials, first call | README / SETUP |
| [01-agent-loop](labs/01-agent-loop.ipynb) | The agent loop, results, history, `@tool` | 01-agent-loop |
| [02-model-providers](labs/02-model-providers.ipynb) | Bedrock / Anthropic / OpenAI / Ollama, config, structured output | 02-model-providers |
| [03-tools-and-mcp](labs/03-tools-and-mcp.ipynb) | Vended tools, MCP clients, tool filtering, executors | 03-mcp-tools |
| [04-callbacks-streaming](labs/04-callbacks-streaming.ipynb) | Callback handlers, silent mode, `stream_async` | 04-callbacks-streaming |
| [05-hooks](labs/05-hooks.ipynb) | Lifecycle hooks, guardrails, human-in-the-loop interrupts | 05-hooks |
| [06-sessions](labs/06-sessions.ipynb) | `FileSessionManager`, `agent.state`, S3 | 09-persistent-memory |
| [07-agents-as-tools](labs/07-agents-as-tools.ipynb) | Multi-agent composition | 10-agents-as-tools |

## Quick start

```bash
uv venv --python 3.12 .venv && source .venv/bin/activate     # Python 3.10+ required
uv pip install -r requirements.txt                            # or: pip install -r requirements.txt
python -m ipykernel install --user --name strands-labs --display-name "Strands Labs (.venv)"
cp .env.example .env                                          # choose LAB_PROVIDER
jupyter lab labs/
```

Run the labs in order. Every lab gets its model from `lab_config.get_model()`, so set `LAB_PROVIDER` once
(`bedrock`, `anthropic`, `openai`, or `ollama`) and all labs use it.

- **Bedrock:** valid AWS credentials (`aws configure` or `aws sso login`), region `us-east-1`.
- **Ollama:** use a tool-capable model, for example `ollama pull gemma4:latest`.

Labs write scratch files to `labs/workspace/` (git-ignored).

## Regenerating / running headless

```bash
LAB_PROVIDER=ollama jupyter nbconvert --to notebook --execute --inplace labs/*.ipynb
```
