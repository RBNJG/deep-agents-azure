# Decisiones de arquitectura

Estos ADR registran las decisiones fijadas para Procurement Agent Workbench y permiten revisar sus consecuencias antes de implementar. `Aceptado` significa que el equipo acordó la dirección; los detalles de producto y compatibilidad indicados como abiertos siguen pendientes. Un ADR no es evidencia de que el diseño esté implementado o probado.

| ADR | Estado | Decisión |
|---|---|---|
| [0001](0001-postgresql-persistencia.md) | Aceptado | PostgreSQL para estado del agente y datos propios; Docker local y Flexible Server temporal en Azure |
| [0002](0002-demo-azure-efimera.md) | Aceptado | Azure solo para integración/demo y destrucción al terminar; Terraform con state local protegido fuera de Git como perfil inicial |
| [0003](0003-separacion-identidades.md) | Aceptado | Identidad delegada de usuario, principal de servicio/workload e identidad de inicialización con permisos separados |
| [0004](0004-microsoft-graph-opcional.md) | Aceptado | Microsoft Graph queda fuera del núcleo y se incorpora solo como perfil opcional posterior |

## Cuestiones abiertas

- Versiones compatibles de Python, Deep Agents, LangGraph, MCP y saver/store PostgreSQL: medir y fijar en B00.2–B00.4.
- Esquemas/roles SQL y coordinación entre transacciones de negocio, checkpoint y outbox: definir en B00.3, B01 y B03.
- Región, tamaño, cuota y presupuesto Azure disponibles: decidir antes del apply de B04 y revisar para B08.
- Tenant/usuarios de prueba, permisos Entra y suscripción autorizada: son prerrequisitos de las pruebas reales B04/B06, no se dan por disponibles.
- Modelo de pruebas reales y presupuesto de tokens/llamadas: fijar antes de habilitarlas en B03/B10.
- Viabilidad de Graph según tipo de cuenta, permisos y flujo OBO: evaluar solo al llegar a B12.

## Referencias

- `docs/PROJECT_CONTEXT.md`: producto, restricciones y mapa de rutas.
- `docs/CONTRACTS.md`: contratos de identidad, autorización, persistencia e idempotencia.
- `docs/ARCHITECTURE_REFERENCE.md`: análisis y fuentes de la propuesta original.
- `docs/tasks/index.json`: estado del backlog; sus estados no se deducen de estos ADR.
