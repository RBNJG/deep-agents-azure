# ADR 0004: Microsoft Graph como extensión opcional

- Estado: Aceptado
- Fecha: 2026-10-03
- Alcance: acceso futuro a correo/archivos Microsoft 365

## Contexto

El caso principal puede demostrarse con dataset sintético, bandeja interna de demo y sistemas propios. Dependencia de una licencia, consentimiento o tipo particular de cuenta Microsoft impediría el recorrido base.

## Decisión

Microsoft Graph es una extensión opcional posterior al núcleo, planificada en B12. El producto base no requiere licencia Microsoft 365, no envía correo real y no depende de Graph para cargar datos o eliminar Azure. El perfil Graph se identifica explícitamente y su acceso delegado requiere una cuenta y permisos compatibles.

## Consecuencias

- La bandeja por defecto es interna y nunca afirma enviar correo real.
- Graph no bloquea B00–B11 ni la demo base.
- La extensión debe reutilizar ingestión y referencias de evidencia existentes, limitar acceso y dejar intacto el perfil básico al desactivarse.
- Se mantiene fuera el pago a proveedores y la compra real.

## Cuestiones abiertas

En B12 evaluar tipo de cuenta, APIs disponibles, scopes/consentimiento, flujo OBO y restricciones de licencia. No se presupone que cuentas personales y cuentas de trabajo soporten la misma cadena.

## Referencias

`docs/PROJECT_CONTEXT.md`, `docs/CONTRACTS.md`, el bloque B12 de `docs/tasks/index.json` y las secciones Graph de `docs/ARCHITECTURE_REFERENCE.md`.
