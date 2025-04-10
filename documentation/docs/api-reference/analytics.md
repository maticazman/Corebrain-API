# Analíticas

CoreBrain proporciona endpoints para obtener estadísticas de uso y rendimiento.

## Endpoints

### Obtener estadísticas de uso

```
GET /api/analytics/usage
```

**Parámetros de consulta:**
- `days` - Número de días a analizar (defecto: 30)
- `group_by` - Agrupar por 'day', 'week' o 'month' (defecto: 'day')

**Encabezados:**
```
X-API-Key: tu_api_key_aquí
```

**Respuesta exitosa (200):**
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

### Obtener estadísticas de costos

```
GET /api/analytics/costs
```

**Parámetros de consulta:**
- `days` - Número de días a analizar (defecto: 30)
- `group_by` - Agrupar por 'day', 'week' o 'month' (defecto: 'day')

**Encabezados:**
```
X-API-Key: tu_api_key_aquí
```

**Respuesta exitosa (200):**
```json
{
  "start_date": "2025-02-21T00:00:00Z",
  "end_date": "2025-03-23T00:00:00Z",
  "group_by": "day",
  "total_usd": 45.67,
  "costs": [
    {
      "date": "2025-03-01",
      "tokens": {
        "input": 125670,
        "output": 74320,
        "total": 199990
      },
      "usd": {
        "input": 1.88,
        "output": 5.57,
        "total": 7.45
      }
    },
    {
      "date": "2025-03-02",
      "tokens": {
        "input": 145230,
        "output": 82450,
        "total": 227680
      },
      "usd": {
        "input": 2.18,
        "output": 6.18,
        "total": 8.36
      }
    }
  ]
}
```

### Obtener consultas populares

```
GET /api/analytics/top-queries
```

**Parámetros de consulta:**
- `limit` - Número máximo de consultas a retornar (defecto: 10)
- `days` - Número de días a analizar (defecto: 7)

**Encabezados:**
```
X-API-Key: tu_api_key_aquí
```

**Respuesta exitosa (200):**
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