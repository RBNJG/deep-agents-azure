# ADR 0001: PostgreSQL para persistencia

- Estado: Aceptado
- Fecha: 2026-10-03
- Alcance: persistencia local y perfil de demo Azure

## Contexto

El producto requiere persistir datos de compras y también pausas/reanudaciones duraderas del agente. Debe poder desarrollarse localmente y usar la misma base tecnológica en la demo con identidad Azure real. Los contratos de negocio y las escrituras del worker necesitan permisos diferenciados.

## Decisión

Usar PostgreSQL como persistencia común. En desarrollo local se ejecutará con Docker. Para integración/demo Azure se usará Azure Database for PostgreSQL Flexible Server temporal. LangGraph saver/store y las tablas de negocio propias vivirán en PostgreSQL; Blob Storage conserva archivos grandes. Esquemas y roles separarán estado del agente, memoria, dominio, control y auditoría, con privilegios mínimos. UAMIs autentican workloads ante Azure; roles SQL controlan el acceso a datos. Migraciones e inicialización usan una identidad distinta de la runtime.

## Consecuencias

- Las mismas abstracciones y migraciones deben servir localmente y en Azure.
- PostgreSQL local es un requisito para las pruebas de persistencia; mocks no validan reinicios duraderos.
- Borrar la base elimina checkpoints; el seed crea una demo limpia y no restaura sesiones antiguas.
- Checkpoints de LangGraph y tablas propias no comparten automáticamente una transacción. Las escrituras entre sistemas requieren idempotencia y reconciliación/outbox cuando corresponda.
- No se declara conectividad UAMI, configuración SQL ni compatibilidad de versiones hasta probarlas en sus tareas.

## Cuestiones abiertas

Fijar versiones de saver/store y combinación con Deep Agents/LangGraph en B00.4; concretar esquemas, roles, migraciones y estrategia de recuperación en B00.3/B01/B03; elegir tamaño y región de Flexible Server en B04 según cuota y coste disponibles.

## Referencias

`docs/PROJECT_CONTEXT.md`, `docs/CONTRACTS.md` y las secciones de persistencia de `docs/ARCHITECTURE_REFERENCE.md`.
