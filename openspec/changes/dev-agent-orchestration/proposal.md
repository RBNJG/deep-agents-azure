# Orquestación de agentes de desarrollo

## Why

Las implementaciones necesitan separar decisiones y revisión de la escritura de
código para concentrar el coste de los modelos más capaces en el razonamiento.
El usuario solicita OpenSpec siempre, esfuerzo `high` para razonar y `medium`
para implementar.

## What Changes

- Configurar Codex por proyecto con coordinador, planificador y revisor
  `gpt-6.1-sol`/`high`, y worker `gpt-6-luna`/`medium`.
- Establecer delegación explícita en AGENTS.md: diseño, implementación acotada,
  revisión independiente y corrección, con ejecución secuencial por defecto.
- Integrar el protocolo con OpenSpec, handoffs y estados del índice.
- Documentar activación, límites del cliente y comprobaciones sin inferencia.

## Capabilities

### New Capabilities

Ninguna capacidad de producto: configuración de herramientas de desarrollo.
Este cambio utiliza `skip_specs: true`.

### Modified Capabilities

Ninguna. No modifica el runtime de compras ni sus contratos.

## Impact

Encargo transversal de herramientas **DEV.1**, separado de B00–B12 y registrado
en `docs/tasks/DEV.md`. Fuentes: instrucciones del usuario, AGENTS.md,
documentación compartida, guía de ejecución, flujo OpenSpec y documentación
oficial de subagentes Codex. Dependencias: configuración OpenSpec existente y
entorno local de B00.2, comprobados en disco. B00.3 tiene cambios previos que
se conservan. No requiere que B00.3/B00.4 estén terminados.

Se añaden archivos `.codex/`, guía y handoff, y se amplían instrucciones e índice.
Se excluyen funcionalidades B03/B09, despliegues, llamadas de prueba a modelos,
cambios globales de Codex, instalación de extensiones y modificación de permisos.
La carga efectiva de roles requiere un cliente Codex compatible y una nueva sesión;
la disponibilidad comercial y el ahorro exacto dependen de la cuenta y el uso.
