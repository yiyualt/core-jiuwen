# coding: utf-8
"""LLM client abstraction — configuration and client interface.

Provides:
- ModelClientConfig: connection parameters (provider, api_key, etc.)
- ModelRequestConfig: request parameters (model, temperature, etc.)
- LLMClient: abstract base class for LLM providers
- FakeLLMClient: test double with preprogrammed responses
"""

from abc import ABC, abstractmethod
from typing import AsyncIterator

from pydantic import BaseModel, Field


class ModelClientConfig(BaseModel):
    """Connection configuration for an LLM provider.

    Attributes:
        provider: Provider name (e.g., "openai", "anthropic").
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


class FakeLLMClient(LLMClient):
    """A fake LLM client that returns preprogrammed responses.

    Used in tests to avoid real API calls. Responses are returned
    in order, cycling when exhausted.

    Usage::

        client = FakeLLMClient(["Hello!", "How can I help?"])
        response = await client.chat([{"role": "user", "content": "Hi"}])
        assert response == "Hello!"
        assert client.call_count == 1
    """

    def __init__(self, responses: list[str] | None = None):
        self.responses: list[str] = responses or ["default response"]
        self.call_count: int = 0
        self.last_messages: list[dict] = []

    async def chat(self, messages: list[dict], config: ModelRequestConfig | None = None) -> str:
        """Return the next preprogrammed response."""
        self.last_messages = messages
        response = self.responses[self.call_count % len(self.responses)]
        self.call_count += 1
        return response

    async def chat_stream(self, messages: list[dict], config: ModelRequestConfig | None = None) -> AsyncIterator[str]:
        """Stream the preprogrammed response as a single chunk."""
        text = await self.chat(messages, config)
        yield text
