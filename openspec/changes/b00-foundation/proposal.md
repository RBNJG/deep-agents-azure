# Proposal

## Why

La planificación de B00 existe en `docs/tasks/B00.md`, pero aún no hay un proyecto Python instalable. Se necesita una fundación verificable antes de implementar persistencia, compras o el runtime del agente.

## What Changes

- Incorporar B00 al flujo OpenSpec conservando los IDs y la autoridad de contratos, ADRs y estados del backlog.
- B00.1: reconocer la documentación integrada en `dev` mediante PR #1; conservar `READY_FOR_REVIEW` mientras no se concilie formalmente su revisión.
- B00.2: crear paquete instalable, entorno bloqueado, configuración tipada, entradas mínimas de API/worker/MCP, health/readiness, herramientas de calidad y contenedores locales.
- B00.3: materializar posteriormente los contratos v0 y sus fixtures sin duplicarlos por servicio.
- B00.4: verificar posteriormente el recorrido de eco Deep Agents/modelo simulado/MCP HTTP y registrar compatibilidad.
- Encargo actual: implementar exclusivamente B00.2. B00.3 y B00.4 permanecen pendientes.

## Capabilities

### New Capabilities

- `service-lifecycle`: arranque validado y señales de salud/disponibilidad de los tres procesos.
- `shared-contracts`: modelos compartidos, serialización estable y separación entre aprobación de herramienta y decisión de compra (B00.3).
- `agent-tool-transport`: compatibilidad demostrada de agente simulado y herramienta MCP local sobre HTTP (B00.4).

### Modified Capabilities

Ninguna: no existen especificaciones principales previas.

## Impact

Fuentes: `docs/PROJECT_CONTEXT.md`, `docs/CONTRACTS.md`, `docs/DEVELOPMENT_PLAN.md`, `docs/tasks/B00.md`, `docs/handoffs/B00.1.md` y ADRs 0001–0004.
No hay dependencias de entrada al bloque. B00.2 toma como antecedente la entrega documental B00.1; su fusión no cambia automáticamente el estado del índice.
Afecta a empaquetado raíz, `apps/`, `packages/`, `tests/`, scripts, CI local y documentación de desarrollo. Las versiones del runtime agéntico quedan sujetas a B00.4.
Quedan fuera Azure real, base de negocio, UI, procesamiento de colas, compras y llamadas a proveedores LLM. Preparar Docker no prueba su ejecución.
