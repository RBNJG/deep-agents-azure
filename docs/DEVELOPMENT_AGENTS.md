# Agentes para implementar el proyecto

Esta configuración corresponde al asistente de desarrollo Codex. Los agentes
del producto, su proveedor LLM y los subagentes de B09 conservan su planificación.

## Roles y coste

| Responsabilidad | Configuración | Modelo | Esfuerzo |
|---|---|---|---|
| Coordinador: alcance, decisiones finales e integración | [config.toml](../.codex/config.toml) | `gpt-6.1-sol` | `high` |
| Planner: análisis, diseño y artefactos OpenSpec | [planner.toml](../.codex/agents/planner.toml) | `gpt-6.1-sol` | `high` |
| Worker: código y pruebas con decisiones resueltas | [worker.toml](../.codex/agents/worker.toml) | `gpt-6-luna` | `medium` |
| Reviewer: revisión independiente y verificación | [reviewer.toml](../.codex/agents/reviewer.toml) | `gpt-6.1-sol` | `high` |

Los agentes sin especialización heredan el nivel de razonamiento capaz. El rol
`worker` sustituye al integrado con el mismo nombre en clientes compatibles.
La selección sigue la [documentación oficial de subagentes Codex](https://learn.chatgpt.com/docs/agent-configuration/subagents):
Sol para trabajo exigente y Luna para tareas estrechas de menor coste. El catálogo
local consultado el 2026-10-31 incluye ambos y sus esfuerzos. No se promete un
ahorro fijo: más delegaciones, contexto o reintentos también consumen tokens.

## Flujo obligatorio

1. El coordinador delimita **un subbloque** y selecciona el cambio según
   [el flujo OpenSpec](OPENSPEC_WORKFLOW.md). Consulta `context`, `list`, `status`
   e `instructions apply`; lee los `contextFiles` y comprueba dependencias reales.
   Un estado `blocked` impide implementar. Preparar artefactos no ejecuta código
   ni autoriza por sí mismo la implementación.
2. Delega en `planner` el análisis que falte. Usa `openspec-explore`,
   `openspec-propose` o `openspec-update-change` según corresponda. Reutiliza
   artefactos comprobados. El planner devuelve decisiones, casillas, archivos,
   interfaces y aceptación; cualquier pregunta material se resuelve antes del código.
3. Delega en `worker` las tareas ya razonadas mediante `openspec-apply-change`.
   Entrega la ficha y handoffs, propiedad de archivos, restricciones y comandos.
   El worker conserva cambios ajenos y verifica cada casilla antes de marcarla.
   Si descubre un problema de diseño, devuelve evidencia al planner.
4. Delega en `reviewer` la revisión del diff final y su evidencia mediante
   `openspec-verify-change`. Comprueba contratos, escenarios, seguridad,
   idempotencia y qué pruebas se han ejecutado realmente. Devuelve hallazgos
   con prioridad, archivo/línea y corrección. No edita la implementación.
5. Las correcciones vuelven al worker; las decisiones nuevas, al planner.
   Revisa de nuevo el comportamiento corregido. El coordinador integra y
   mantiene [handoff](handoffs/README.md), casillas e [índice](tasks/index.json)
   en `READY_FOR_REVIEW`. Solo la aceptación según
   [la guía de ejecución](EXECUTION_GUIDE.md) permite `DONE`.
6. Sincroniza/archiva con las skills correspondientes únicamente cuando se
   cumpla la puerta de salida de **todo el bloque**. No archivar B00 por acabar B00.3.

El coordinador no sustituye al worker escribiendo código de producto ni delega
decisiones de arquitectura en el modelo económico. Los roles planner/reviewer
leen fuentes y el planner puede escribir planificación; el código lo escribe el worker.

## Encargo mínimo para cada delegación

```text
Cambio OpenSpec: <nombre>; subbloque: <ID>; rol: <planner|worker|reviewer>.
Casillas exactas: <IDs y rutas devueltas por instructions apply>.
Fuentes: AGENTS.md, contexto, contratos, ADRs, ficha y handoffs de dependencias.
Dependencias comprobadas y decisiones resueltas: <resumen con evidencia>.
Archivos asignados: <lista>; interfaces que conservar: <lista>.
Criterios de aceptación y comandos económicos: <lista>.
Entorno permitido: LOCAL / dobles / LLM / AZURE, con límites de la sesión.
No estás solo: conserva cambios ajenos y no edites fuera de tu propiedad.
Devuelve archivos, resultados observados, riesgos y cuestiones abiertas.
No crees subagentes ni marques tu entrega DONE.
```

## Activación y compatibilidad

Abrir **una nueva sesión Codex** en la raíz después de guardar la configuración.
La sesión ya abierta puede mantener su modelo y catálogo anteriores. Codex carga
configuración de proyecto en carpetas de confianza; si la ignora, comprobar la
confianza en el cliente. No modificar permisos o configuración global como solución
automática. Overrides explícitos de la sesión pueden cambiar el modelo del coordinador:
comprobar que sigue en Sol/`high`.

Los TOML de [agentes](../.codex/agents/) se descubren por su campo `name` en
clientes Codex compatibles; no necesitan registros `agents.<rol>.config_file`.
Comprobar al iniciar la primera delegación los nombres disponibles y el
modelo/esfuerzo efectivo de planner, worker y reviewer. Validar TOML solo comprueba
sintaxis y política; no demuestra que el host haya cargado el rol o hecho inferencia.

Si el host de VS Code/Copilot no descubre estos roles pero permite elegir modelo
y esfuerzo al delegar, cargar las instrucciones del TOML y pasar explícitamente
el par correspondiente. Cuando una bifurcación con historial completo impida
cambiar modelo, usar `fork_turns=none` y el encargo mínimo. No asumir que una
etiqueta `worker` implica Luna o `medium`. Si el host no permite fijarlos,
informar del límite y usar un cliente compatible para implementar con esta política.

Los roles heredan proveedor, MCP, sandbox y aprobaciones de la sesión principal.
La instrucción de revisión sin edición es conductual, no aislamiento de permisos.
No se configura un proveedor, secreto o recurso Azure adicional.

## Concurrencia y validación

Ejecución secuencial por defecto y límite de dos subagentes concurrentes,
excluyendo el coordinador. El límite del host puede ser menor. No hay delegación
recursiva. Paralelizar solo trabajo independiente con propiedad clara; usar
ramas/worktrees para escrituras paralelas según la guía de ejecución. Un solo
responsable integra contratos, lockfile, migraciones, casillas e índice.

Validar con `openspec.cmd validate <cambio> --strict`, parseo TOML/JSON y revisión
de los pares modelo/esfuerzo. Para esta configuración solo se requieren controles
LOCAL; no se llaman modelos de la aplicación ni Azure. Las pruebas de cada
subbloque se eligen según sus criterios y se registran con su entorno real.

Los encargos de herramientas ajenos a B00–B12 se registran bajo `tooling_tasks`
en el índice y en una [ficha DEV](tasks/DEV.md), con cambio y handoff propios.
Mantienen los mismos estados sin alterar los recuentos ni dependencias del producto.
