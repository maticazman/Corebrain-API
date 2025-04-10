
# CoreBrain API

![CoreBrain Logo](assets/images/corebrain-logo.png){ align=center width=300 }

**Plataforma de IA que conecta tus datos con la inteligencia avanzada de modelos de lenguaje.**

CoreBrain es una API que permite a los desarrolladores conectar sus bases de datos MongoDB con modelos de lenguaje como Claude de Anthropic para crear experiencias conversacionales poderosas que pueden analizar, interpretar y responder preguntas sobre los datos almacenados.

## Características principales

### 🧠 Inteligencia avanzada
Potenciado por Claude de Anthropic, CoreBrain ofrece una comprensión profunda del lenguaje natural y capacidad para trabajar con instrucciones complejas.

### 🔍 Consultas en lenguaje natural
Permite a los usuarios consultar bases de datos MongoDB utilizando lenguaje natural, sin necesidad de conocer la sintaxis de las consultas.

### 🛡️ Seguridad por diseño
Sistema de permisos granular que garantiza que los usuarios solo puedan acceder a los datos para los que tienen autorización.

### 📊 Analítica integrada
Seguimiento detallado del uso, rendimiento y costos para optimizar la integración.

### 🔄 Fácil integración
SDK disponible para múltiples lenguajes y plataformas, con opciones para JavaScript, Python y más.

## Casos de uso

CoreBrain es ideal para:

- **Asistentes internos para empresas** que necesitan responder preguntas sobre datos de negocios
- **Aplicaciones de análisis de datos** que requieren una interfaz conversacional
- **Chatbots de soporte** que deben consultar bases de datos para resolver problemas
- **Herramientas de automatización** que necesitan interpretar datos y tomar decisiones
- **Paneles de control interactivos** donde los usuarios pueden hacer preguntas sobre métricas

## Arquitectura

CoreBrain consta de tres componentes principales:

1. **api.corebrain.ai**: Backend con FastAPI que procesa mensajes y consultas, conectando con MongoDB y Anthropic.
2. **dashboard.corebrain.ai**: Interfaz de administración para usuarios.
3. **sdk.corebrain.ai**: SDK para la integración en aplicaciones cliente.

## Primeros pasos

Para comenzar a utilizar CoreBrain, sigue estos pasos:

1. [Regístrate](https://dashboard.corebrain.ai/register) para obtener una cuenta.
2. [Crea una API key](getting-started/configuration.md#crear-api-key) desde tu dashboard.
3. [Instala el SDK](sdk/installation.md) en tu aplicación.
4. [Comienza a consultar tus datos](getting-started/first-steps.md) con lenguaje natural.

```javascript
// Ejemplo de integración con JavaScript
import { CoreBrain } from 'corebrain-sdk';

const client = new CoreBrain({
  apiKey: 'tu_api_key',
});

// Crea una conversación
const conversation = await client.conversations.create({
  title: 'Análisis de ventas'
});

// Envía un mensaje y recibe una respuesta
const response = await client.messages.send({
  conversationId: conversation.id,
  content: '¿Cuáles fueron nuestras ventas totales del mes pasado?'
});

console.log(response.aiResponse.content);
```

## Próximos pasos

- Explora la [documentación de la API](api-reference/authentication.md)
- Aprende a [configurar permisos](security/permissions.md)
- Descubre [ejemplos de integración](integration/examples.md)
- Únete a nuestra [comunidad de desarrolladores](https://discord.gg/corebrain)

## Licencia

CoreBrain se distribuye bajo la [Licencia MIT](https://opensource.org/licenses/MIT).

---

¿Tienes alguna pregunta? [Contáctanos](mailto:support@corebrain.ai) o revisa nuestras [Preguntas frecuentes](faq.md).