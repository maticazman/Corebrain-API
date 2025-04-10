# Componentes del sistema

CoreBrain se compone de varios módulos especializados que trabajan juntos para proporcionar una experiencia fluida. A continuación se describen los componentes principales:

## 1. Módulo de autenticación

![Módulo de autenticación](../assets/images/auth-module.png)

Este módulo gestiona:

- **API Keys**: Creación, validación y revocación de claves de API.
- **Tokens JWT**: Para autenticación en el dashboard.
- **Control de permisos**: Validación de niveles de acceso para diferentes operaciones.

### Componentes clave

- `AuthService`: Servicio central para operaciones de autenticación.
- `ApiKeyRepository`: Gestión de almacenamiento y recuperación de API keys.
- `PermissionsManager`: Verificación de permisos para diferentes acciones.

## 2. Módulo de chat

![Módulo de chat](../assets/images/chat-module.png)

Gestiona el flujo conversacional entre usuarios y la IA:

- **Conversaciones**: Creación y gestión de hilos conversacionales.
- **Mensajes**: Procesamiento de mensajes entrantes y salientes.
- **Historial**: Mantenimiento del contexto de la conversación.

### Componentes clave

- `ChatService`: Coordina el procesamiento de mensajes.
- `ConversationRepository`: Almacenamiento y recuperación de conversaciones.
- `MessageRepository`: Gestión de mensajes individuales.

## 3. Módulo de procesamiento de IA

![Módulo de IA](../assets/images/ai-module.png)

Puente entre el lenguaje natural y los modelos de IA:

- **Cliente Anthropic**: Conexión con la API de Claude.
- **Gestión de prompts**: Creación de instrucciones efectivas para la IA.
- **Procesamiento de respuestas**: Extracción y formateo de las respuestas.

### Componentes clave

- `AIService`: Gestión de interacciones con Anthropic Claude.
- `PromptManager`: Construcción y optimización de prompts del sistema.
- `ResponseProcessor`: Procesamiento y filtrado de respuestas.

## 4. Módulo de base de datos

![Módulo de base de datos](../assets/images/db-module.png)

Permite la interacción entre la IA y las bases de datos:

- **Conexiones MongoDB**: Gestión de conexiones a bases de datos.
- **Procesamiento de consultas**: Traducción de lenguaje natural a operaciones MongoDB.
- **Sanitización**: Validación y sanitización de consultas.

### Componentes clave

- `DatabaseService`: Interfaz principal para operaciones de base de datos.
- `QueryTranslator`: Conversión de consultas en lenguaje natural a MongoDB.
- `ResultFormatter`: Formateo de resultados para su consumo.

## 5. Módulo de analíticas

![Módulo de analíticas](../assets/images/analytics-module.png)

Seguimiento y análisis del uso del sistema:

- **Tracking de eventos**: Registro de eventos importantes.
- **Métricas de uso**: Seguimiento de consumo de tokens y consultas.
- **Costos**: Cálculo de costos asociados al uso.

### Componentes clave

- `AnalyticsService`: Coordinación de recopilación y procesamiento de analíticas.
- `EventTracker`: Registro de eventos importantes del sistema.
- `CostCalculator`: Estimación y seguimiento de costos de API.

## 6. SDK

![Estructura del SDK](../assets/images/sdk-structure.png)

Biblioteca cliente para integración con aplicaciones:

- **Cliente API**: Conexión con los endpoints de la API.
- **Gestión de caché**: Optimización de rendimiento mediante caché local.
- **Gestión de errores**: Manejo unificado de errores y reintentos.

### Componentes clave

- `CoreBrainClient`: Clase principal para interactuar con la API.
- `ConversationManager`: Gestión de conversaciones desde el cliente.
- `MessageManager`: Envío y recepción de mensajes.