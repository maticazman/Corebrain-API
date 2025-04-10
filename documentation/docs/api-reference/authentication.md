# Autenticación

CoreBrain API proporciona dos métodos de autenticación:

1. **API Keys**: Para integración en aplicaciones cliente
2. **JWT (JSON Web Tokens)**: Para el dashboard y operaciones administrativas

## API Keys

Las API Keys son el método principal para autenticar solicitudes a la API desde aplicaciones cliente. Se envían a través del encabezado HTTP `X-API-Key`.

### Formato

Las API Keys tienen el siguiente formato:

- `sk_live_XXXXXXXXXXXXXXXXXXXX` - Para uso en producción
- `sk_test_XXXXXXXXXXXXXXXXXXXX` - Para desarrollo y pruebas

### Niveles de permiso

Cada API Key tiene un nivel de permiso asociado:

| Nivel  | Descripción |
|--------|-------------|
| `read` | Solo lectura (consultas) |
| `write` | Lectura + escritura (mensajes, conversaciones) |
| `admin` | Acceso completo (incluye gestión de API Keys) |

### Endpoints

#### Validar API Key

```
GET /api/auth/validate
```

**Encabezados:**
```
X-API-Key: tu_api_key_aquí
```

**Respuesta exitosa (200):**
```json
{
  "valid": true,
  "level": "write",
  "name": "API Key para App"
}
```

#### Crear API Key (requiere autenticación JWT Admin)

```
POST /api/auth/api-keys
```

**Cuerpo:**
```json
{
  "name": "API Key para App Móvil",
  "user_id": "usr_123456789",
  "level": "write",
  "allowed_domains": ["miapp.com", "*.miapp.com"]
}
```

**Respuesta exitosa (201):**
```json
{
  "id": "key_123456789",
  "name": "API Key para App Móvil",
  "level": "write",
  "key": "sk_live_abcdefghijklmnopqrst",
  "created_at": "2025-03-23T12:34:56Z",
  "expires_at": null,
  "allowed_domains": ["miapp.com", "*.miapp.com"]
}
```

#### Revocar API Key (requiere autenticación JWT Admin)

```
DELETE /api/auth/api-keys/{api_key_id}
```

**Respuesta exitosa (200):**
```json
{
  "message": "API key revocada correctamente"
}
```

## JWT (JSON Web Tokens)

Los tokens JWT se utilizan para autenticar usuarios en el dashboard y realizar operaciones administrativas. Se envían a través del encabezado HTTP `Authorization: Bearer {token}`.

### Obtener token (Login)

```
POST /api/auth/token
```

**Cuerpo** (formato form-urlencoded):
```
username=usuario@ejemplo.com&password=contraseña_secreta
```

**Respuesta exitosa (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user_id": "usr_123456789",
  "email": "usuario@ejemplo.com",
  "name": "Nombre del Usuario",
  "role": "admin"
}
```

### Crear usuario (requiere autenticación JWT Admin)

```
POST /api/auth/users
```

**Cuerpo:**
```json
{
  "email": "nuevo@usuario.com",
  "name": "Nuevo Usuario",
  "password": "contraseña_segura"
}
```

**Respuesta exitosa (201):**
```json
{
  "id": "usr_987654321",
  "email": "nuevo@usuario.com",
  "name": "Nuevo Usuario",
  "created_at": "2025-03-23T12:34:56Z",
  "role": "user"
}
```

## Manejo de errores de autenticación

### API Key inválida

**Respuesta (401):**
```json
{
  "detail": "API key inválida o expirada"
}
```

### Token JWT inválido o expirado

**Respuesta (401):**
```json
{
  "detail": "No se pudo validar credenciales",
  "headers": {
    "WWW-Authenticate": "Bearer"
  }
}
```

### Permisos insuficientes

**Respuesta (403):**
```json
{
  "detail": "No tienes permisos suficientes para esta operación"
}
```