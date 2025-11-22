"""
Application Configuration
Manages environment variables and application settings
"""

from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Project Info
    PROJECT_NAME: str = "AuthBrasil CNPJ API"
    PROJECT_DESCRIPTION: str = """
## API completa para consultas de CNPJ automatizadas no Brasil

Acesse dados oficiais da Receita Federal de forma programática.

### Recursos Principais

- 🔍 **Consultas por CNPJ** - Dados completos de empresas brasileiras
- 📊 **Dados Estruturados** - Respostas em JSON padronizadas
- ⚡ **Alta Performance** - Respostas em menos de 100ms
- 🔒 **Segurança** - Autenticação via Bearer Token
- 🔄 **Sempre Atualizado** - Sincronização mensal com Receita Federal

### Autenticação

Todas as requisições autenticadas devem incluir o header:

```
Authorization: Bearer SUA_API_KEY
```

Obtenha sua API Key criando uma conta em [authbrasil.app.br](https://authbrasil.app.br)

### Rate Limits

- **Starter:** 500 requisições/mês
- **Pro:** 5.000 requisições/mês  
- **Enterprise:** 50.000 requisições/mês

### Suporte

- **Email:** suporte@authbrasil.com.br
- **Docs:** [docs.authbrasil.app.br](https://docs.authbrasil.app.br)
"""
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # API
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Database
    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "https://app.authbrasil.app.br",
        "http://app.authbrasil.app.br"
    ]
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_LOGIN_ATTEMPTS: int = 5
    
    # Stripe
    STRIPE_SECRET_KEY: str = ""
    STRIPE_PUBLISHABLE_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""
    
    # Email
    EMAIL_FROM: str = "noreply@authbrasil.com.br"
    EMAIL_PROVIDER: str = "sendgrid"
    SENDGRID_API_KEY: str = ""
    
    # ETL
    RECEITA_BASE_URL: str = "https://arquivos.receitafederal.gov.br/dados/cnpj/dados_abertos_cnpj/"
    ETL_CHUNK_SIZE: int = 100000
    ETL_TEMP_DIR: str = "/tmp/etl_receita"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


settings = Settings()
