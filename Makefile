sync:
	uv sync

setup:
	uv tool install ruff
	uv tool install ipython

lint:
	ruff check