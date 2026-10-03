# ADR 0003: Separar identidades y autoridad

- Estado: Aceptado
- Fecha: 2026-10-03
- Alcance: usuarios, API, worker, MCP, datos e inicialización

## Contexto

El solicitante, aprobador, usuario ajeno al proyecto y los workloads tienen capacidades diferentes. La identidad que accede finalmente a Azure no sustituye el permiso del usuario sobre una acción o un objeto. Una decisión de compra debe ser humana y separada de la autorización de una herramienta.

## Decisión

La aplicación valida identidad delegada, scopes, roles y membresías del usuario en el servidor. Workloads usan principals/UAMIs separados con permisos mínimos; la inicialización/migración tiene una identidad distinta de runtime. El worker no escribe decisiones humanas. MCP vuelve a validar contexto, autorización e idempotencia antes de cada efecto, incluso al reanudar una ejecución. El modelo no elige tenant, actor, usuario ni credenciales. La aprobación/rechazo de compra solo se ofrece mediante un endpoint humano autenticado y un comando de dominio, nunca como herramienta autónoma del LLM.

## Consecuencias

- Un error de autorización delegada se corrige en la identidad/permiso delegado, no elevando permisos del servicio.
- App-only se rechaza en operaciones que requieran un usuario.
- Los subagentes que comparten proceso no quedan aislados por identidad Azure; aislamiento fuerte requeriría workloads separados.
- PostgreSQL aplica roles SQL además de la identidad de administración Azure.
- Tests simulados no prueban la cadena real de Entra/UAMI; B04/B06 deben guardar evidencia separada.

## Cuestiones abiertas

Definir la emisión/verificación concreta del contexto confiable API→MCP, app registrations/roles/scopes y principales SQL, y decidir usuarios reales de prueba en B04/B06. No se consideran resueltos por crear el modelo de contrato.

## Referencias

`docs/PROJECT_CONTEXT.md`, `docs/CONTRACTS.md` y las secciones de identidad de `docs/ARCHITECTURE_REFERENCE.md`.
