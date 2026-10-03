# Contexto compartido: Procurement Agent Workbench

Fecha: 1 de octubre de 2026. Documento de desarrollo, no implementación existente. El repo de destino todavía no se ha conectado ni modificado.

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
