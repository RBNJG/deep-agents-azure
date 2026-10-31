# Instrucciones para agentes

Este archivo es la guía vigente para trabajar en Procurement Agent Workbench. Complementa las instrucciones del usuario y no reemplaza instrucciones de alcance más específico en subdirectorios.

## Orquestación de implementaciones con OpenSpec

- Trabaja siempre con OpenSpec: selecciona cambio y subbloque, consulta estado e instrucciones y lee sus artefactos antes de implementar. Si faltan, prepáralos con la skill correspondiente respetando su límite de planificación y la autorización vigente. No apliques el bloque entero por defecto.
- Para las implementaciones, delega explícitamente el razonamiento en `planner`, el código en `worker` y la revisión independiente en `reviewer`. El coordinador integra y mantiene el handoff y el índice. Puede reutilizar un plan existente comprobado; no necesita volver a generarlo.
- Coordinador, `planner`, `reviewer` y cualquier agente que investigue o tome decisiones usan **`gpt-6.1-sol` con esfuerzo `high`**. Solo la implementación de tareas ya razonadas usa **`gpt-6-luna` con esfuerzo `medium`**. El worker devuelve las decisiones abiertas al planner.
- La configuración está en [.codex/config.toml](.codex/config.toml) y los roles en [.codex/agents/](.codex/agents/). Sigue [la guía de agentes](docs/DEVELOPMENT_AGENTS.md) para delegar, activar y comprobar modelos. Si el host no carga roles, aplica explícitamente ese mismo modelo/esfuerzo e instrucciones; usa contexto mínimo y `fork_turns=none` cuando el host lo requiera para cambiar modelo. Si no lo admite, informa del límite antes de atribuir la separación de costes a la sesión.
- Secuencial por defecto: plan → implementación → revisión → correcciones. Como máximo dos subagentes concurrentes, solo para trabajo independiente. Los subagentes no delegan a otros agentes. No crees agentes para saludos o preguntas sin trabajo de implementación.
- Cada delegación define cambio, subbloque, casillas, decisiones, archivos propios, dependencias, criterios y validaciones. Los workers no están solos: deben conservar cambios ajenos. Coordina contratos, lockfile y migraciones con un único responsable.
- La revisión contrasta diff y OpenSpec; las correcciones vuelven al worker. El coordinador solo propone `READY_FOR_REVIEW`; `DONE` y archivo requieren cumplir los criterios y la revisión establecida.

## Antes de cambiar código

- Lee `docs/PROJECT_CONTEXT.md`, `docs/CONTRACTS.md`, `docs/DEVELOPMENT_PLAN.md`, el encargo `docs/tasks/<BLOQUE>.md` y los handoffs de sus dependencias.
- Inspecciona el repositorio y comprueba en código que las dependencias declaradas están disponibles. Los documentos describen el objetivo; no prueban que algo esté implementado.
- Implementa solo el subbloque asignado. Reutiliza los contratos compartidos; no redefinas `ActorContext`, `Money`, `Run`, `ActionApproval` o `PurchaseDecision` en cada servicio.
- Respeta los ADRs aceptados en `docs/adr/`. Si hace falta cambiar una decisión, registra el motivo, el impacto y la migración en un ADR y actualiza contratos y consumidores dentro del alcance acordado.

## Stack y límites de seguridad

- Stack acordado: Python, FastAPI, Deep Agents sobre LangGraph, servidor MCP propio, PostgreSQL, Terraform y Azure temporal para demos. Consulta `docs/PROJECT_CONTEXT.md` para los componentes y perfiles.
- Separa lógica de negocio determinista, transporte MCP, runtime del agente e infraestructura.
- No expongas la aprobación humana de compra como herramienta autónoma del LLM.
- No uses tokens de desarrollo en cloud ni guardes secretos en Git, Terraform state público, colas, checkpoints o trazas.
- Toda escritura relevante es idempotente y se autoriza en el servidor, también tras una reanudación.
- Las identidades delegada de usuario y de workload son distintas. Un error de autorización delegada no se resuelve usando más permisos de servicio.

## Pruebas y entrega

- Empieza por pruebas económicas; indica si cada validación usa dobles, servicios locales, un LLM real o Azure real.
- No declares una integración real terminada sin probarla. Registra impedimentos externos concretos.
- No hagas refactors globales ni incorpores servicios de pago fuera del alcance sin justificarlo.
- Al cerrar cada subbloque, añade `docs/handoffs/<ID>.md` usando `docs/handoffs/README.md` y actualiza el estado de la tarea correspondiente en `docs/tasks/index.json`.
- Usa los estados `TODO`, `IN_PROGRESS`, `BLOCKED_EXTERNAL`, `READY_FOR_REVIEW` y `DONE` según `docs/EXECUTION_GUIDE.md`. `DONE` requiere que se haya comprobado el criterio de salida; una entrega pendiente de revisión queda `READY_FOR_REVIEW`.
