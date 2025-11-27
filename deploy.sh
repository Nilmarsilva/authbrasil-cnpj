#!/bin/bash
# Deploy Automático do Sistema ETL
# Execute na VPS: bash deploy.sh

set -e  # Parar em caso de erro

echo "🚀 Iniciando deploy do Sistema ETL..."
echo ""

# 1. Atualizar código
echo "📥 1. Atualizando código..."
cd /root/authbrasil-cnpj
git pull origin main
echo "✅ Código atualizado"
echo ""

# 2. Aplicar migrations
echo "🗄️  2. Aplicando migrations..."
docker exec authbrasil_api.1.kwdd4khfwu6h43blsejaumh7f alembic upgrade head
echo "✅ Migrations aplicadas"
echo ""

# 3. Rebuild Backend
echo "🔧 3. Rebuilding backend..."
docker build -t authbrasil/api:latest ./backend
docker service update --image authbrasil/api:latest authbrasil_api
echo "✅ Backend atualizado"
echo ""

# 4. Rebuild Frontend
echo "🎨 4. Rebuilding frontend..."
docker build -t authbrasil/frontend:latest ./frontend
docker service update --image authbrasil/frontend:latest authbrasil_frontend
echo "✅ Frontend atualizado"
echo ""

# 5. Verificar serviços
echo "🔍 5. Verificando serviços..."
sleep 5
docker service ls | grep authbrasil
echo ""

# 6. Instruções finais
echo "✅ Deploy concluído!"
echo ""
echo "📋 PRÓXIMOS PASSOS:"
echo ""
echo "1. Criar superuser (se ainda não criou):"
echo "   docker exec -it databases_postgres.1.mrttx12uwquw44ho80kojdweo psql -U authbrasil_user -d authbrasil_cnpj"
echo "   UPDATE users SET is_superuser = true WHERE email = 'seu@email.com';"
echo ""
echo "2. Testar:"
echo "   https://app.authbrasil.app.br/admin/etl"
echo ""
echo "3. Ver logs (se necessário):"
echo "   docker service logs -f authbrasil_api --tail 50"
echo ""
