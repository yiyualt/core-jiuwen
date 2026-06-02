## Context

4 个新组件，每个都是独立可测的 WorkflowComponent。

## Decisions

**1. QuestionerComponent**

```python
class QuestionerComponent(WorkflowComponent):
    def __init__(self, question: str, field_name: str):
        # 如果输入缺少 field_name，返回追问
        ...

    async def invoke(self, inputs, **kwargs) -> dict:
        value = inputs.get(self._field_name)
        if value:
            return {"output": value}
        return {"question": self._question, "field": self._field_name}
```

**2. IntentDetectionComponent**

```python
class IntentDetectionComponent(WorkflowComponent):
    def __init__(self, intents: dict[str, list[str]]):
        # intents = {"greeting": ["hello", "hi"], "farewell": ["bye"]}
        ...

    async def invoke(self, inputs, **kwargs) -> dict:
        query = inputs.get("query", "").lower()
        for intent, keywords in self._intents.items():
            if any(kw in query for kw in keywords):
                return {"intent": intent, "confidence": 1.0}
        return {"intent": "unknown", "confidence": 0.0}
```

**3. HTTPRequestComponent**

```python
class HTTPRequestComponent(WorkflowComponent):
    def __init__(self, url_template: str, method="GET"):
        # url_template = "https://api.example.com/{{endpoint}}"
        ...

    async def invoke(self, inputs, **kwargs) -> dict:
        url = self._render_template(self._url_template, inputs)
        resp = await http_client.request(self._method, url, json=inputs.get("body"))
        return {"status": resp.status, "body": resp.text}
```

**4. LoopComponent**

```python
class LoopComponent(WorkflowComponent):
    def __init__(self, max_iterations: int = 10):
        self._items = []  # accumulate items across iterations

    async def invoke(self, inputs, **kwargs) -> dict:
        item = inputs.get("item")
        if item:
            self._items.append(item)
        self._count += 1
        done = self._count >= self._max_iterations
        return {"items": list(self._items), "count": self._count, "done": done}
```
