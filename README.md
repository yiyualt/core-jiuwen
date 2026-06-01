# jiuwen Core

An educational reproduction of an AI agent SDK, rebuilt incrementally
from first principles.

## Introduction

**jiuwen Core** is a Python SDK for building AI agent applications, providing:
- Card/Config split architecture for metadata and runtime separation
- Workflow orchestration with component-based DAG execution
- LLM integration with async streaming
- Agent system with ReAct and Workflow agents
- Tool calling and multi-agent coordination

## Installation

```bash
pip install -e .
```

## Development

```bash
# Install with dev dependencies
uv sync

# Run tests
uv run pytest tests/ -v
```

## Version History

| Version | Feature |
|---------|---------|
| v0.0.1  | Core Primitives — BaseCard, package structure |

## License

This is an educational project. See the original openJiuwen Core for the
production SDK.
