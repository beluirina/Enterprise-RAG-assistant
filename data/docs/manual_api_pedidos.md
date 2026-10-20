# Manual Técnico - API de Pedidos v2

Documentación interna para desarrolladores de NovaTech. Equipo dueño: Squad Pedidos.

## 1. Descripción general

La API de Pedidos permite crear, consultar y cancelar pedidos de los clientes de la plataforma NovaShop. Es una API REST que trabaja con JSON.

- URL base de producción: https://api.novatech.com.ar/pedidos/v2
- URL base de staging: https://staging-api.novatech.com.ar/pedidos/v2

La versión v1 está deprecada y se apaga definitivamente el 30 de junio de 2027. Todas las integraciones nuevas deben usar v2.

## 2. Autenticación

Todas las llamadas requieren un token Bearer en el header Authorization. Los tokens se generan desde el Portal de Desarrolladores con el rol "integrador" y duran 60 minutos. Para renovarlos se usa el endpoint POST /auth/refresh.

Ejemplo de header: `Authorization: Bearer <token>`

## 3. Límites de uso (rate limiting)

Cada token puede hacer hasta 100 solicitudes por minuto. Si se supera el límite, la API responde con el código 429 Too Many Requests y el header Retry-After indica cuántos segundos esperar.

## 4. Endpoints principales

- GET /pedidos: lista pedidos. Admite filtros por estado y fecha.
- GET /pedidos/{id}: devuelve el detalle de un pedido.
- POST /pedidos: crea un pedido nuevo. Requiere el header Idempotency-Key para evitar pedidos duplicados.
- POST /pedidos/{id}/cancelar: cancela un pedido. Solo se pueden cancelar pedidos en estado "pendiente" o "confirmado".

Estados posibles de un pedido: pendiente, confirmado, en_preparacion, enviado, entregado y cancelado.

## 5. Paginación

Los listados están paginados. Por defecto se devuelven 50 resultados por página y el máximo permitido es 200, usando el parámetro page_size. La respuesta incluye el campo next_cursor para pedir la página siguiente.

## 6. Códigos de error

- 400: la solicitud tiene datos inválidos. El cuerpo de la respuesta indica qué campo falló.
- 401: el token falta, es inválido o expiró.
- 404: el pedido no existe.
- 409: conflicto, por ejemplo intentar cancelar un pedido ya enviado.
- 429: se superó el límite de solicitudes.
- 500: error interno. Si se repite, reportarlo en #squad-pedidos.

## 7. Webhooks

La API puede notificar cambios de estado mediante webhooks. Cada notificación viene firmada con HMAC-SHA256 en el header X-Nova-Signature. Si el servidor del cliente no responde con 200, se reintenta hasta 5 veces con espera exponencial.
