FROM python:3.13-slim

# 1. Instalar o UV de forma eficiente
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

RUN apt update -y \
    && apt install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    default-libmysqlclient-dev \
    pkg-config \
    wait-for-it \
    curl \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivos de projeto (pyproject.toml e lockfile)
COPY pyproject.toml uv.lock* ./

# Instalar dependências com o uv
# --no-install-project evita que ele tente instalar seu código antes de copiá-lo
RUN uv sync --no-dev --frozen --no-install-project

COPY . .

# 6. Sincronizar o projeto final
RUN uv sync --no-dev --frozen

# Copiar e tornar executável o script de entrada
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
CMD ["uv", "run", "gunicorn", "--bind", ":8000", "kernel.wsgi"]