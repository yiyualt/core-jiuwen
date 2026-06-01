.PHONY: test check fix install

install:
	uv sync

test:
	uv run pytest tests/ -v $(TESTFLAGS)

check:
	uv run ruff check jiuwen/ tests/

fix:
	uv run ruff check --fix jiuwen/ tests/

type-check:
	uv run mypy jiuwen/
