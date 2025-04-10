/api.corebrain.ai/
  ├── app/
  │   ├── main.py                   # Punto de entrada de la aplicación FastAPI
  │   ├── routers/                  # Rutas de la API
  │   │   ├── auth.py               # Endpoints de autenticación
  │   │   ├── chat.py               # Endpoints de conversaciones
  │   │   ├── users.py              # Endpoints de gestión de usuarios
  │   │   ├── integrations.py       # Endpoints para integraciones externas
  │   │   └── analytics.py          # Endpoints para analíticas
  │   ├── models/                   # Modelos de datos y esquemas Pydantic
  │   │   ├── user.py               # Modelo de usuarios
  │   │   ├── conversation.py       # Modelo de conversaciones
  │   │   ├── message.py            # Modelo de mensajes
  │   │   ├── api_key.py            # Modelo de llaves API
  │   │   └── integration.py        # Modelo de integraciones
  │   ├── core/                     # Configuración del núcleo
  │   │   ├── config.py             # Configuración general
  │   │   ├── security.py           # Configuración de seguridad y JWT
  │   │   └── logging.py            # Configuración de logs
  │   ├── services/                 # Lógica de negocio
  │   │   ├── ai_service.py         # Integración con Anthropic
  │   │   ├── auth_service.py       # Servicio de autenticación
  │   │   ├── chat_service.py       # Procesamiento de conversaciones
  │   │   └── analytics_service.py  # Recopilación y procesamiento de analíticas
  │   ├── database/                 # Acceso a base de datos
  │   │   ├── session.py            # Configuración de sesión de base de datos
  │   │   ├── crud/                 # Operaciones CRUD
  │   │   │   ├── user.py           # Operaciones para usuarios
  │   │   │   ├── conversation.py   # Operaciones para conversaciones
  │   │   │   └── message.py        # Operaciones para mensajes
  │   │   └── migrations/           # Migraciones de base de datos
  │   ├── middleware/               # Middleware personalizado
  │   │   ├── authentication.py     # Middleware de autenticación
  │   │   ├── rate_limiter.py       # Limitador de peticiones
  │   │   └── logging.py            # Middleware de logging
  │   └── utils/                    # Utilidades generales
  │       ├── helpers.py            # Funciones auxiliares
  │       ├── validators.py         # Validadores personalizados
  │       └── exceptions.py         # Excepciones personalizadas
  ├── tests/                        # Tests automatizados
  │   ├── conftest.py               # Configuración de pytest
  │   ├── test_auth.py              # Tests de autenticación
  │   ├── test_chat.py              # Tests de conversaciones
  │   └── test_analytics.py         # Tests de analíticas
  ├── alembic/                      # Configuración de Alembic para migraciones
  │   ├── versions/                 # Versiones de migraciones
  │   └── env.py                    # Entorno de Alembic
  ├── Dockerfile                    # Configuración para Docker
  ├── docker-compose.yml            # Configuración para Docker Compose
  ├── requirements.txt              # Dependencias Python
  ├── .env.example                  # Ejemplo de variables de entorno
  └── README.md                     # Documentación