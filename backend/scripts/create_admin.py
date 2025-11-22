"""
Script para criar usuário administrador
Uso: python scripts/create_admin.py
"""

import asyncio
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
sys.path.append(str(Path(__file__).parent.parent))

from app.db.session import async_session
from app.models.user import User
from app.core.security import get_password_hash
from sqlalchemy import select


async def create_admin_user():
    """Cria o usuário administrador se não existir"""
    
    admin_email = "admin@authbrasil.com.br"
    admin_password = "Admin@123"  # MUDAR DEPOIS!
    admin_name = "Administrador"
    
    async with async_session() as session:
        # Verificar se admin já existe
        result = await session.execute(
            select(User).where(User.email == admin_email)
        )
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            print(f"✅ Usuário admin já existe: {admin_email}")
            print(f"   ID: {existing_user.id}")
            print(f"   Nome: {existing_user.full_name}")
            return
        
        # Criar novo usuário admin
        admin_user = User(
            email=admin_email,
            full_name=admin_name,
            hashed_password=get_password_hash(admin_password),
            is_active=True,
            is_superuser=True,
            is_verified=True,
        )
        
        session.add(admin_user)
        await session.commit()
        await session.refresh(admin_user)
        
        print("=" * 60)
        print("✅ USUÁRIO ADMIN CRIADO COM SUCESSO!")
        print("=" * 60)
        print(f"Email: {admin_email}")
        print(f"Senha: {admin_password}")
        print(f"ID: {admin_user.id}")
        print("=" * 60)
        print("⚠️  IMPORTANTE: Altere a senha após o primeiro login!")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(create_admin_user())
