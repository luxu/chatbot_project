FROM python:3.13-slim

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

# Instalar o UV
RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
    && export PATH="/root/.local/bin:$PATH" \
    && /root/.local/bin/uv --version \
    && ln -s /root/.local/bin/uv /usr/local/bin/uv

# Copiar arquivos de projeto (pyproject.toml e lockfile)
COPY pyproject.toml uv.lock* ./

# Instalar dependências com o uv
RUN uv sync --no-dev --frozen

COPY . .

# Copiar e tornar executável o script de entrada
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
CMD [ "gunicorn", "--bind", ":8000", "kernel.wsgi" ]