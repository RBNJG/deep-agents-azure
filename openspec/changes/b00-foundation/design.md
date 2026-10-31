# Design

## Context

Ver `proposal.md` para motivación y alcance. La inspección de las tres ramas remotas confirma que solo existe documentación. `dev` contiene la PR #1 (B00.1), pero el índice mantiene `READY_FOR_REVIEW`. El encargo actual limita la implementación a B00.2.

## Goals / Non-Goals

**Goals:** Un único paquete Python instalable, tres puntos de entrada y utilidades comunes, con lockfile y comprobaciones económicas. Mantener las responsabilidades en las rutas ya acordadas.

**Non-Goals:** Implementar contratos de negocio, el transporte MCP o el runtime agéntico en B00.2. Un proceso de salud del worker no consume colas. No se prepara infraestructura Azure ni se cambia ningún ADR aceptado.

## Decisions

1. **Python 3.12 y uv.** El equipo dispone de Python 3.12.1. Los metadatos oficiales de Deep Agents (>=3.11), LangGraph, MCP y saver PostgreSQL (>=3.10) admiten 3.12; esto no demuestra integración. Fijar la serie 3.12 en el proyecto y lockfile frente a usar el Python 3.15 predeterminado del equipo sin certificar. Usar uv con versión fijada y lockfile versionado frente a instalaciones independientes por proceso. B00.4 incorporará y probará la combinación exacta de SDKs; no instalar el runtime completo por anticipado.
2. **Un paquete raíz y namespaces existentes.** Distribuir `apps` y `packages` con un único proyecto, manteniendo los directorios de contratos, dominio, agentes y plataforma separados. Evitar un workspace de múltiples distribuciones mientras aún no hay interfaces implementadas. El namespace `packages.platform` evita ocultar el módulo estándar `platform`. Usar editable exacto de Hatch y `editables` en desarrollo: Python 3.12/Windows con locale cp1252 interpreta incorrectamente una ruta UTF-8 con tilde escrita directamente en un `.pth`; el importador exacto conserva la ruta y permite ejecutar desde otro directorio. Las wheels de producción no necesitan este importador.
3. **Factories sin efectos al importar.** Cada entrada carga configuración al arrancar, no al importar módulos. Configuración tipada con prefijo `PAW_`, identificador de entorno obligatorio, puertos validados y perfil local explícito. Ninguna credencial por defecto. Rechazar perfiles futuros hasta implementar sus garantías.
4. **Ciclo de vida común.** Los tres servicios usan FastAPI para sondas. `/health` prueba vida del proceso; `/ready` refleja inicialización y cierre mediante lifespan. Las respuestas identifican el servicio y no incluyen configuración. No publicar un endpoint MCP ficticio. No confundir el servicio de sondas del worker con un ejecutor de segmentos.
5. **Contenedor común, comando por servicio.** Una imagen sin root instala el proyecto desde el lockfile; Compose configura tres procesos y puertos, sin BD ni Azurite hasta B01. Un check HTTP estándar sirve como healthcheck. Comandos Python portables y tareas VS Code para desarrollo y validación; CI económica repite el mismo flujo sin secretos.
6. **Calidad y evidencia.** Ruff, mypy estricto y pytest. Pruebas ASGI locales para configuración y transición de disponibilidad; un smoke de procesos reales comprueba HTTP y cierre. Separar estas pruebas de MCP/LLM/Azure. Documentar si Docker no está instalado y mantener pendiente esa comprobación, sin declarar B00 completo.
7. **Trazabilidad incremental.** El mapa B00–B12 vive en `docs/OPENSPEC_WORKFLOW.md`; solo se crea B00 ahora. No convertir requisitos futuros en principales. Mantener B00.1 en revisión y separar sus evidencias históricas de las validaciones nuevas. B00.3 usa los campos de `docs/CONTRACTS.md`; B00.4 agrega la prueba de eco y su ADR de compatibilidad.

## Risks / Trade-offs

- Metadatos compatibles no garantizan que los SDKs colaboren: B00.4 prueba el transporte real con modelo simulado antes de ampliar.
- Docker ausente en el equipo: verificar lo disponible y registrar la construcción/arranque como comprobación externa pendiente si no hay motor.
- Doble seguimiento: mantener IDs estables, handoff e índice junto a las casillas; no deducir `DONE` de una casilla ni de una PR.
- Readiness inicial limitada al ciclo de vida: los futuros bloques incorporarán dependencias reales cuando existan; ahora no afirmar conexión a PostgreSQL, colas o identidad.

## Migration Plan

Incorporar configuración y artefactos OpenSpec, implementar B00.2, comprobar instalación y servicios, registrar handoff e índice. No hay datos que migrar. El rollback revierte los archivos de este subbloque; nunca borra configuración local, state ni recursos externos.

## Open Questions

B00.3 fija schemas exportados y canonicalización exacta dentro de los contratos existentes. B00.4 selecciona y prueba las APIs exactas de runtime/MCP y saver/store. B01 incorpora infraestructura local de datos. No bloquean el esqueleto de B00.2.
