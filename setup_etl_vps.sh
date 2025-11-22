#!/bin/bash
# Setup ETL na VPS - Rodar como root
# Tempo estimado: 5 minutos

set -e  # Parar se der erro

echo "🚀 Iniciando configuração do ETL na VPS..."

# 1. Atualizar código
echo "📥 Atualizando código do GitHub..."
cd /root/backend
git pull origin main

# 2. Instalar dependências Python
echo "📦 Instalando dependências..."
pip3 install httpx beautifulsoup4 lxml

# 3. Criar banco de dados (se não existir)
echo "💾 Criando banco de dados..."
sudo -u postgres psql -c "CREATE DATABASE authbrasil_cnpj" 2>/dev/null || echo "Banco já existe"

# 4. Rodar migrations
echo "🗄️  Criando tabelas..."
cd /root/backend
alembic upgrade head

# 5. Criar diretório para dados
echo "📁 Criando diretório de dados..."
mkdir -p /root/data/receita

# 6. Verificar tabelas criadas
echo "✅ Verificando tabelas..."
sudo -u postgres psql -d authbrasil_cnpj -c "\dt"

echo ""
echo "✅ Setup concluído!"
echo ""
echo "🚀 Para rodar o ETL:"
echo "cd /root"
echo "nohup python3 backend/run_etl.py --truncate > etl.log 2>&1 &"
echo ""
echo "📊 Para monitorar:"
echo "tail -f etl.log"
