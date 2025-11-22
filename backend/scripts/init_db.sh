#!/bin/bash
# Script para inicializar o banco de dados
# Uso: bash scripts/init_db.sh

echo "🔧 Iniciando banco de dados..."
echo ""

# 1. Criar migration inicial
echo "📝 Criando migration inicial..."
cd /app
alembic revision --autogenerate -m "Initial migration - create all tables"

# 2. Aplicar migrations
echo "🚀 Aplicando migrations..."
alembic upgrade head

# 3. Criar usuário admin
echo "👤 Criando usuário admin..."
python scripts/create_admin.py

echo ""
echo "✅ Banco inicializado com sucesso!"
echo "📧 Email admin: admin@authbrasil.com.br"
echo "🔑 Senha admin: Admin@123"
echo ""
echo "⚠️  IMPORTANTE: Altere a senha após o primeiro login!"
