# DEV — Herramientas de desarrollo

Trabajo transversal autorizado por el usuario, independiente del backlog de
producto B00–B12. No cuenta como implementación de los subagentes de B09.

## DEV.1 — Configurar agentes de desarrollo con OpenSpec

**Modo:** LOCAL. **Dependencias:** configuración OpenSpec y entorno local de B00.2
presentes; comprobar archivos y handoff, sin cambiar su estado de revisión.

**Implementar:** coordinador/planificador/revisor con `gpt-6.1-sol` y esfuerzo
`high`; implementación acotada con `gpt-6-luna` y `medium`. Delegación explícita,
revisión independiente y trazabilidad OpenSpec en todas las implementaciones.

**Entregable:** configuración Codex del proyecto, roles, guía, instrucciones
conciliadas, cambio `dev-agent-orchestration`, handoff e índice.

**Aceptación:** TOML y JSON válidos; modelo y esfuerzo explícitos por rol;
protocolo que impida asignar decisiones abiertas al worker; OpenSpec estricto
válido; instrucciones de activación y límites sin afirmar inferencias no probadas.

**Fuera de alcance:** runtime de compras, Azure, cambios globales del cliente y
pruebas de inferencia con modelos reales. No altera contratos ni ADRs de producto.

**Entrega:** [handoff DEV.1](../handoffs/DEV.1.md), usando la plantilla común.
