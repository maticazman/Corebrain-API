# README.md

# CoreBrain API

API para procesamiento de mensajes con IA y consultas a bases de datos en lenguaje natural.

## Características

- Procesamiento de mensajes con Anthropic Claude
- Consultas a bases de datos MongoDB en lenguaje natural
- Autenticación mediante API keys con diferentes niveles de permisos
- Cache de respuestas para optimizar rendimiento
- Rate limiting para protección contra abusos
- Logging detallado para monitorización
- Validación y sanitización de consultas

## Arquitectura

El proyecto está dividido en tres componentes principales:

1. **api.corebrain.ai**: Backend con FastAPI que procesa mensajes y consultas
2. **dashboard.corebrain.ai**: Interfaz de administración para usuarios
3. **sdk.corebrain.ai**: SDK para la integración en aplicaciones cliente

Este repositorio contiene el código para la API (api.corebrain.ai).

## Requisitos

- Python 3.10+
- MongoDB 5.0+
- Redis 6.2+
- Cuenta en Anthropic para acceso a Claude API

## Instalación

### Usando Docker (recomendado)

1. Clona este repositorio:
   ```bash
   git clone https://github.com/yourusername/corebrain-api.git
   cd corebrain-api
   ```

2. Copia el archivo `.env.example` a `.env` y configura las variables de entorno:
   ```bash
   cp .env.example .env
   # Edita el archivo .env con tu configuración
   ```

3. Construye y ejecuta los contenedores:
   ```bash
   docker-compose up -d
   ```

La API estará disponible en http://localhost:8000

### Instalación manual

1. Clona este repositorio:
   ```bash
   git clone https://github.com/yourusername/corebrain-api.git
   cd corebrain-api
   ```

2. Crea y activa un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Copia el archivo `.env.example` a `.env` y configura las variables de entorno:
   ```bash
   cp .env.example .env
   # Edita el archivo .env con tu configuración
   ```

5. Ejecuta la aplicación:
   ```bash
   uvicorn app.main:app --reload
   ```

## Estructura del proyecto

```
/api.corebrain.ai/
  ├── app/
  │   ├── main.py                   # Punto de entrada de la aplicación
  │   ├── routers/                  # Rutas de la API
  │   │   ├── auth.py               # Endpoints de autenticación
  │   │   ├── chat.py               # Endpoints de conversaciones
  │   │   ├── database.py           # Endpoints para consultas a BD
  │   │   └── analytics.py          # Endpoints para analíticas
  │   ├── models/                   # Modelos Pydantic
  │   │   ├── api_key.py            # Modelo de API keys
  │   │   ├── message.py            # Modelo de mensajes
  │   │   ├── conversation.py       # Modelo de conversaciones
  │   │   ├── user.py               # Modelo de usuarios
  │   │   └── database_query.py     # Modelo de consultas
  │   ├── core/                     # Configuración central
  │   │   ├── config.py             # Configuración general
  │   │   ├── security.py           # Seguridad y autenticación
  │   │   ├── logging.py            # Sistema de registro
  │   │   ├── permissions.py        # Control de permisos
  │   │   └── cache.py              # Gestión de caché
  │   ├── services/                 # Lógica de negocio
  │   │   ├── auth_service.py       # Servicio de autenticación
  │   │   ├── chat_service.py       # Procesamiento de mensajes
  │   │   ├── db_service.py         # Consultas a base de datos
  │   │   └── analytics_service.py  # Analíticas
  │   ├── database/                 # Acceso a bases de datos
  │   │   ├── session.py            # Gestión de conexiones
  │   │   └── repositories/         # Repositorios
  │   └── middleware/               # Middleware
  │       ├── authentication.py     # Autenticación
  │       ├── rate_limiter.py       # Limitador de peticiones
  │       └── request_validator.py  # Validación de solicitudes
  ├── docs/                         # Documentación adicional
  ├── Dockerfile                    # Configuración Docker
  ├── docker-compose.yml            # Configuración Docker Compose
  ├── requirements.txt              # Dependencias Python
  └── README.md                     # Este archivo
```

## Uso de la API

### Autenticación

La API utiliza un sistema de autenticación basado en API keys. Todas las solicitudes deben incluir una API key válida en el encabezado `X-API-Key`.

```bash
curl -X GET "http://localhost:8000/api/auth/validate" \
     -H "X-API-Key: tu_api_key_aquí"
```

### Procesamiento de mensajes

Para enviar un mensaje y recibir una respuesta procesada por IA:

```bash
curl -X POST "http://localhost:8000/api/chat/conversations/tu_conversation_id/messages" \
     -H "X-API-Key: tu_api_key_aquí" \
     -H "Content-Type: application/json" \
     -d '{
           "content": "¿Qué es la inteligencia artificial?",
           "conversation_id": "tu_conversation_id",
           "metadata": {"source": "api_example"}
         }'
```

### Consultas a bases de datos

Para realizar una consulta en lenguaje natural a la base de datos:

```bash
curl -X POST "http://localhost:8000/api/database/query" \
     -H "X-API-Key: tu_api_key_aquí" \
     -H "Content-Type: application/json" \
     -d '{
           "query": "¿Cuáles son los 5 productos más vendidos?",
           "collection_name": "products",
           "limit": 5
         }'
```

## Niveles de permisos

La API utiliza tres niveles de permisos para las API keys:

1. **read**: Acceso de solo lectura a datos básicos
2. **write**: Acceso de lectura y escritura para enviar mensajes y crear conversaciones
3. **admin**: Acceso completo a todas las funcionalidades, incluyendo creación de API keys y análisis

## Documentación de la API

La documentación interactiva está disponible en:

- OpenAPI/Swagger: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

Nota: En producción, la documentación solo está disponible en entornos de desarrollo.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, sigue estos pasos:

1. Haz un fork del repositorio
2. Crea una rama para tu funcionalidad (`git checkout -b feature/amazing-feature`)
3. Realiza tus cambios y haz commit (`git commit -m 'Add some amazing feature'`)
4. Sube la rama (`git push origin feature/amazing-feature`)
5. Abre un Pull Request

## Licencia

Este proyecto está licenciado bajo [MIT License](LICENSE).


# docs/api-reference.md

# Referencia de la API CoreBrain

Esta documentación proporciona una referencia detallada de los endpoints disponibles en la API de CoreBrain.

## Base URL

```
https://api.corebrain.ai
```

## Autenticación

Todas las solicitudes a la API requieren una API key válida que debe enviarse en el encabezado HTTP `X-API-Key`.

Ejemplo:
```
X-API-Key: sk_live_1a2b3c4d5e6f7g8h9i0j
```

## Endpoints

### Autenticación

#### Validar API Key

```
GET /api/auth/validate
```

Valida una API key y devuelve información sobre sus permisos.

**Respuesta**

```json
{
  "valid": true,
  "level": "write",
  "name": "Nombre de la API key"
}
```

#### Crear API Key

```
POST /api/auth/api-keys
```

Crea una nueva API key (requiere permisos de administrador).

**Cuerpo de la solicitud**

```json
{
  "name": "Nombre de la API key",
  "user_id": "id_del_usuario",
  "level": "read",
  "expires_at": "2025-12-31T23:59:59Z",
  "allowed_domains": ["example.com", "*.example.org"]
}
```

**Respuesta**

```json
{
  "id": "api_key_id",
  "name": "Nombre de la API key",
  "level": "read",
  "key": "sk_live_1a2b3c4d5e6f7g8h9i0j",
  "created_at": "2025-03-23T12:34:56Z",
  "expires_at": "2025-12-31T23:59:59Z",
  "allowed_domains": ["example.com", "*.example.org"]
}
```

#### Revocar API Key

```
DELETE /api/auth/api-keys/{api_key_id}
```

Revoca una API key existente (requiere permisos de administrador).

**Respuesta**

```json
{
  "message": "API key revocada correctamente"
}
```

### Chat

#### Crear Conversación

```
POST /api/chat/conversations
```

Crea una nueva conversación.

**Cuerpo de la solicitud**

```json
{
  "title": "Nueva conversación",
  "user_id": "id_del_usuario",
  "metadata": {
    "source": "web_app",
    "tags": ["support", "onboarding"]
  }
}
```

**Respuesta**

```json
{
  "id": "conversation_id",
  "title": "Nueva conversación",
  "created_at": "2025-03-23T12:34:56Z",
  "updated_at": "2025-03-23T12:34:56Z",
  "last_message_at": null,
  "message_count": 0
}
```

#### Obtener Conversación

```
GET /api/chat/conversations/{conversation_id}
```

Obtiene una conversación con sus mensajes.

**Parámetros de consulta**

- `messages_limit` - Número máximo de mensajes a devolver (por defecto: 10)

**Respuesta**

```json
{
  "id": "conversation_id",
  "title": "Nueva conversación",
  "created_at": "2025-03-23T12:34:56Z",
  "updated_at": "2025-03-23T12:34:56Z",
  "last_message_at": "2025-03-23T12:35:30Z",
  "message_count": 2,
  "messages": [
    {
      "id": "message_id_1",
      "content": "Hola, ¿qué es CoreBrain?",
      "is_user": true,
      "created_at": "2025-03-23T12:35:00Z",
      "metadata": {}
    },
    {
      "id": "message_id_2",
      "content": "CoreBrain es una plataforma...",
      "is_user": false,
      "created_at": "2025-03-23T12:35:30Z",
      "metadata": {
        "model": "claude-3-opus-20240229",
        "tokens": {
          "input": 10,
          "output": 150
        }
      }
    }
  ]
}
```

#### Enviar Mensaje

```
POST /api/chat/conversations/{conversation_id}/messages
```

Envía un mensaje y obtiene respuesta de la IA.

**Cuerpo de la solicitud**

```json
{
  "content": "¿Qué es la inteligencia artificial?",
  "conversation_id": "{conversation_id}",
  "metadata": {
    "source": "api_example"
  }
}
```

**Respuesta**

```json
{
  "user_message": {
    "id": "message_id_user",
    "content": "¿Qué es la inteligencia artificial?",
    "is_user": true,
    "created_at": "2025-03-23T12:36:00Z",
    "metadata": {
      "source": "api_example"
    }
  },
  "ai_response": {
    "id": "message_id_ai",
    "content": "La inteligencia artificial (IA) es una rama...",
    "model": "claude-3-opus-20240229",
    "created_at": "2025-03-23T12:36:02Z",
    "tokens": {
      "input": 15,
      "output": 200
    },
    "processing_time": 1.5,
    "metadata": {
      "anthropic_version": "0.5.0",
      "model": "claude-3-opus-20240229"
    }
  }
}
```

### Base de Datos

#### Consulta en Lenguaje Natural

```
POST /api/database/query
```

Ejecuta una consulta en lenguaje natural sobre la base de datos.

**Cuerpo de la solicitud**

```json
{
  "query": "¿Cuáles son los 5 productos más vendidos?",
  "collection_name": "products",
  "limit": 5,
  "metadata": {
    "source": "dashboard"
  }
}
```

**Respuesta**

```json
{
  "natural_query": "¿Cuáles son los 5 productos más vendidos?",
  "mongo_query": {
    "collection": "products",
    "operation": "find",
    "query": {},
    "sort": {"sales": -1},
    "limit": 5
  },
  "result": {
    "data": [
      {"_id": "product_id_1", "name": "Producto A", "sales": 1500},
      {"_id": "product_id_2", "name": "Producto B", "sales": 1200},
      {"_id": "product_id_3", "name": "Producto C", "sales": 980},
      {"_id": "product_id_4", "name": "Producto D", "sales": 850},
      {"_id": "product_id_5", "name": "Producto E", "sales": 720}
    ],
    "count": 5,
    "query_time_ms": 15.6,
    "has_more": true,
    "metadata": {
      "total_count": 150,
      "skip": 0,
      "limit": 5,
      "collection": "products"
    }
  },
  "explanation": "Aquí tienes los 5 productos con mayor número de ventas...",
  "metadata": {
    "processing_time": 2.1,
    "anthropic_model": "claude-3-opus-20240229"
  }
}
```

#### Obtener Esquema de Base de Datos

```
GET /api/database/collections
```

Obtiene información sobre las colecciones y esquemas de la base de datos.

**Respuesta**

```json
{
  "collections": {
    "products": {
      "document_count": 150,
      "schema": {
        "name": {
          "type": "str",
          "example": "Producto A"
        },
        "price": {
          "type": "float",
          "example": "29.99"
        },
        "category": {
          "type": "str",
          "example": "electronics"
        },
        "sales": {
          "type": "int",
          "example": "1500"
        }
      }
    },
    "categories": {
      "document_count": 12,
      "schema": {
        "name": {
          "type": "str",
          "example": "Electronics"
        },
        "description": {
          "type": "str",
          "example": "Electronic devices and accessories"
        }
      }
    }
  }
}
```

### Analíticas

#### Obtener Estadísticas de Uso

```
GET /api/analytics/usage
```

Obtiene estadísticas de uso (requiere permisos de administrador).

**Parámetros de consulta**

- `days` - Número de días a analizar (por defecto: 30)
- `group_by` - Agrupar por 'day', 'week' o 'month' (por defecto: 'day')

**Respuesta**

```json
{
  "start_date": "2025-02-21T00:00:00Z",
  "end_date": "2025-03-23T00:00:00Z",
  "group_by": "day",
  "stats": [
    {
      "date": "2025-03-01",
      "total": 256,
      "events": {
        "message_processed": 187,
        "nl_query_processed": 69
      }
    },
    {
      "date": "2025-03-02",
      "total": 312,
      "events": {
        "message_processed": 245,
        "nl_query_processed": 67
      }
    }
  ]
}
```

#### Obtener Consultas Populares

```
GET /api/analytics/top-queries
```

Obtiene las consultas más populares (requiere permisos de administrador).

**Parámetros de consulta**

- `limit` - Número máximo de consultas a devolver (por defecto: 10)
- `days` - Número de días a analizar (por defecto: 7)

**Respuesta**

```json
[
  {
    "query": "¿Cuáles son los productos más vendidos?",
    "count": 45,
    "collections": ["products"],
    "last_used": "2025-03-23T10:15:30Z"
  },
  {
    "query": "¿Quiénes son nuestros mejores clientes?",
    "count": 32,
    "collections": ["customers", "orders"],
    "last_used": "2025-03-22T15:45:12Z"
  }
]
```

## Códigos de estado HTTP

- `200 OK` - La solicitud se ha completado correctamente
- `201 Created` - El recurso se ha creado correctamente
- `400 Bad Request` - La solicitud es inválida o malformada
- `401 Unauthorized` - Falta autenticación o las credenciales son inválidas
- `403 Forbidden` - El cliente no tiene suficientes permisos
- `404 Not Found` - El recurso solicitado no existe
- `429 Too Many Requests` - Se ha excedido el límite de peticiones
- `500 Internal Server Error` - Error interno del servidor

## Manejo de errores

Todas las respuestas de error tienen el siguiente formato:

```json
{
  "detail": "Descripción del error"
}
```

## Rate Limiting

La API implementa límites de tasa para proteger contra abusos. Los límites por defecto son:

- 60 peticiones por minuto
- 5 peticiones por segundo en ráfaga

Cuando se excede el límite, se devuelve un código de estado `429 Too Many Requests` con un encabezado `Retry-After` que indica cuántos segundos esperar antes de realizar una nueva solicitud.


# docs/integration-guide.md

# Guía de Integración - CoreBrain API

Esta guía proporciona instrucciones paso a paso para integrar CoreBrain API en tu aplicación.

## Requisitos Previos

Para utilizar CoreBrain API, necesitas:

1. Una cuenta en [CoreBrain Dashboard](https://dashboard.corebrain.ai)
2. Una API key (formato: `sk_live_XXXXXXXXXXXXXXXXXXXX` o `sk_test_XXXXXXXXXXXXXXXXXXXX`)
3. Tener configurada una conexión a la base de datos que deseas consultar

## Obtener una API Key

1. Inicia sesión en [CoreBrain Dashboard](https://dashboard.corebrain.ai)
2. Ve a "Configuración" > "API Keys"
3. Haz clic en "Crear API Key" y proporciona un nombre descriptivo
4. Selecciona el nivel de permisos adecuado:
   - **read**: Para solo consultar datos
   - **write**: Para enviar mensajes y crear conversaciones
   - **admin**: Para acceso completo (no recomendado para producción)
5. Copia la API key generada (solo se muestra una vez)

## Integración Básica

### 1. Crear una Conversación

Antes de enviar mensajes, debes crear una conversación:

```bash
curl -X POST "https://api.corebrain.ai/api/chat/conversations" \
     -H "X-API-Key: tu_api_key_aquí" \
     -H "Content-Type: application/json" \
     -d '{
           "title": "Nueva conversación",
           "metadata": {
             "app_version": "1.0.0",
             "user_email": "usuario@ejemplo.com"
           }
         }'
```

Respuesta:

```json
{
  "id": "conversation_id",
  "title": "Nueva conversación",
  "created_at": "2025-03-23T12:34:56Z",
  "updated_at": "2025-03-23T12:34:56Z",
  "last_message_at": null,
  "message_count": 0
}
```

Guarda el `id` de la conversación para usarlo en las siguientes solicitudes.

### 2. Enviar un Mensaje

```bash
curl -X POST "https://api.corebrain.ai/api/chat/conversations/{conversation_id}/messages" \
     -H "X-API-Key: tu_api_key_aquí" \
     -H "Content-Type: application/json" \
     -d '{
           "content": "¿Qué productos tenemos?",
           "conversation_id": "{conversation_id}",
           "metadata": {
             "source": "example_app"
           }
         }'
```

### 3. Consultar la Base de Datos

Para hacer preguntas sobre tus datos:

```bash
curl -X POST "https://api.corebrain.ai/api/database/query" \
     -H "X-API-Key: tu_api_key_aquí" \
     -H "Content-Type: application/json" \
     -d '{
           "query": "¿Cuáles son los clientes que más compran?",
           "limit": 10
         }'
```

## Ejemplos de Integración

### JavaScript / Node.js

```javascript
// Usando fetch en el navegador o node-fetch en Node.js
async function sendMessage(conversationId, message) {
  const response = await fetch(`https://api.corebrain.ai/api/chat/conversations/${conversationId}/messages`, {
    method: 'POST',
    headers: {
      'X-API-Key': 'tu_api_key_aquí',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      content: message,
      conversation_id: conversationId
    })
  });
  
  return await response.json();
}

// Uso
sendMessage('conversation_id', '¿Qué productos tenemos?')
  .then(response => {
    console.log('Respuesta de IA:', response.ai_response.content);
  })
  .catch(error => {
    console.error('Error:', error);
  });
```

### Python

```python
import requests

def send_message(conversation_id, message, api_key):
    url = f"https://api.corebrain.ai/api/chat/conversations/{conversation_id}/messages"
    
    headers = {
        "X-API-Key": api_key,
        "Content-Type": "application/json"
    }
    
    data = {
        "content": message,
        "conversation_id": conversation_id
    }
    
    response = requests.post(url, json=data, headers=headers)
    return response.json()

# Uso
conversation_id = "tu_conversation_id"
api_key = "tu_api_key_aquí"
response = send_message(conversation_id, "¿Qué productos tenemos?", api_key)
print("Respuesta de IA:", response["ai_response"]["content"])
```

## Manejo de Errores

Es importante implementar un manejo adecuado de errores:

```javascript
async function sendMessage(conversationId, message) {
  try {
    const response = await fetch(`https://api.corebrain.ai/api/chat/conversations/${conversationId}/messages`, {
      method: 'POST',
      headers: {
        'X-API-Key': 'tu_api_key_aquí',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        content: message,
        conversation_id: conversationId
      })
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || `Error ${response.status}: ${response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error al enviar mensaje:', error.message);
    throw error;
  }
}
```

## Recomendaciones para Producción

### Gestión de API Keys

- Nunca expongas tu API key en código del lado del cliente
- Para aplicaciones web, crea un proxy en tu backend para manejar las llamadas a CoreBrain API
- Utiliza API keys distintas para desarrollo y producción
- Establece restricciones de dominio para tus API keys

### Optimización de Rendimiento

- Mantén las conversaciones activas para aprovechar el contexto
- Implementa un sistema de caché para consultas frecuentes
- Usa identificadores de conversación permanentes por usuario
- Considera almacenar respuestas localmente para acceso sin conexión

### Manejo de Rate Limiting

```javascript
async function sendMessageWithRetry(conversationId, message, maxRetries = 3) {
  let retries = 0;
  
  while (retries < maxRetries) {
    try {
      return await sendMessage(conversationId, message);
    } catch (error) {
      if (error.response && error.response.status === 429) {
        // Obtener tiempo de espera del encabezado Retry-After
        const retryAfter = parseInt(error.response.headers['retry-after'] || '2');
        
        console.log(`Rate limit alcanzado. Reintentando en ${retryAfter} segundos...`);
        
        // Esperar el tiempo indicado
        await new Promise(resolve => setTimeout(resolve, retryAfter * 1000));
        
        retries++;
      } else {
        // Para otros errores, lanzar inmediatamente
        throw error;
      }
    }
  }
  
  throw new Error(`Se excedió el número máximo de reintentos (${maxRetries})`);
}
```

## Consultas Avanzadas a Base de Datos

Para obtener el máximo provecho de las consultas a la base de datos, sigue estas recomendaciones:

### 1. Especificar la Colección

Cuando sea posible, especifica la colección para enfocar la consulta:

```json
{
  "query": "¿Cuáles son nuestros clientes premium?",
  "collection_name": "customers"
}
```

### 2. Proporcionar Contexto Adicional

Añade metadatos para mejorar la comprensión de la consulta:

```json
{
  "query": "Muestra las ventas del mes pasado",
  "metadata": {
    "timeframe": "last_month",
    "context": "dashboard_sales_report"
  }
}
```

### 3. Limitar y Filtrar Resultados

Utiliza los parámetros de límite para controlar el volumen de datos:

```json
{
  "query": "¿Quiénes son nuestros mejores clientes?",
  "limit": 5
}
```

## Feedback y Mejoras Continuas

Para ayudarnos a mejorar CoreBrain API:

1. Implementa un sistema de feedback donde los usuarios puedan marcar respuestas útiles o incorrectas
2. Envía consultas problemáticas a nuestro equipo de soporte
3. Monitorea el uso y las respuestas para identificar áreas de mejora

## Preguntas Frecuentes

### ¿Cómo puedo probar la API sin afectar mis datos reales?

Utiliza una API key de tipo `sk_test_` que opera en un entorno de pruebas.

### ¿Cuántas consultas puedo hacer por minuto?

El plan estándar permite 60 consultas por minuto, con un límite de 5 consultas por segundo en ráfaga.

### ¿Cómo puedo asegurarme de que mis datos están seguros?

CoreBrain implementa encriptación en tránsito y en reposo, y no almacena tus datos de forma permanente.

### ¿Puedo integrar CoreBrain con mi propio modelo de IA?

Actualmente no, CoreBrain utiliza exclusivamente el modelo Claude de Anthropic.

### ¿Cómo filtro información sensible antes de procesarla?

Implementa filtros en tu aplicación antes de enviar datos a CoreBrain API.

## Soporte

Si necesitas ayuda o tienes preguntas:

- Documentación: [docs.corebrain.ai](https://docs.corebrain.ai)
- Soporte técnico: [support@corebrain.ai](mailto:support@corebrain.ai)
- Centro de ayuda: [help.corebrain.ai](https://help.corebrain.ai)


# docs/sdk-reference.md

# Referencia del SDK de CoreBrain

Esta documentación proporciona una referencia completa para el SDK de CoreBrain, que facilita la integración de tus aplicaciones con CoreBrain API.

## Instalación

### Node.js

```bash
npm install corebrain-sdk
```

### Python

```bash
pip install corebrain-sdk
```

## Inicialización

### Node.js

```javascript
const CoreBrain = require('corebrain-sdk');

const client = new CoreBrain({
  apiKey: 'tu_api_key_aquí',
  baseUrl: 'https://api.corebrain.ai'  // Opcional
});
```

### Python

```python
from corebrain_sdk import CoreBrain

client = CoreBrain(
    api_key='tu_api_key_aquí',
    base_url='https://api.corebrain.ai'  # Opcional
)
```

## Autenticación

El SDK utiliza la API key proporcionada durante la inicialización para autenticar todas las solicitudes.

### Validar la API Key

#### Node.js

```javascript
client.auth.validateApiKey()
  .then(result => {
    console.log('API key válida:', result.valid);
    console.log('Nivel de permisos:', result.level);
  })
  .catch(error => {
    console.error('Error al validar API key:', error);
  });
```

#### Python

```python
try:
    result = client.auth.validate_api_key()
    print(f"API key válida: {result['valid']}")
    print(f"Nivel de permisos: {result['level']}")
except Exception as e:
    print(f"Error al validar API key: {e}")
```

## Gestión de Conversaciones

### Crear una Conversación

#### Node.js

```javascript
client.conversations.create({
  title: 'Nueva conversación',
  metadata: {
    source: 'sdk_example',
    user_id: '123'
  }
})
  .then(conversation => {
    console.log('ID de conversación:', conversation.id);
  })
  .catch(error => {
    console.error('Error al crear conversación:', error);
  });
```

#### Python

```python
try:
    conversation = client.conversations.create(
        title="Nueva conversación",
        metadata={
            "source": "sdk_example",
            "user_id": "123"
        }
    )
    print(f"ID de conversación: {conversation['id']}")
except Exception as e:
    print(f"Error al crear conversación: {e}")
```

### Obtener una Conversación

#### Node.js

```javascript
client.conversations.get('conversation_id')
  .then(conversation => {
    console.log('Título:', conversation.title);
    console.log('Mensajes:', conversation.messages.length);
  })
  .catch(error => {
    console.error('Error al obtener conversación:', error);
  });
```

#### Python

```python
try:
    conversation = client.conversations.get("conversation_id")
    print(f"Título: {conversation['title']}")
    print(f"Mensajes: {len(conversation['messages'])}")
except Exception as e:
    print(f"Error al obtener conversación: {e}")
```

## Envío de Mensajes

### Enviar un Mensaje

#### Node.js

```javascript
client.messages.send({
  conversation_id: 'conversation_id',
  content: '¿Qué es CoreBrain?',
  metadata: {
    source: 'sdk_example'
  }
})
  .then(response => {
    console.log('Mensaje de usuario:', response.user_message.content);
    console.log('Respuesta de IA:', response.ai_response.content);
  })
  .catch(error => {
    console.error('Error al enviar mensaje:', error);
  });
```

#### Python

```python
try:
    response = client.messages.send(
        conversation_id="conversation_id",
        content="¿Qué es CoreBrain?",
        metadata={
            "source": "sdk_example"
        }
    )
    print(f"Mensaje de usuario: {response['user_message']['content']}")
    print(f"Respuesta de IA: {response['ai_response']['content']}")
except Exception as e:
    print(f"Error al enviar mensaje: {e}")
```

## Consultas a Base de Datos

### Consulta en Lenguaje Natural

#### Node.js

```javascript
client.database.query({
  query: '¿Cuáles son los productos más vendidos este mes?',
  collection_name: 'products',  // Opcional
  limit: 5,
  metadata: {
    source: 'dashboard'
  }
})
  .then(response => {
    console.log('Consulta MongoDB:', response.mongo_query);
    console.log('Resultados:', response.result.data);
    console.log('Explicación:', response.explanation);
  })
  .catch(error => {
    console.error('Error al consultar base de datos:', error);
  });
```

#### Python

```python
try:
    response = client.database.query(
        query="¿Cuáles son los productos más vendidos este mes?",
        collection_name="products",  # Opcional
        limit=5,
        metadata={
            "source": "dashboard"
        }
    )
    print(f"Consulta MongoDB: {response['mongo_query']}")
    print(f"Resultados: {response['result']['data']}")
    print(f"Explicación: {response['explanation']}")
except Exception as e:
    print(f"Error al consultar base de datos: {e}")
```

### Obtener Esquema de Base de Datos

#### Node.js

```javascript
client.database.getSchema()
  .then(schema => {
    console.log('Colecciones disponibles:', Object.keys(schema.collections));
    console.log('Esquema de productos:', schema.collections.products.schema);
  })
  .catch(error => {
    console.error('Error al obtener esquema:', error);
  });
```

#### Python

```python
try:
    schema = client.database.get_schema()
    print(f"Colecciones disponibles: {list(schema['collections'].keys())}")
    print(f"Esquema de productos: {schema['collections']['products']['schema']}")
except Exception as e:
    print(f"Error al obtener esquema: {e}")
```

## Gestión de Eventos

### Node.js

```javascript
// Registrar manejadores de eventos
client.on('error', error => {
  console.error('Error en SDK:', error);
});

client.on('rateLimited', retryAfter => {
  console.warn(`Rate limit alcanzado. Reintentando en ${retryAfter} segundos.`);
});

// Para APIs con streaming (si está disponible)
client.on('messageStream', chunk => {
  process.stdout.write(chunk);
});
```

### Python

```python
# Registrar manejadores de eventos
@client.on("error")
def handle_error(error):
    print(f"Error en SDK: {error}")

@client.on("rate_limited")
def handle_rate_limit(retry_after):
    print(f"Rate limit alcanzado. Reintentando en {retry_after} segundos.")

# Para APIs con streaming (si está disponible)
@client.on("message_stream")
def handle_message_stream(chunk):
    print(chunk, end="", flush=True)
```

## Opciones de Configuración

El SDK acepta las siguientes opciones de configuración:

### Node.js

```javascript
const client = new CoreBrain({
  apiKey: 'tu_api_key_aquí',
  baseUrl: 'https://api.corebrain.ai',
  timeout: 30000,  // Tiempo de espera en ms (por defecto: 30000)
  retries: 3,      // Número de reintentos (por defecto: 3)
  debug: false,    // Habilitar logs de depuración (por defecto: false)
  cache: {
    enabled: true,         // Habilitar caché (por defecto: true)
    ttl: 60 * 60 * 1000,   // Tiempo de vida de caché en ms (por defecto: 1 hora)
    maxSize: 100           // Máximo número de ítems en caché (por defecto: 100)
  }
});
```

### Python

```python
client = CoreBrain(
    api_key='tu_api_key_aquí',
    base_url='https://api.corebrain.ai',
    timeout=30.0,  # Tiempo de espera en segundos (por defecto: 30.0)
    retries=3,     # Número de reintentos (por defecto: 3)
    debug=False,   # Habilitar logs de depuración (por defecto: False)
    cache={
        "enabled": True,        # Habilitar caché (por defecto: True)
        "ttl": 60 * 60,         # Tiempo de vida de caché en segundos (por defecto: 1 hora)
        "max_size": 100         # Máximo número de ítems en caché (por defecto: 100)
    }
)
```

## Manejo de Errores

El SDK proporciona clases de error específicas para distintos tipos de problemas:

### Node.js

```javascript
const { ApiError, AuthError, RateLimitError, NetworkError } = require('corebrain-sdk');

try {
  // Código que utiliza el SDK
} catch (error) {
  if (error instanceof AuthError) {
    console.error('Error de autenticación:', error.message);
  } else if (error instanceof RateLimitError) {
    console.error('Límite de tasa excedido. Reintentar en:', error.retryAfter, 'segundos');
  } else if (error instanceof ApiError) {
    console.error('Error de API:', error.message, 'Código:', error.code);
  } else if (error instanceof NetworkError) {
    console.error('Error de red:', error.message);
  } else {
    console.error('Error desconocido:', error);
  }
}
```

### Python

```python
from corebrain_sdk.exceptions import ApiError, AuthError, RateLimitError, NetworkError

try:
    # Código que utiliza el SDK
except AuthError as e:
    print(f"Error de autenticación: {e}")
except RateLimitError as e:
    print(f"Límite de tasa excedido. Reintentar en: {e.retry_after} segundos")
except ApiError as e:
    print(f"Error de API: {e}, Código: {e.code}")
except NetworkError as e:
    print(f"Error de red: {e}")
except Exception as e:
    print(f"Error desconocido: {e}")
```

## Ejemplos Completos

### Node.js - Aplicación de Chat Simple

```javascript
const CoreBrain = require('corebrain-sdk');
const readline = require('readline');

// Inicializar cliente
const client = new CoreBrain({
  apiKey: 'tu_api_key_aquí'
});

// Crear interfaz de línea de comandos
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

// Función principal
async function startChat() {
  console.log('Iniciando chat con CoreBrain...');
  
  try {
    // Validar API key
    const validation = await client.auth.validateApiKey();
    console.log(`API key válida (nivel: ${validation.level})`);
    
    // Crear conversación
    const conversation = await client.conversations.create({
      title: 'Conversación de CLI'
    });
    
    console.log(`Conversación creada con ID: ${conversation.id}`);
    console.log('Escribe tus mensajes (escribir "salir" para terminar):\n');
    
    // Loop de chat
    const chatLoop = () => {
      rl.question('> ', async (input) => {
        if (input.toLowerCase() === 'salir') {
          console.log('¡Adiós!');
          rl.close();
          return;
        }
        
        try {
          // Enviar mensaje
          const response = await client.messages.send({
            conversation_id: conversation.id,
            content: input
          });
          
          // Mostrar respuesta
          console.log(`\nCoreBrain: ${response.ai_response.content}\n`);
          
          // Continuar chat
          chatLoop();
        } catch (error) {
          console.error('Error al enviar mensaje:', error.message);
          chatLoop();
        }
      });
    };
    
    chatLoop();
  } catch (error) {
    console.error('Error:', error.message);
    rl.close();
  }
}

startChat();
```

### Python - Aplicación de Chat Simple

```python
from corebrain_sdk import CoreBrain
import time

# Inicializar cliente
client = CoreBrain(api_key='tu_api_key_aquí')

def start_chat():
    print("Iniciando chat con CoreBrain...")
    
    try:
        # Validar API key
        validation = client.auth.validate_api_key()
        print(f"API key válida (nivel: {validation['level']})")
        
        # Crear conversación
        conversation = client.conversations.create(
            title="Conversación de CLI"
        )
        
        print(f"Conversación creada con ID: {conversation['id']}")
        print("Escribe tus mensajes (escribir 'salir' para terminar):\n")
        
        # Loop de chat
        while True:
            user_input = input("> ")
            
            if user_input.lower() == "salir":
                print("¡Adiós!")
                break
            
            try:
                # Enviar mensaje
                response = client.messages.send(
                    conversation_id=conversation["id"],
                    content=user_input
                )
                
                # Mostrar respuesta
                print(f"\nCoreBrain: {response['ai_response']['content']}\n")
                
            except Exception as e:
                print(f"Error al enviar mensaje: {e}")
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    start_chat()
```

## Roadmap y Próximas Características

- Soporte para streaming de respuestas
- Cliente para React Native
- Integración con TypeScript
- Funciones de administración de API keys
- Análisis y exportación de conversaciones

## Soporte

Si necesitas ayuda o tienes preguntas sobre el SDK:

- Documentación: [docs.corebrain.ai/sdk](https://docs.corebrain.ai/sdk)
- Repositorio: [github.com/corebrain/corebrain-sdk](https://github.com/corebrain/corebrain-sdk)
- Problemas: [github.com/corebrain/corebrain-sdk/issues](https://github.com/corebrain/corebrain-sdk/issues)
- Soporte: [sdk-support@corebrain.ai](mailto:sdk-support@corebrain.ai)