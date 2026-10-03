# Instrucciones para agentes del proyecto

Este archivo es una propuesta para integrar en el repositorio de Procurement Agent Workbench. No reemplazar instrucciones existentes sin conciliarlas.

- Lee docs/PROJECT_CONTEXT.md, docs/CONTRACTS.md y el archivo del bloque/subbloque asignado.
- Implementa solo el subbloque pedido, con sus dependencias verificadas en código y handoffs.
- Reutiliza los contratos compartidos; no redefines ActorContext, Money, Run o Approval en cada servicio.
- Python/FastAPI/Deep Agents/LangGraph, PostgreSQL, MCP, Terraform y Azure son decisiones del proyecto.
- Separa lógica de negocio determinista, transporte MCP, runtime del agente e infraestructura.
- No expongas aprobaciones humanas de compra como herramientas autónomas del LLM.
- No uses tokens de desarrollo en cloud ni guardes secretos en Git, state público, colas, checkpoints o trazas.
- Toda escritura relevante es idempotente y se autoriza en servidor, también tras una reanudación.
- Pruebas económicas primero; etiqueta qué se ha validado con dobles y qué con servicios reales.
- No declares una integración real terminada sin probarla; documenta impedimentos externos.
- Al cerrar el trabajo añade docs/handoffs/<ID>.md y actualiza el estado de la tarea.
- No hagas refactors globales ni incorpores servicios de pago nuevos fuera del alcance sin justificar el cambio.
