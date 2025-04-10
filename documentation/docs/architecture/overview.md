# Visión general de la arquitectura

CoreBrain utiliza una arquitectura modular y escalable diseñada para procesar consultas en lenguaje natural, interactuar con bases de datos MongoDB y proporcionar respuestas contextuales utilizando modelos de lenguaje avanzados.

## Arquitectura general

![Arquitectura de CoreBrain](../assets/images/architecture-overview.png)

El sistema está dividido en tres componentes principales:

1. **api.corebrain.ai**: El backend basado en FastAPI que procesa las solicitudes, gestiona la autenticación y se comunica con servicios externos.
2. **dashboard.corebrain.ai**: La interfaz de administración para que los usuarios gestionen su cuenta, API keys y analíticas.
3. **sdk.corebrain.ai**: El SDK que permite a los desarrolladores integrar fácilmente CoreBrain en sus aplicaciones.

## Flujo de datos

1. La aplicación cliente envía una solicitud a través del SDK de CoreBrain.
2. El SDK formatea la solicitud y la envía a la API.
3. La API autentica la solicitud y verifica los permisos.
4. Si la solicitud implica una consulta a la base de datos, se procesa a través del motor de procesamiento natural a MongoDB.
5. El resultado se combina con el contexto de la conversación y se envía al modelo de lenguaje (Claude).
6. La respuesta del modelo se procesa y se devuelve al cliente.

## Componentes tecnológicos

### Backend (API)

- **FastAPI**: Framework web rápido para construir APIs con Python 3.7+
- **Motor/PyMongo**: Cliente asincrónico de MongoDB para Python
- **Anthropic SDK**: Cliente oficial para interactuar con la API de Claude
- **Redis**: Para caché y limitación de tasa
- **Pydantic**: Validación de datos y configuración

### Frontend (Dashboard)

- **React/Next.js**: Framework de frontend para la interfaz de usuario
- **TypeScript**: Tipado estático para mejorar la calidad del código
- **TailwindCSS**: Framework CSS para el diseño
- **React Query**: Gestión de estado del lado del servidor
- **Recharts**: Biblioteca para visualización de datos

### SDK

- **JavaScript/TypeScript**: SDK principal para aplicaciones web
- **Python**: SDK para aplicaciones backend y análisis de datos
- **Node.js**: SDK para aplicaciones servidor

## Seguridad

CoreBrain implementa varias capas de seguridad:

- **API Keys con niveles de permiso**: Cada API key tiene un nivel específico de acceso (read, write, admin).
- **Sanitización de consultas**: Todas las consultas MongoDB son sanitizadas para prevenir inyecciones.
- **Control de acceso a colecciones**: Las API keys solo pueden acceder a colecciones específicas.
- **Rate limiting**: Limitación de solicitudes para prevenir abusos.
- **Encriptación en tránsito**: Todas las comunicaciones utilizan HTTPS/TLS.
- **Logging extensivo**: Registro detallado de todas las operaciones para auditoría.