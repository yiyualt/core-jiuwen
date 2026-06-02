# coding: utf-8
"""HTTPRequestComponent — makes HTTP requests from workflow pipelines."""

import string

from jiuwen.core.workflow.components.component import WorkflowComponent


class HTTPRequestComponent(WorkflowComponent):
    """Makes HTTP requests with template-based URLs.

    Supports {{variable}} substitution in URLs and JSON body.

    Usage::

        comp = HTTPRequestComponent("https://api.example.com/{{endpoint}}")
        result = await comp.invoke({"endpoint": "users", "body": {"name": "Alice"}})
        # → {"status": 200, "body": "..."}
    """

    def __init__(self, url_template: str, method: str = "GET", headers: dict | None = None):
        super().__init__()
        self._url_template = url_template
        self._method = method.upper()
        self._headers = headers or {}

    async def invoke(self, inputs: dict, **kwargs) -> dict:
        url = self._render(inputs)
        body = inputs.get("body")

        try:
            import aiohttp
        except ImportError:
            # Fallback to urllib for sync requests
            import json
            import urllib.request
            data = json.dumps(body).encode() if body else None
            req = urllib.request.Request(url, data=data, method=self._method, headers=self._headers)
            try:
                with urllib.request.urlopen(req, timeout=30) as resp:
                    return {"status": resp.status, "body": resp.read().decode("utf-8", errors="replace")}
            except Exception as e:
                return {"status": 0, "body": str(e), "error": str(e)}

        async with aiohttp.ClientSession() as session:
            try:
                async with session.request(
                    self._method, url, json=body, headers=self._headers, timeout=aiohttp.ClientTimeout(total=30)
                ) as resp:
                    text = await resp.text()
                    return {"status": resp.status, "body": text}
            except Exception as e:
                return {"status": 0, "body": str(e), "error": str(e)}

    def _render(self, inputs: dict) -> str:
        converted = self._url_template.replace("{{", "$").replace("}}", "")
        t = string.Template(converted)
        return t.safe_substitute(**{k: str(v) for k, v in inputs.items()})
