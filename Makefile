sync:  ## Sync the requirements
	uv sync

setup:  ## Setup tools needed
	uv tool install ruff
	uv tool install ipython

lint:  ## Lint and format with Ruff
	@ruff check
	@ruff format . --check
	@ruff format .



#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := show-help
.PHONY: show-help
show-help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
