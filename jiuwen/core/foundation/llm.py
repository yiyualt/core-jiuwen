# coding: utf-8
"""LLM client abstraction — configuration, client interface, and OpenAI implementation.

Provides:
- ModelClientConfig: connection parameters (provider, api_key, etc.)
- ModelRequestConfig: request parameters (model, temperature, etc.)
- LLMClient: abstract base class for LLM providers
- OpenAIClient: real implementation using the OpenAI SDK
"""

import os
from abc import ABC, abstractmethod
from typing import AsyncIterator

from pydantic import BaseModel, Field


class ModelClientConfig(BaseModel):
    """Connection configuration for an LLM provider.

    Attributes:
        provider: Provider name (e.g., "openai").
        api_key: API key for authentication.
        api_base: Base URL for the API endpoint.
        verify_ssl: Whether to verify SSL certificates.
    """

    provider: str = ""
    api_key: str = ""
    api_base: str = ""
    verify_ssl: bool = True


class ModelRequestConfig(BaseModel):
    """Request parameters for an LLM call.

    Attributes:
        model: Model name (e.g., "gpt-4", "claude-3").
        temperature: Sampling temperature (0.0-2.0).
        max_tokens: Maximum tokens in the response.
        top_p: Nucleus sampling parameter.
        stop: Optional stop sequences.
    """

    model: str = ""
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=1024, ge=1)
    top_p: float = Field(default=1.0, ge=0.0, le=1.0)
    stop: list[str] | None = None


class LLMClient(ABC):
    """Abstract base class for LLM provider clients.

    Subclasses implement chat() and chat_stream() for specific providers.
    """

    @abstractmethod
    async def chat(self, messages: list[dict], config: ModelRequestConfig | None = None) -> str:
        """Send a chat request and return the complete response.

        Args:
            messages: List of message dicts with "role" and "content" keys.
            config: Optional request configuration (uses defaults if None).

        Returns:
            The model's complete text response.
        """
        ...

    @abstractmethod
    async def chat_stream(self, messages: list[dict], config: ModelRequestConfig | None = None) -> AsyncIterator[str]:
        """Send a chat request and stream the response token by token.

        Args:
            messages: List of message dicts with "role" and "content" keys.
            config: Optional request configuration.

        Yields:
            Text chunks as they are received from the model.
        """
        ...


class OpenAIClient(LLMClient):
    """Real LLM client using the OpenAI SDK.

    Supports any OpenAI-compatible API (e.g., Azure, local models).

    Usage::

        # From environment variables
        client = OpenAIClient.from_env()

        # Explicit configuration
        client = OpenAIClient(ModelClientConfig(
            provider="openai",
            api_key="sk-...",
            api_base="https://api.openai.com/v1",
        ))

        # Chat
        response = await client.chat(
            [{"role": "user", "content": "Hello!"}],
            ModelRequestConfig(model="gpt-4", temperature=0.7),
        )
    """

    def __init__(self, client_config: ModelClientConfig):
        """Initialize the OpenAI client.

        Args:
            client_config: Connection configuration for the LLM provider.
        """
        try:
            import openai
        except ImportError:
            raise ImportError(
                "openai package is required. Install it with: pip install openai"
            )

        import openai

        http_client = None
        if not client_config.verify_ssl:
            import httpx
            http_client = httpx.AsyncClient(verify=False)

        self._config = client_config
        self._client = openai.AsyncOpenAI(
            api_key=client_config.api_key,
            base_url=client_config.api_base or None,
            http_client=http_client,
        )

    @classmethod
    def from_env(cls, env_file: str | None = None) -> "OpenAIClient":
        """Create an OpenAIClient from environment variables / .env file.

        Reads the following variables:
        - OPENAI_API_KEY (required)
        - OPENAI_API_BASE (default: https://api.openai.com/v1)
        - OPENAI_MODEL (default: gpt-4o)

        Args:
            env_file: Optional path to a .env file. If None, loads from .env in cwd.

        Returns:
            Configured OpenAIClient instance.
        """
        try:
            from dotenv import load_dotenv
        except ImportError:
            raise ImportError(
                "python-dotenv is required for .env loading. Install with: pip install python-dotenv"
            )

        if env_file:
            load_dotenv(env_file)
        else:
            load_dotenv()

        api_key = os.getenv("OPENAI_API_KEY", "")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY not found in environment. "
                "Set it in .env or export it directly."
            )

        return cls(ModelClientConfig(
            provider=os.getenv("OPENAI_PROVIDER", "openai"),
            api_key=api_key,
            api_base=os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1"),
            verify_ssl=os.getenv("OPENAI_SSL_VERIFY", "true").lower() != "false",
        ))

    async def chat(self, messages: list[dict], config: ModelRequestConfig | None = None) -> str:
        """Send a chat request and return the complete response."""
        cfg = config or ModelRequestConfig()
        if not cfg.model:
            cfg.model = os.getenv("OPENAI_MODEL", "gpt-4o")

        response = await self._client.chat.completions.create(
            model=cfg.model,
            messages=messages,
            temperature=cfg.temperature,
            max_tokens=cfg.max_tokens,
            top_p=cfg.top_p,
            stop=cfg.stop or None,
        )
        return response.choices[0].message.content or ""

    async def chat_stream(self, messages: list[dict], config: ModelRequestConfig | None = None) -> AsyncIterator[str]:
        """Stream the response token by token."""
        cfg = config or ModelRequestConfig()
        if not cfg.model:
            cfg.model = os.getenv("OPENAI_MODEL", "gpt-4o")

        stream = await self._client.chat.completions.create(
            model=cfg.model,
            messages=messages,
            temperature=cfg.temperature,
            max_tokens=cfg.max_tokens,
            top_p=cfg.top_p,
            stop=cfg.stop or None,
            stream=True,
        )
        async for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                yield content
