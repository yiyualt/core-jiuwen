# coding: utf-8
"""StreamEmitter — async streaming output for agents.

Provides an async-iterable queue that producers emit chunks into
and consumers iterate over.
"""

import asyncio
from typing import Any, AsyncIterator


class StreamEmitter:
    """Async stream emitter for real-time agent output.

    Usage::

        emitter = StreamEmitter()

        # Producer
        async def produce():
            await emitter.emit("Hello ")
            await emitter.emit("World!")
            await emitter.close()

        # Consumer
        async for chunk in emitter:
            print(chunk, end="")
    """

    def __init__(self):
        self._queue: asyncio.Queue[Any] = asyncio.Queue()
        self._closed = False

    async def emit(self, chunk: Any) -> None:
        """Emit a chunk of data to the stream.

        Args:
            chunk: Data to emit. None signals end of stream.
        """
        await self._queue.put(chunk)

    async def close(self) -> None:
        """Signal the end of the stream."""
        if not self._closed:
            self._closed = True
            await self._queue.put(None)

    def __aiter__(self) -> AsyncIterator[Any]:
        return self

    async def __anext__(self) -> Any:
        if self._closed and self._queue.empty():
            raise StopAsyncIteration
        chunk = await self._queue.get()
        if chunk is None:
            raise StopAsyncIteration
        return chunk
