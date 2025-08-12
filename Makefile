export UV_PROJECT_ENVIRONMENT=src/venv
export IMAGE_REPOSITORY=asia-east1-docker.pkg.dev/crawler-kit/crawler-kit/test

.PHONY: \
	dev \
	format \
	lint \
	test \
	deploy \
	install \
	tree \
	freeze \
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
	@uv pip compile pyproject.toml --extra firebase > src/requirements.txt

push:
	@docker push $(IMAGE_REPOSITORY):latest

build:
	@docker build --platform=linux/amd64 . -t $(IMAGE_REPOSITORY):latest