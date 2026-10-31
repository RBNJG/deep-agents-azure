# Diseño de agentes de desarrollo

## Context

Ver [propuesta](proposal.md). El proyecto ya utiliza OpenSpec 1.16.0 y dispone
de Python 3.12 para validaciones locales. Codex instalado informa
`0.164.0-alpha.11.1`; su catálogo local contiene los dos modelos y esfuerzos.
No hay configuración `.codex/` previa. Los ADRs de producto y contratos
compartidos siguen vigentes; esta configuración no cambia esas decisiones.

## Goals / Non-Goals

Asignar capacidad y esfuerzo explícitos por responsabilidad y hacer reutilizable
el protocolo entre sesiones. Mantener el backlog de producto B00–B12 separado
de DEV.1. No elegir el proveedor/modelo del agente de compras.

## Decisions

1. **Configuración nativa por proyecto.** `.codex/config.toml` selecciona
   `gpt-6.1-sol`/`high` para el coordinador y subagentes sin rol especializado.
   Los TOML autónomos de `.codex/agents/` definen `planner`, `worker` y `reviewer`
   con `name`, `description`, `developer_instructions`, modelo y esfuerzo.
   Se evita cambiar preferencias globales y se reutiliza el nombre integrado
   `worker` para que la implementación no herede un modelo más caro.
2. **Capacidad por función.** Planner y reviewer usan `gpt-6.1-sol`/`high`;
   worker, `gpt-6-luna`/`medium`. Es la distinción recomendada por la
   [documentación oficial](https://learn.chatgpt.com/docs/agent-configuration/subagents)
   para trabajo exigente frente a tareas estrechas. No se fija una tarifa ni
   se promete un porcentaje de ahorro. Ante ambigüedad, el worker devuelve
   la decisión al planner; no cambia silenciosamente de modelo.
3. **OpenSpec y propiedad.** Coordinador selecciona cambio y subbloque;
   planner razona y mantiene artefactos, worker implementa las casillas
   autorizadas, reviewer contrasta artefactos y diff sin editarlos.
   El coordinador integra, actualiza handoff/índice y comunica límites.
   Cada delegación recibe rutas, dependencias, criterios y comandos concretos.
4. **Coste de coordinación.** Secuencial por defecto; máximo dos subagentes
   concurrentes y sin delegación recursiva. Paralelizar solo tareas independientes
   con propiedad/aislamiento acordados. Reutilizar resúmenes y revisar el diff
   final; repetir revisión cuando las correcciones cambien el comportamiento.
5. **Clientes y permisos.** Si el host no descubre roles TOML pero permite elegir
   modelo/esfuerzo, utilizar el mismo mapa explícitamente y contexto mínimo
   (`fork_turns=none` cuando lo exija el host). Si no puede aplicarlo, registrar
   el límite sin declarar activa la separación. Los roles heredan permisos;
   una instrucción de revisión sin edición no es una sandbox independiente.

## Risks / Trade-offs

- Configuración ignorada por un cliente o carpeta sin confianza → documentar
  reinicio, confianza y verificación del modelo/rol en la primera delegación.
- Worker de menor capacidad encuentra trabajo ambiguo → planificador descompone
  y resuelve contratos antes de continuar. No abaratar revisión o diseño.
- Más agentes pueden consumir más tokens → pocas delegaciones acotadas,
  secuenciales y sin exploración/revisión duplicada.
- Validación estática no demuestra inferencia → informar exactamente lo probado;
  no lanzar modelos reales como prueba de esta configuración.

## Migration Plan

Versionar configuración e instrucciones, abrir nueva sesión Codex en el proyecto
y verificar que el host descubre los roles. Reversión: retirar únicamente la
configuración y los añadidos de DEV.1, conservando cambios ajenos.
No hay migración de datos ni cambios de dependencias.

Validación LOCAL: parseo TOML/JSON, coherencia de modelos/esfuerzos y trazabilidad,
OpenSpec estricto y whitespace. Sin dobles de negocio, LLM real ni Azure real.
