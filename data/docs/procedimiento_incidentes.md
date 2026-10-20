# Procedimiento de Gestión de Incidentes Técnicos

NovaTech Soluciones S.A. - Área de Ingeniería y Operaciones (SRE). Versión 1.4.

## 1. Objetivo

Definir cómo se detectan, clasifican, comunican y resuelven los incidentes que afectan a los servicios productivos de NovaTech.

## 2. Niveles de severidad

- SEV1 (crítico): el servicio principal está caído o hay pérdida de datos de clientes. Tiempo máximo de primera respuesta: 15 minutos.
- SEV2 (alto): una funcionalidad importante no funciona o el rendimiento está muy degradado para muchos clientes. Tiempo máximo de primera respuesta: 30 minutos.
- SEV3 (medio): falla parcial con alternativa disponible, o impacto en pocos clientes. Tiempo máximo de primera respuesta: 4 horas hábiles.
- SEV4 (bajo): problema menor o cosmético. Se atiende en el siguiente sprint.

## 3. Cómo reportar un incidente

Cualquier empleado que detecte un posible incidente debe reportarlo en el canal de Slack #incidentes indicando qué servicio está afectado, desde cuándo y a quién impacta. Para SEV1 y SEV2 también hay que activar la guardia desde PagerDuty con el comando /pd trigger.

## 4. Roles durante un incidente

- Incident Commander (IC): coordina la respuesta y toma las decisiones. Por defecto es la persona de guardia del equipo SRE.
- Responsable de comunicación: actualiza la página de estado (status.novatech.com.ar) y avisa a Atención al Cliente.
- Equipo técnico: investiga y aplica la solución.

Durante un SEV1 el responsable de comunicación debe publicar una actualización cada 30 minutos, aunque no haya novedades.

## 5. Guardias (on-call)

Las guardias son semanales, de lunes 10:00 a lunes 10:00. Cada ingeniero de backend y SRE participa de la rotación. La guardia se compensa con un adicional del 15% del sueldo bruto mensual por semana de guardia. Durante la guardia hay que poder responder en menos de 15 minutos.

## 6. Cierre y postmortem

Un incidente se cierra cuando el servicio vuelve a funcionar normalmente durante al menos 1 hora. Para todos los incidentes SEV1 y SEV2 se debe escribir un postmortem dentro de los 5 días hábiles posteriores al cierre. El postmortem es "sin culpables" (blameless): se analizan causas y procesos, no personas. Se guarda en la carpeta Confluence "Postmortems" e incluye cronología, causa raíz, impacto y acciones correctivas con responsable y fecha.
