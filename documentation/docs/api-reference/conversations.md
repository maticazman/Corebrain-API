
# Conversaciones

Las conversaciones son hilos de mensajes entre el usuario y la IA. Cada conversación tiene un identificador único y puede contener múltiples mensajes.

## Endpoints

### Crear conversación

```
POST /api/chat/conversations
```

**Encabezados:**
```
X-API-Key: tu_api_key_aquí
Content-Type: application/json
```

**Cuerpo:**
```json
{
  "title": "Análisis de ventas",
  "metadata": {
    "source": "app_mobile",
    "user_reference": "user_12345"
  }
}
```

**Respuesta exitosa (201):**
```json
{
  "id": "conv_123456789",
  "title": "Análisis de ventas",
  "created_at": "2025-03-23T12:34:56Z",
  "updated_at": "2025-03-23T12:34:56Z",
  "last_message_at": null,
  "message_count": 0
}
```

### Obtener conversación

```
GET /api/chat/conversations/{conversation_id}
```

**Parámetros de consulta:**
- `messages_limit` - Cantidad máxima de mensajes a retornar (defecto: 10)

**Encabezados:**
```
X-API-Key: tu_api_key_aquí
```

**Respuesta exitosa (200):**
```json
{
  "id": "conv_123456789",
  "title": "Análisis de ventas",
  "created_at": "2025-03-23T12:34:56Z",
  "updated_at": "2025-03-23T12:34:56Z",
  "last_message_at": "2025-03-23T12:35:30Z",
  "message_count": 2,
  "messages": [
    {
      "id": "msg_123456789",
      "content": "¿Cuántas ventas tuvimos el mes pasado?",
      "is_user": true,
      "created_at": "2025-03-23T12:35:00Z",
      "metadata": {}
    },
    {
      "id": "msg_987654321",
      "content": "El mes pasado tuvieron un total de 1,254 ventas por un valor total de $45,678.",
      "is_user": false,
      "created_at": "2025-03-23T12:35:30Z",
      "metadata": {
        "model": "claude-3-opus-20240229",
        "tokens": {
          "input": 22,
          "output": 24
        }
      }
    }
  ]
}
```

### Listar conversaciones

```
GET /api/chat/conversations
```

**Parámetros de consulta:**
- `limit` - Cantidad máxima de conversaciones (defecto: 20)
- `offset` - Desplazamiento para paginación (defecto: 0)

**Encabezados:**
```
X-API-Key: tu_api_key_aquí
```

**Respuesta exitosa (200):**
```json
{
  "conversations": [
    {
      "id": "conv_123456789",
      "title": "Análisis de ventas",
      "created_at": "2025-03-23T12:34:56Z",
      "updated_at": "2025-03-23T12:35:30Z",
      "last_message_at": "2025-03-23T12:35:30Z",
      "message_count": 2
    },
    {
      "id": "conv_987654321",
      "title": "Soporte técnico",
      "created_at": "2025-03-23T10:15:30Z",
      "updated_at": "2025-03-23T10:20:45Z",
      "last_message_at": "2025-03-23T10:20:45Z",
      "message_count": 5
    }
  ],
  "count": 2
}
```

### Actualizar conversación

```
PATCH /api/chat/conversations/{conversation_id}
```

**Encabezados:**
```
X-API-Key: tu_api_key_aquí
Content-Type: application/json
```

**Cuerpo:**
```json
{
  "title": "Análisis de ventas Q1 2025"
}
```

**Respuesta exitosa (200):**
```json
{
  "id": "conv_123456789",
  "title": "Análisis de ventas Q1 2025",
  "created_at": "2025-03-23T12:34:56Z",
  "updated_at": "2025-03-23T13:45:30Z",
  "last_message_at": "2025-03-23T12:35:30Z",
  "message_count": 2
}
```

### Eliminar conversación

```
DELETE /api/chat/conversations/{conversation_id}
```

**Encabezados:**
```
X-API-Key: tu_api_key_aquí
```

**Respuesta exitosa (200):**
```json
{
  "message": "Conversación eliminada correctamente"
}
```

# docs/api-reference/messages.md

# Mensajes

Los mensajes son el componente principal de interacción con la IA. Un mensaje del usuario genera una respuesta de la IA utilizando el contexto de la conversación.

## Endpoints

### Enviar mensaje

```
POST /api/chat/conversations/{conversation_id}/messages
```

**Encabezados:**
```
X-API-Key: tu_api_key_aquí
Content-Type: application/json
```

**Cuerpo:**
```json
{
  "content": "¿Cuántos usuarios activos tuvimos la semana pasada?",
  "conversation_id": "conv_123456789",
  "metadata": {
    "source": "dashboard_analytics",
    "user_locale": "es-MX"
  }
}
```

**Respuesta exitosa (200):**
```json
{
  "user_message": {
    "id": "msg_123456789",
    "content": "¿Cuántos usuarios activos tuvimos la semana pasada?",
    "is_user": true,
    "created_at": "2025-03-23T14:15:30Z",
    "metadata": {
      "source": "dashboard_analytics",
      "user_locale": "es-MX"
    }
  },
  "ai_response": {
    "id": "msg_987654321",
    "content": "La semana pasada tuvieron 2,543 usuarios activos, lo que representa un aumento del 15% con respecto a la semana anterior.",
    "model": "claude-3-opus-20240229",
    "created_at": "2025-03-23T14:15:32Z",
    "tokens": {
      "input": 35,
      "output": 28
    },
    "processing_time": 1.8,
    "metadata": {
      "anthropic_version": "0.5.0",
      "model": "claude-3-opus-20240229",
      "queries_executed": 1,
      "cost": {
        "input_usd": 0.000525,
        "output_usd": 0.0021,
        "total_usd": 0.002625
      }
    }
  }
}
```

### Obtener mensajes de una conversación

```
GET /api/chat/conversations/{conversation_id}/messages
```

**Parámetros de consulta:**
- `limit` - Cantidad máxima de mensajes (defecto: 50)
- `before` - ID del mensaje antes del cual obtener mensajes (para paginación)

**Encabezados:**
```
X-API-Key: tu_api_key_aquí
```

**Respuesta exitosa (200):**
```json
{
  "messages": [
    {
      "id": "msg_123456789",
      "content": "¿Cuántos usuarios activos tuvimos la semana pasada?",
      "is_user": true,
      "created_at": "2025-03-23T14:15:30Z",
      "metadata": {
        "source": "dashboard_analytics"
      }
    },
    {
      "id": "msg_987654321",
      "content": "La semana pasada tuvieron 2,543 usuarios activos, lo que representa un aumento del 15% con respecto a la semana anterior.",
      "is_user": false,
      "created_at": "2025-03-23T14:15:32Z",
      "metadata": {
        "model": "claude-3-opus-20240229",
        "tokens": {
          "input": 35,
          "output": 28
        }
      }
    }
  ],
  "count": 2
}
```