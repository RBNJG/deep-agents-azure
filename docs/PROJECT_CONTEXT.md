# Contexto compartido: Procurement Agent Workbench

Fecha de revisión: 3 de octubre de 2026. Este documento fija el contexto de producto y las decisiones base; no implica que las capacidades planeadas ya estén implementadas. El estado de trabajo está en `docs/tasks/index.json`.

## Producto

Asistente de compras técnicas: entender una necesidad, consultar inventario y política, comparar ofertas PDF/XLSX, detectar información ausente, pedir aclaraciones, generar una comparativa y tramitar una solicitud con aprobación humana. El dataset es sintético; la persistencia, las acciones sobre el sistema propio y la identidad Azure deben ser reales cuando se use el perfil cloud.

Recorrido de referencia: se necesitan equipos para un laboratorio; hay tres ofertas y una no detalla el transporte; el agente pregunta, espera una respuesta, recalcula mediante código, propone una opción y crea una solicitud pendiente. Un aprobador distinto puede decidir. Reiniciar el worker conserva la espera. Duplicar un mensaje no duplica la solicitud ni la publicación.

## Decisiones fijadas

- Python, FastAPI, Deep Agents sobre LangGraph y servidor MCP propio.
- PostgreSQL local con Docker y Azure Database for PostgreSQL Flexible Server temporal. Checkpointer y Store de LangGraph, más tablas de negocio propias.
- Blob Storage para ficheros; Storage Queue para ejecuciones; Azurite/adaptadores para desarrollo local.
- Dos Container Apps para API/web y MCP; Container Apps Job para ejecutar un segmento hasta terminar o interrumpirse.
- Entra para usuarios y UAMIs por workload; permisos de usuario y de servicio comprobados en MCP.
- Key Vault para credenciales de proveedores que las necesiten, como Langfuse; acceso mediante UAMI y sin incluir valores en Terraform ni en sus outputs.
- Terraform para infraestructura; scripts/Jobs para migraciones y seed. Una única base de código soporta local y Azure.
- GitHub Actions valida y construye imágenes; GHCR público. El perfil inicial despliega desde el equipo con state local protegido, fuera de Git. OIDC y backend remoto son una ampliación opcional.
- Azure existe solo durante integración/demo. Conservar fuera del entorno código, imágenes, dataset, skills aprobadas y resultados seleccionados.
- Langfuse Cloud opcional al inicio y conectado en el bloque de evaluación. Logs correlacionados desde el primer recorrido.
- Microsoft Graph es opcional; el núcleo no necesita una licencia Microsoft 365 ni pagar/comprar realmente a un proveedor.

## Límites del MVP

Un tenant de demostración, dos proyectos y tres perfiles: solicitante, aprobador y usuario ajeno. Moneda EUR y aritmética Decimal con reglas de redondeo explícitas. Documentos de texto/tablas conocidos; OCR, divisas, ERP real y pagos quedan fuera. Se admite una sesión activa por hilo; varias tareas de proyectos distintos deben permanecer aisladas.

El buzón de demo almacena mensajes de prueba dentro del producto y nunca afirma haber enviado correo real. El perfil Graph tendrá una etiqueta distinta. No exponer shell, SQL arbitrario ni selección libre de URLs/credenciales al modelo.

## Identidad y aprobación

Una acción del usuario exige token delegado válido, scopes y permiso sobre el objeto/proyecto. Una acción de servicio exige app role y permisos de su workload. La aplicación calcula el contexto de identidad; el modelo no elige tenant, usuario ni credenciales. Un error delegado no se resuelve usando más permisos de servicio.

La UAMI autentica a PostgreSQL, pero los permisos de datos se configuran mediante roles SQL. El worker no puede escribir decisiones de aprobación. El MCP comprueba esas decisiones antes del efecto. Los subagentes que comparten proceso no tienen aislamiento de UAMI.

Hay dos decisiones diferentes: autorizar una herramienta concreta y aprobar una solicitud de compra. La aprobación de compra es una acción humana autenticada; no se expone al LLM como una herramienta que pueda autoaprobarse. El aprobador de una compra tampoco obtiene acceso libre al hilo privado del solicitante.

## Persistencia y coste

Un interrupt guarda el estado y termina el segmento. No se mantiene un proceso vivo esperando personas. Tokens y secretos nunca se guardan en prompts, checkpoints, colas ni trazas. La entrega de cola es al menos una vez; los efectos se hacen idempotentes.

Eliminar PostgreSQL elimina sus checkpoints. El seed reconstruye una demo limpia, no una sesión antigua. Las skills aceptadas sobreviven en Git; restaurar una sesión requiere snapshot compatible y es una ampliación.

Tests locales usan modelos simulados. Las pruebas con modelo real tienen presupuesto explícito de tokens/llamadas y resultados separados. Los tests de identidad Azure se etiquetan como tales; no se declaran superados con un mock.

## Estructura de código propuesta

| Ruta | Responsabilidad |
|---|---|
| apps/api/ | API, identidad, endpoints humanos y web mínima |
| apps/worker/ | Cola, leases, segmentos y reanudación |
| apps/mcp_server/ | Transporte MCP y autorización de herramientas |
| packages/contracts/ | Pydantic, enums y contratos compartidos |
| packages/domain/ | Compras, reglas y cálculos deterministas |
| packages/agents/ | Harness, herramientas adaptadas, skills y subagentes |
| packages/platform/ | PostgreSQL, storage, identidad, cola y telemetría |
| migrations/ | Evolución de tablas propias y roles |
| demo/datasets/v1/ | Fixtures, manifiesto y generadores |
| skills/ | Procedimientos aprobados |
| infra/ | Terraform reusable y entorno efímero |
| scripts/ | Inicialización, seed, deploy, export y teardown |
| tests/, evals/ | Pruebas y evaluación |

Estas rutas se materializan en B00; no se presupone que ya existan. Evitar varias implementaciones del mismo contrato en servicios distintos.

## Mapa de rutas previsto

El backlog se ejecuta en orden B00–B11; B12 es opcional. Las rutas siguientes son destinos de implementación, no evidencia de código ya creado:

| Ruta | Responsabilidad |
|---|---|
| `apps/api/` | API, identidad, endpoints humanos y web mínima |
| `apps/worker/` | Cola, leases, segmentos y reanudación |
| `apps/mcp_server/` | Transporte MCP, autenticación de llamadas y autorización de herramientas |
| `packages/contracts/` | Modelos Pydantic, enums y contratos compartidos |
| `packages/domain/` | Reglas, cálculos deterministas y decisiones de compras |
| `packages/agents/` | Harness Deep Agents/LangGraph, adaptadores de herramientas, skills y subagentes |
| `packages/platform/` | Adaptadores de PostgreSQL, almacenamiento, cola, identidad y telemetría |
| `migrations/` | Migraciones de negocio, control y auditoría; inicialización de roles |
| `demo/datasets/v1/` | Dataset sintético, manifiesto y generadores reproducibles |
| `skills/` | Procedimientos aprobados con revisión de cambios |
| `infra/` | Módulos Terraform reutilizables y perfil de demo Azure efímera |
| `scripts/` | Desarrollo, migración, seed, preflight, deploy, export y teardown |
| `tests/`, `evals/` | Tests locales, integraciones y evaluaciones separados por entorno |
| `docs/adr/` | Decisiones arquitectónicas y su estado |
| `docs/tasks/`, `docs/handoffs/` | Backlog canónico y contexto transferible por subbloque |

## Decisiones y cuestiones abiertas

Las decisiones acordadas se registran en `docs/adr/README.md`. Aún requieren validación o elección durante los subbloques que les corresponden:

- versiones compatibles y fijadas de Python, Deep Agents, LangGraph, MCP y los paquetes de saver/store PostgreSQL (B00.2–B00.4);
- detalle de esquemas PostgreSQL, roles SQL, migraciones y estrategia de reconciliación entre transacciones propias y checkpoints (B00.3, B01 y B03);
- región, SKU/cuota, nombres y límites concretos para la demo Azure, y si algún experimento de red privada cabe en el presupuesto (B04/B08);
- disponibilidad de tenant, usuarios de prueba, permisos Entra y suscripción Azure para validar identidad real; no hay credenciales ni recursos implícitos en esta planificación (B04/B06);
- proveedor/modelo LLM y presupuesto de llamadas para las pruebas reales; los tests locales usarán modelos simulados (B00.4/B03/B10);
- cuenta, permisos y factibilidad OBO de Microsoft Graph. Graph es opcional y no bloquea el perfil base (B12).
