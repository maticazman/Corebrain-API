
# Base de datos

CoreBrain permite ejecutar consultas en lenguaje natural sobre bases de datos MongoDB conectadas.

## Endpoints

### Consulta en lenguaje natural

```
POST /api/database/query
```

**Encabezados:**
```
X-API-Key: tu_api_key_aquí
Content-Type: application/json
```

**Cuerpo:**
```json
{
  "query": "¿Cuáles son los 5 productos más vendidos este mes?",
  "collection_name": "products",
  "limit": 5,
  "metadata": {
    "context": "dashboard_sales_report"
  }
}
```

**Respuesta exitosa (200):**
```json
{
  "natural_query": "¿Cuáles son los 5 productos más vendidos este mes?",
  "mongo_query": {
    "collection": "products",
    "operation": "find",
    "query": {},
    "sort": {"sales": -1},
    "limit": 5
  },
  "result": {
    "data": [
      {"_id": "prod_123", "name": "Laptop Pro", "sales": 256},
      {"_id": "prod_456", "name": "Smartphone X", "sales": 187},
      {"_id": "prod_789", "name": "Tablet Ultra", "sales": 145},
      {"_id": "prod_012", "name": "Monitor 4K", "sales": 98},
      {"_id": "prod_345", "name": "Auriculares BT", "sales": 87}
    ],
    "count": 5,
    "query_time_ms": 25.4,
    "has_more": true,
    "metadata": {
      "total_count": 120,
      "skip": 0,
      "limit": 5,
      "collection": "products"
    }
  },
  "explanation": "Los 5 productos más vendidos este mes son Laptop Pro (256 unidades), Smartphone X (187 unidades), Tablet Ultra (145 unidades), Monitor 4K (98 unidades) y Auriculares BT (87 unidades). Estos datos representan el top 5 de un total de 120 productos en el catálogo.",
  "metadata": {
    "processing_time": 1.2,
    "anthropic_model": "claude-3-opus-20240229"
  }
}
```

### Obtener esquema de base de datos

```
GET /api/database/collections
```

**Encabezados:**
```
X-API-Key: tu_api_key_aquí
```

**Respuesta exitosa (200):**
```json
{
  "collections": {
    "products": {
      "document_count": 120,
      "schema": {
        "name": {
          "type": "string",
          "example": "Laptop Pro"
        },
        "price": {
          "type": "number",
          "example": "999.99"
        },
        "category": {
          "type": "string",
          "example": "electronics"
        },
        "sales": {
          "type": "number",
          "example": "256"
        }
      }
    },
    "customers": {
      "document_count": 5430,
      "schema": {
        "name": {
          "type": "string",
          "example": "John Doe"
        },
        "email": {
          "type": "string",
          "example": "john@example.com"
        },
        "signup_date": {
          "type": "date",
          "example": "2024-01-15T10:30:00Z"
        }
      }
    }
  }
}
```