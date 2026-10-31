# Procurement Agent Workbench

Asistente de compras técnicas basado en Python, Deep Agents/LangGraph y un servidor MCP propio. PostgreSQL aporta persistencia; Terraform provisiona una demo temporal en Azure.

## Guía del repositorio

- [Contexto, alcance y mapa de componentes](docs/PROJECT_CONTEXT.md)
- [Contratos compartidos](docs/CONTRACTS.md)
- [Decisiones de arquitectura aceptadas](docs/adr/README.md)
- [Plan y dependencias](docs/DEVELOPMENT_PLAN.md)
- [Backlog por bloques y subbloques](docs/tasks/index.json) y [encargo B00](docs/tasks/B00.md)
- [Cómo ejecutar y entregar tareas](docs/EXECUTION_GUIDE.md)
- [Desarrollo local y comprobaciones](docs/LOCAL_DEVELOPMENT.md)
- [Flujo OpenSpec y mapa del backlog](docs/OPENSPEC_WORKFLOW.md)
- [Handoffs entre sesiones](docs/handoffs/README.md)

## Estado

El repositorio está materializando la fundación B00. B00.1 aporta documentación y decisiones. B00.2 incorpora el paquete Python y los procesos API/worker/MCP con sondas de salud; su estado y validaciones están en el índice y el handoff. El dominio de compras, los contratos ejecutables, el runtime agéntico y la infraestructura Azure siguen pendientes. OpenSpec conserva el alcance y seguimiento del bloque sin confundir planificación con implementación.
