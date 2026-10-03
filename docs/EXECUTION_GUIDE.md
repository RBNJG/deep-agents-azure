# Cómo encargar el trabajo a agentes de código

## Unidad de trabajo

Un bloque entrega una capacidad revisable. Un subbloque es el encargo habitual de un agente y debería caber en una PR centrada. No pedir a un agente que implemente el paquete entero en una sesión. Si un subbloque crece, dividirlo preservando interfaces y criterios de salida.

Antes de empezar: leer AGENTS.md, PROJECT_CONTEXT.md, CONTRACTS.md, el bloque elegido y los handoffs de dependencias; inspeccionar el código real. Los documentos describen el objetivo, no prueban que una dependencia esté implementada.

Orden de autoridad: instrucciones vigentes del usuario, restricciones reales del repositorio, contratos aceptados/ADRs y esta planificación. El archivo AGENTS.md del paquete se integra con el existente; no lo sustituye a ciegas. La referencia de arquitectura explica el contexto; esta guía precisa el orden y los contratos, incluida la separación entre decisión de compra y aprobación de herramienta.

## Prompt de encargo

    Implementa únicamente el subbloque <ID> de Procurement Agent Workbench.
    Lee AGENTS.md, docs/PROJECT_CONTEXT.md, docs/CONTRACTS.md,
    docs/tasks/<BLOQUE>.md y los handoffs de sus dependencias.
    Comprueba qué existe realmente y qué dependencias están terminadas.
    Mantén el stack y los contratos acordados. Limita cambios al alcance
    del subbloque; cualquier cambio transversal debe quedar explícito.
    Implementa el resultado completo y ejecuta las comprobaciones indicadas.
    Distingue pruebas locales, simuladas, con LLM y con Azure real.
    No inventes resultados ni ocultes dependencias externas sin configurar.
    Al terminar, escribe docs/handoffs/<ID>.md con cambios, comandos y
    resultados, decisiones, limitaciones y siguiente paso desbloqueado.
    Si falta una credencial o permiso, completa lo local posible y registra
    el impedimento concreto. No marques la prueba cloud como superada.

## Entrega y revisión

Cada entrega incluye commit/PR, lista de archivos, interfaces/migraciones, pruebas realmente ejecutadas, resultados observados y pasos para reproducir. Un TODO en el camino principal no satisface el criterio de aceptación. No sustituir MCP por llamadas directas a Python para hacer pasar una prueba end-to-end.

Estados del backlog: TODO, IN_PROGRESS, BLOCKED_EXTERNAL, READY_FOR_REVIEW y DONE. DONE exige comprobar el criterio de salida; el autor puede proponer READY_FOR_REVIEW y el mantenedor aceptar la entrega. El index.json se entrega con todas las tareas TODO; no constituye evidencia de avance.

No hay que terminar Azure para desarrollar código local: B05, B07 y B09 pueden avanzar con sus dependencias locales mientras un preflight cloud queda bloqueado. B08/B10/B11 no pueden declarar demo Azure completa si faltan las pruebas reales de B04/B06.

Para reducir gasto, preparar primero el código y las comprobaciones locales de cada bloque; agrupar después sus pruebas Azure en sesiones cortas y retirar el entorno al acabar. B06 y los bloques posteriores recrean lo necesario con IaC: no dependen de mantener vivo el entorno de B04. El conjunto de 30–50 casos de B10 incluye pruebas deterministas económicas; no todos requieren modelo real ni Azure.

## Uso de varios agentes

Orden secuencial por defecto. Con contratos estables, B04 y B05 admiten trabajo independiente; B07 y B09 también, después de B05. Para trabajo paralelo usar ramas/worktrees, un responsable de integración y propiedad de archivos. Evitar cambios simultáneos de contratos, lockfile o migraciones sin coordinación. No juntar ramas basándose solo en que sus tests aislados pasan.

## Coste y entornos

Las tareas indican modo: LOCAL, LLM o AZURE. LOCAL no provisiona cloud. LLM necesita configuración y límites de gasto de la sesión. AZURE usa una suscripción, environment_id y state identificados, con preflight y retirada; respetar la autorización vigente y los controles del repositorio. Una tarea de código no da permiso para borrar entornos ajenos.

No modificar presupuestos, consentimientos o permisos para sortear un error. Investigar y documentar la causa. Un deploy fallido conserva el state para poder limpiar. Los datos de seed y reset son sintéticos y pertenecen al entorno de demo identificado.

## Continuidad entre sesiones

El siguiente agente recibe contexto compartido, subbloque actual y handoff anterior; no necesita toda la conversación. El handoff informa de hechos del repositorio, no de planes imaginados. Las decisiones nuevas se añaden a ADR y los cambios de contrato se reflejan en CONTRACTS.md.

Crear primero B00.1. Al terminar cada bloque, ejecutar su puerta de salida antes de avanzar por la ruta recomendada. Las fuentes del SDK se verifican al fijar versiones; no copiar ejemplos de versiones distintas sin comprobarlos.
