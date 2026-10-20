# Resultados de la evaluación

Fecha: 2026-10-20 · Embeddings: `tfidf` · Generador: `extractive` · top_k=4 · umbral=0.2

| Métrica | Valor |
|---|---|
| Preguntas totales | 90 (77 con respuesta, 13 sin respuesta) |
| Recuperación Hit@1 (doc correcto en el 1er lugar) | 94.8% |
| Recuperación Hit@4 (doc correcto en el top 4) | 100.0% |
| Exactitud de respuesta (contiene el dato esperado) | 87.0% |
| Abstención correcta (dice "no sé" cuando no hay info) | 84.6% |
| Abstención incorrecta (dice "no sé" pero sí había info) | 6.5% |

## Errores (12)

| # | Pregunta | Esperado | Respuesta del sistema |
|---|---|---|---|
| 6 | ¿Cuántos días de vacaciones no usados puedo pasar al año siguiente? | responder | Política de Vacaciones - NovaTech Soluciones S.A. [2] Los días transferidos vencen el 31 de marzo del año siguiente. [1] Los empleados que n |
| 11 | ¿Cuántos días por semana hay que ir a la oficina? | responder | No encontré información suficiente en la documentación para responder esa pregunta. |
| 17 | ¿Cuál es la dirección de la oficina central? | responder | No encontré información suficiente en la documentación para responder esa pregunta. |
| 18 | ¿Qué hago si me roban la notebook? | responder | No encontré información suficiente en la documentación para responder esa pregunta. |
| 31 | ¿Cuál es la URL base de producción de la API de Pedidos? | responder | La API de Pedidos permite crear, consultar y cancelar pedidos de los clientes de la plataforma NovaShop. [1] Equipo dueño: Squad Pedidos. [1 |
| 34 | ¿Cuánto dura un token de la API de Pedidos? | responder | GET /pedidos: lista pedidos. [1] La API de Pedidos permite crear, consultar y cancelar pedidos de los clientes de la plataforma NovaShop. [2 |
| 37 | ¿Cuándo se apaga la versión v1 de la API? | responder | No encontré información suficiente en la documentación para responder esa pregunta. |
| 41 | ¿Qué pasa el primer día de trabajo? | responder | El primer día se trabaja de forma presencial en la oficina central. [1] Esta guía resume lo que tenés que saber durante tus primeras semanas |
| 48 | ¿Qué plan de prepaga tienen los empleados? | responder | No encontré información suficiente en la documentación para responder esa pregunta. |
| 75 | ¿Puedo hacer una denuncia anónima? | responder | Ante robo o pérdida hay que avisar a Mesa de Ayuda dentro de las 24 horas y hacer la denuncia policial. [1] No se debe prestar a familiares  |
| 84 | ¿Cuál es la contraseña del wifi de la oficina? | abstenerse | Está prohibido compartir contraseñas o anotarlas en papel. [1] Se deben cambiar cada 90 días y no se pueden repetir las últimas 5 contraseña |
| 86 | ¿Cuál fue la facturación de NovaTech el año pasado? | abstenerse | Las facturas se reciben únicamente en formato electrónico en facturas@novatech.com.ar y deben incluir el número de orden de compra. [1] Las  |
