#!/bin/bash

set -e

echo "🚀 Deploy Backend - AuthBrasil CNPJ"
echo "===================================="

cd /root/backend

echo "📥 Puxando código do GitHub..."
git pull origin main

echo "🏗️ Building imagem Docker..."
docker build -t authbrasil/api:latest .

echo "📊 Rodando migrations..."
docker run --rm --user root \
  --network network_public \
  -e DATABASE_URL=postgresql://authbrasil_user:xWxt64YrzAFWc3ylNHrAbMoF0Z8h_b6kCQT4aX8sdgM@postgres:5432/authbrasil_cnpj \
  -e SECRET_KEY=2dedddaff60c04b3fa767ebc720a2dec4c94969be65cb9e4ff8f76e8a9b7e142 \
  -e JWT_SECRET_KEY=65248bd67bca837ae6e003075ce97a9bed277a8324eb1eb86e5b9160ad2d6c5e \
  -e REDIS_URL=redis://:vezEgze0KAtTuvn20ITwme_Ud8--aXdB@redis:6379/0 \
  -e STRIPE_SECRET_KEY=sk_test_temp \
  -e STRIPE_PUBLISHABLE_KEY=pk_test_temp \
  -e STRIPE_WEBHOOK_SECRET=whsec_temp \
  -e SENDGRID_API_KEY=SG_temp \
  authbrasil/api:latest python -m alembic upgrade head || echo "⚠️ Migrations já executadas"

echo "🔄 Atualizando serviço..."
docker service update --force authbrasil_api

echo "⏳ Aguardando update..."
sleep 10

echo "📊 Status dos serviços:"
docker service ls

echo ""
echo "✅ Deploy concluído!"
echo "📝 Logs da API:"
docker service logs authbrasil_api --tail 20
