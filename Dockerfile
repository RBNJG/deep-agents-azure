FROM ghcr.io/astral-sh/uv:0.13.6 AS uv
FROM python:3.12-slim

COPY --from=uv /uv /uvx /usr/local/bin/
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"
WORKDIR /app
COPY pyproject.toml uv.lock README.md LICENSE ./
COPY apps ./apps
COPY packages ./packages
RUN uv sync --locked --no-dev --no-editable \
    && groupadd --gid 10001 paw \
    && useradd --uid 10001 --gid paw --no-create-home paw
USER 10001:10001
EXPOSE 8000
HEALTHCHECK --interval=10s --timeout=3s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/ready', timeout=2)"
CMD ["paw-api"]
