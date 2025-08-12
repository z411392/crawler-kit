FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app
RUN uv venv -p 3.13
ENV PATH="/app/.venv/bin:$PATH"

ADD pyproject.toml pyproject.toml
RUN uv pip install -e ".[cli]"
RUN uv pip compile pyproject.toml --extra firebase

ADD prefect.toml prefect.toml
ADD src src