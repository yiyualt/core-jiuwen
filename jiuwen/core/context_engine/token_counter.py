# coding: utf-8
"""TokenCounter — estimates token count for messages."""


class TokenCounter:
    """Estimates the token count of messages for context window management.

    Uses a simple heuristic (chars/4) which approximates English text.
    Falls back to char-based counting if tiktoken is not available.

    Usage::

        counter = TokenCounter()
        count = counter.count([{"role": "user", "content": "Hello, world!"}])
    """

    def __init__(self, model: str = "gpt-4"):
        self._model = model
        self._encoder = None
        try:
            import tiktoken
            self._encoder = tiktoken.encoding_for_model(model)
        except (ImportError, KeyError):
            pass  # fallback to char-based

    def count(self, messages: list[dict]) -> int:
        """Count tokens in a list of messages.

        Args:
            messages: List of message dicts with "content" key.

        Returns:
            Estimated token count.
        """
        if self._encoder:
            total = 0
            for msg in messages:
                content = msg.get("content", "")
                total += len(self._encoder.encode(content))
            return max(1, total)
        # Fallback: ~4 chars per token
        total = 0
        for msg in messages:
            total += len(msg.get("content", ""))
        return max(1, total // 4)
