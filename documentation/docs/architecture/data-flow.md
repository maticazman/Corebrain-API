# Flujo de datos

Esta sección explica en detalle cómo fluyen los datos a través de los diferentes componentes de CoreBrain, desde la solicitud inicial hasta la respuesta final.

## Procesamiento de mensajes

![Flujo de procesamiento de mensajes](../assets/images/message-flow.png)

### 1. Solicitud del cliente

El flujo comienza cuando una aplicación cliente envía un mensaje utilizando el SDK de CoreBrain:

```javascript
const response = await client.messages.send({
  conversationId: "conv_123",
  content: "¿Cuántos usuarios se registraron la semana pasada?"
});
```

### 2. Validación y autenticación

Cuando la solicitud llega a la API:

1. Se verifica la API key en el encabezado `X-API-Key`.
2. Se comprueban los permisos para la operación solicitada.
3. Se valida el formato y contenido de la solicitud.

### 3. Procesamiento contextual

El servicio de chat:

1. Recupera la conversación especificada o crea una nueva.
2. Obtiene el historial de mensajes previos para contexto.
3. Guarda el mensaje del usuario en la base de datos.

### 4. Análisis de la consulta

El sistema determina si el mensaje requiere acceso a la base de datos:

1. Analiza el contenido del mensaje buscando palabras clave.
2. Si es necesario, recupera información sobre las colecciones disponibles.
3. Prepara el contexto para el modelo de IA.

### 5. Interacción con la IA

El servicio de IA:

1. Construye un prompt para Claude con el mensaje, historial y contexto de la base de datos.
2. Envía la solicitud a la API de Anthropic.
3. Claude genera una respuesta que puede incluir consultas MongoDB.

### 6. Ejecución de consultas (si es necesario)

Si Claude sugiere una consulta MongoDB:

1. El sistema extrae la consulta de la respuesta.
2. Sanitiza la consulta para prevenir operaciones maliciosas.
3. Ejecuta la consulta contra la base de datos especificada.
4. Formatea los resultados para enviarlos de vuelta a Claude.

### 7. Generación de la respuesta final

Con los resultados de la consulta:

1. Se genera un nuevo prompt para Claude incluyendo los resultados.
2. Claude interpreta los datos y genera una respuesta final.
3. El sistema guarda la respuesta en la base de datos.
4. Se calcula y registra el costo de la operación.

### 8. Retorno al cliente

Finalmente:

1. La respuesta se formatea según la especificación de la API.
2. Se envía de vuelta al cliente a través del SDK.
3. Se actualizan las métricas y analíticas.

## Flujo de tokens y costos

![Flujo de tokens y costos](../assets/images/token-flow.png)

Cada interacción con Claude consume tokens que tienen un costo asociado. CoreBrain realiza un seguimiento detallado de este consumo:

1. Se cuentan los tokens de entrada (prompt) y salida (respuesta).
2. Se calcula el costo en USD basado en las tarifas actuales de Anthropic.
3. Los costos se almacenan asociados a la conversación.
4. Se actualizan las métricas globales para facturación y analíticas.

## Optimizaciones de rendimiento

CoreBrain implementa varias optimizaciones para mejorar el rendimiento y reducir costos:

1. **Caché**: Las respuestas frecuentes se almacenan en caché para evitar llamadas innecesarias a Claude.
2. **Análisis previo**: El sistema analiza si un mensaje requiere acceso a la base de datos antes de consultar a Claude.
3. **Limitación de contexto**: Solo se envía la información relevante a Claude para reducir el consumo de tokens.
4. **Procesamiento en paralelo**: Las consultas a la base de datos se pueden ejecutar en paralelo cuando es posible.