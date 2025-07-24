export UV_PROJECT_ENVIRONMENT=functions/venv
# export IMAGE_REPOSITORY=""

.PHONY: \
	dev \
	format \
	lint \
	test \
	deploy \
	install \
	tree \
	freeze \
	keygen \
	help \
	build \
	push



format:
	@uvx ruff format .

dev:
	@firebase emulators:start --only functions,pubsub

lint:
	@uvx ruff check .

test:
	@uv run pytest -k "test_upload_pdf"

deploy:
	@firebase deploy --only functions

install:
	@uv pip install -e ".[firebase,cli,dev]"

tree:
	@tree -I 'build|__pycache__|*.egg-info|venv|.venv|*.log'

freeze:
	@uv pip compile pyproject.toml --extra firebase > functions/requirements.txt