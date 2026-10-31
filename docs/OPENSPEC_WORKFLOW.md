# Planificación y ejecución con OpenSpec

La planificación original sigue en [DEVELOPMENT_PLAN.md](DEVELOPMENT_PLAN.md),
[tasks/index.json](tasks/index.json) y las fichas de bloque. OpenSpec transforma
cada bloque en un cambio ejecutable de forma progresiva. No se importan como
capacidades implementadas las funciones que solo están descritas en el plan.

## Fuentes y estados

- [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md), [CONTRACTS.md](CONTRACTS.md) y
  [ADRs](adr/README.md) conservan las decisiones compartidas.
- [La configuración](../openspec/config.yaml) aplica contexto, reglas por artefacto
  y orientaciones de ejecución y archivo. Las skills locales de `.github/skills/`
  permiten trabajar desde Copilot; no son comandos de PowerShell.
- El índice conserva `TODO`, `IN_PROGRESS`, `BLOCKED_EXTERNAL`,
  `READY_FOR_REVIEW` y `DONE`. Una casilla marcada certifica la tarea descrita;
  no equivale a aceptación del subbloque. No basta una fusión para inventar pruebas.
- Cada encargo toma **un subbloque** y termina con su handoff e índice actualizado.
  Las tareas de subbloques posteriores permanecen sin marcar.
- Las especificaciones principales se actualizan al sincronizar/archivar un cambio
  verificado. No copiar deltas pendientes a las principales para aparentar avance.

## Mapa completo del backlog

Los nombres futuros son destinos propuestos; solo B00 se crea ahora.

| Bloque / cambio | Fuente | Dependencias |
|---|---|---|
| B00 / `b00-foundation` | [B00](tasks/B00.md) | Ninguna |
| B01 / `b01-local-persistence-dataset` | [B01](tasks/B01.md) | B00 |
| B02 / `b02-purchasing-domain-mcp` | [B02](tasks/B02.md) | B01 |
| B03 / `b03-durable-agent` | [B03](tasks/B03.md) | B02 |
| B04 / `b04-azure-identity-preflight` | [B04](tasks/B04.md) | B03 |
| B05 / `b05-async-api-worker` | [B05](tasks/B05.md) | B03 |
| B06 / `b06-real-authorization` | [B06](tasks/B06.md) | B04, B05 |
| B07 / `b07-process-ui` | [B07](tasks/B07.md) | B05 |
| B08 / `b08-ephemeral-azure-demo` | [B08](tasks/B08.md) | B06, B07 |
| B09 / `b09-skills-memory-subagents` | [B09](tasks/B09.md) | B03, B05 |
| B10 / `b10-evaluation-observability` | [B10](tasks/B10.md) | B08, B09 |
| B11 / `b11-portfolio-reproduction` | [B11](tasks/B11.md) | B10 |
| B12 / `b12-optional-graph` | [B12](tasks/B12.md) | B11; opcional |

Cada cambio tendrá propuesta, diseño, deltas con escenarios y tareas que mantengan
los cuatro IDs originales. Revisar código y handoffs antes de crearlo: el mapa
no demuestra que sus dependencias estén disponibles.

## Uso desde Copilot con Codex

Las implementaciones siguen [el protocolo de agentes](DEVELOPMENT_AGENTS.md)
y los modelos/esfuerzos de [AGENTS.md](../AGENTS.md). El coordinador selecciona
cambio y subbloque; planner prepara decisiones, worker aplica y reviewer verifica.
Los límites del cliente y la activación se explican en esa guía.

En el **chat**, indicar por ejemplo:

```text
Usa openspec-apply-change con b00-foundation e implementa únicamente B00.2.
```

La petición de implementación determina el alcance; no aplicar automáticamente
todo el bloque. Si faltan artefactos, prepararlos con `openspec-propose` antes
de aplicar. El modo `openspec-explore` sirve para investigar y decidir.

En **PowerShell**, desde la raíz, usar el lanzador `.cmd` cuando la política de
scripts impida ejecutar el `.ps1`, sin modificar la política del equipo:

```powershell
openspec.cmd context --json
openspec.cmd list --json
openspec.cmd status --change b00-foundation
openspec.cmd instructions apply --change b00-foundation --json
openspec.cmd validate b00-foundation --strict
```

Versión de generación y validación inicial: OpenSpec 1.16.0. La configuración de
Copilot mantiene `cloudAgent: false`. Versionar configuración, cambios y skills
junto al proyecto; no ejecutar `init` de nuevo sobre el repositorio configurado.
Archivar solo tras completar y comprobar la puerta de salida del bloque.

## Cambios de herramientas de desarrollo

Los encargos transversales que no implementan B00–B12 usan una ficha DEV y
`tooling_tasks` en el índice. DEV.1 se sigue en
[dev-agent-orchestration](../openspec/changes/dev-agent-orchestration/).
Un cambio exclusivo de configuración/documentación puede declarar
`skip_specs: true` sin inventar requisitos de producto. Conserva propuesta,
diseño, tareas verificables y handoff; esto no exime a cambios de comportamiento
del producto de escribir sus especificaciones.
