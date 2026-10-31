# Tasks

Encargo vigente: **solo B00.2**. B00.1 aporta la entrega documental ya integrada;
su índice conserva `READY_FOR_REVIEW`. B00.3 y B00.4 no se implementan en este encargo.
Las casillas acreditan su descripción, no la aceptación final del bloque.

## 1. B00.1 — Integrar contexto y decisiones (LOCAL, sin dependencias)

- [x] 1.1 Comprobar contexto, contratos, mapa de rutas, cuatro ADRs y handoff existentes contra la entrega fusionada mediante PR #1; conservar el estado de revisión del índice y registrar el antecedente en la propuesta.

## 2. B00.2 — Esqueleto y entorno (LOCAL, depende de B00.1)

- [x] 2.1 Crear paquete instalable Python 3.12 con uv y lockfile; comprobar instalación congelada y construcción de distribución, y documentar versiones y comandos.
- [x] 2.2 Crear configuración tipada y entradas mínimas de API, worker y MCP con health/readiness; probar configuración ausente/inválida y disponibilidad antes, durante y después del lifespan sin publicar configuración.
- [x] 2.3 Añadir Ruff, tipos estrictos, pytest, comando común de comprobación, tareas VS Code y CI económica; ejecutar el mismo flujo local y un smoke HTTP de los tres procesos, y documentar su alcance.
- [x] 2.4 Preparar Dockerfile sin root, Compose de tres servicios, healthchecks y configuración de ejemplo sin secretos; documentar construcción, arranque y retirada locales.
- [x] 2.5 Ejecutar Docker Compose build/up, comprobar health/readiness de los tres contenedores y retirarlos; registrar resultados reales o el impedimento externo concreto sin marcar esta casilla si no se ejecutó.
- [x] 2.6 Escribir docs/handoffs/B00.2.md con resultados y límites; actualizar únicamente B00.2 en el índice con estado respaldado por evidencia y comprobar la coherencia con estas casillas.

## 3. B00.3 — Contratos v0 (LOCAL, depende de B00.2)

- [ ] 3.1 Materializar modelos/enums compartidos de docs/CONTRACTS.md, sin redefinirlos por servicio; exportar schemas y fixtures y probar rechazo de entradas inválidas y round-trip de Decimal/versiones.
- [ ] 3.2 Implementar canonicalización/hashes y errores estables; probar equivalencia por orden de claves y diferencias materiales, y verificar que schemas LLM no permiten identidad efectiva.
- [ ] 3.3 Documentar contratos y separar ActionApproval/PurchaseDecision; ejecutar sus comprobaciones, escribir handoff B00.3 y actualizar su estado en el índice.

## 4. B00.4 — Compatibilidad de SDKs (LOCAL, depende de B00.3)

- [ ] 4.1 Fijar combinación Deep Agents/LangGraph/MCP/cliente y saver/store PostgreSQL mediante fuentes oficiales y resolución del lockfile; registrar versiones y disponibilidad sin afirmar conectividad PostgreSQL.
- [ ] 4.2 Implementar prueba de eco con agente y modelo simulado usando MCP HTTP real; probar éxito y transporte ausente sin fallback a llamada directa y documentar el comando reproducible.
- [ ] 4.3 Crear ADR de compatibilidad, ejecutar la prueba de transporte, escribir handoff B00.4 y actualizar su estado; comprobar la puerta de salida del bloque con las cuatro entregas.

## Workflow follow-up

- Conciliar la revisión de B00.1 con la PR fusionada y los criterios originales antes de declarar DONE.
- Revisar cada subbloque y verificar la puerta de salida de B00 antes de sincronizar/archivar.
- Crear B01 únicamente tras comprobar las dependencias reales; conservar el resto del mapa en docs/OPENSPEC_WORKFLOW.md.
