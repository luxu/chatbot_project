#!/bin/bash
set -e

# Ativa o ambiente virtual criado pelo 'uv'
# Isso adiciona o diretório .venv/bin ao PATH do shell
. /app/.venv/bin/activate

# Aguardar PostgreSQL estar disponível
echo "Waiting for external database at ${DB_HOST}:${DB_PORT}..."
# wait-for-it db:5432 --timeout=60 --strict
# wait-for-it ${DB_HOST}:${DB_PORT} --timeout=60 --strict -- echo "Database is ready!"

# Executar migrações
# echo "Running migrations..."
# python manage.py migrate --noinput

# Coleta todos os arquivos estáticos para a pasta STATIC_ROOT
echo "Collecting static files..."
#python manage.py collectstatic --no-input --clear
echo "Static files collected."
# --no-input: Para não pedir confirmação (essencial para scripts)
# --clear: Para limpar a pasta de estáticos antes de copiar os novos arquivos

echo "Starting Django server..."
exec "$@"