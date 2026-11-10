"""Shared model selection for the labs.

Every lab calls `get_model()` so you can switch providers in one place.
Set these in `.env` (copy `.env.example`) or your shell:

    LAB_PROVIDER   bedrock (default) | anthropic | openai | ollama
    LAB_MODEL_ID   optional override of the provider's default model id
"""

from __future__ import annotations

import os
from pathlib import Path

DEFAULT_MODEL_IDS = {
    # None = let Strands pick its built-in Bedrock default
    "bedrock": None,
    "anthropic": "claude-sonnet-5-5",
    "openai": "gpt-4o",
    "ollama": "gemma4:latest",
}


def _load_dotenv() -> None:
    """Minimal .env loader (no extra dependency). Shell vars win."""
    env_file = Path(__file__).with_name(".env")
    if not env_file.exists():
        return
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_dotenv()


def provider() -> str:
    return os.environ.get("LAB_PROVIDER", "ollama").lower()


def model_id() -> str | None:
    return os.environ.get("LAB_MODEL_ID") or DEFAULT_MODEL_IDS[provider()]


def get_model(**overrides):
    """Return a Strands model object for the configured provider."""
    p, mid = provider(), model_id()

    if p == "bedrock":
        from strands.models import BedrockModel

        kwargs = {"region_name": os.environ.get("AWS_REGION", "us-east-1"), **overrides}
        if mid:
            kwargs["model_id"] = mid
        return BedrockModel(**kwargs)

    if p == "anthropic":
        from strands.models.anthropic import AnthropicModel

        return AnthropicModel(
            client_args={"api_key": os.environ["ANTHROPIC_API_KEY"]},
            model_id=mid,
            max_tokens=overrides.pop("max_tokens", 2048),
            **overrides,
        )

    if p == "openai":
        from strands.models.openai import OpenAIModel

        return OpenAIModel(
            client_args={"api_key": os.environ["OPENAI_API_KEY"]},
            model_id=mid,
            **overrides,
        )

    if p == "ollama":
        from strands.models.ollama import OllamaModel

        return OllamaModel(
            host=os.environ.get("OLLAMA_HOST", "http://localhost:11434"),
            model_id=mid,
            **overrides,
        )

    raise ValueError(f"Unknown LAB_PROVIDER '{p}'. Use bedrock, anthropic, openai, or ollama.")


def describe() -> str:
    return f"provider={provider()} model_id={model_id() or '(Strands default)'}"
