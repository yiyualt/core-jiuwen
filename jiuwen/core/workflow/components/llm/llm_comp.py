# coding: utf-8
"""LLMComponent — a workflow component that calls an LLM.

Takes a template-based prompt, fills it with input values, calls
the LLM, and returns the response.
"""

import string
from typing import Any

from pydantic import BaseModel

from jiuwen.core.foundation.llm import (
    ModelClientConfig,
    ModelRequestConfig,
    LLMClient,
    FakeLLMClient,
)
from jiuwen.core.workflow.components.component import WorkflowComponent


class LLMCompConfig(BaseModel):
    """Configuration for an LLM component.

    Attributes:
        model_client_config: Connection settings for the LLM provider.
        model_config: Request parameters (model name, temperature, etc.).
        template_content: List of message dicts with {{variable}} placeholders.
        output_config: Optional JSON Schema for the expected output format.
    """

    model_client_config: ModelClientConfig = ModelClientConfig()
    model_config: ModelRequestConfig = ModelRequestConfig()
    template_content: list[dict] = []
    output_config: dict | None = None


class LLMComponent(WorkflowComponent):
    """A workflow component that calls an LLM with template-based prompts.

    Template variables use {{variable}} syntax. At invoke time, they are
    replaced with values from the inputs dict.

    Usage::

        config = LLMCompConfig(
            model_client_config=ModelClientConfig(provider="test"),
            model_config=ModelRequestConfig(model="test-model"),
            template_content=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "{{query}}"},
            ],
        )
        client = FakeLLMClient(["Hello! I'm here to help."])
        comp = LLMComponent(config, client)
        result = await comp.invoke({"query": "Say hello"})
        # result = {"output": "Hello! I'm here to help."}
    """

    def __init__(self, config: LLMCompConfig, client: LLMClient | None = None):
        """Initialize the LLM component.

        Args:
            config: Component configuration including templates and model settings.
            client: LLM client to use. Defaults to FakeLLMClient if not provided.
        """
        super().__init__()
        self._config = config
        self._client = client or FakeLLMClient()

    @property
    def client(self) -> LLMClient:
        """Access the underlying LLM client (useful for test assertions)."""
        return self._client

    async def invoke(self, inputs: dict, **kwargs) -> dict:
        """Render the prompt template and call the LLM.

        Args:
            inputs: Input values that fill template placeholders.

        Returns:
            Dict with "output" key containing the LLM's text response,
            or a structured dict if output_config specifies "response" format.
        """
        messages = self._render_messages(inputs)
        request_config = self._config.model_config
        response = await self._client.chat(messages, request_config)

        if self._config.output_config:
            return {"output": response, "response": response}
        return {"output": response}

    async def stream(self, inputs: dict, **kwargs):
        """Stream the LLM response token by token."""
        messages = self._render_messages(inputs)
        async for chunk in self._client.chat_stream(messages, self._config.model_config):
            yield {"output": chunk}

    def _render_messages(self, inputs: dict) -> list[dict]:
        """Replace {{variable}} placeholders with actual values."""
        rendered = []
        for msg in self._config.template_content:
            content = msg.get("content", "")
            role = msg.get("role", "user")
            # Render {{var}} → actual value
            rendered_content = self._render_template(content, inputs or {})
            rendered.append({"role": role, "content": rendered_content})
        return rendered

    @staticmethod
    def _render_template(template: str, inputs: dict) -> str:
        """Render a {{variable}} template string with input values."""
        converted = template.replace("{{", "$").replace("}}", "")
        t = string.Template(converted)
        return t.safe_substitute(**inputs)
