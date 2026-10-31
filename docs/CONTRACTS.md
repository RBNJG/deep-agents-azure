# Contratos de implementación v0

Estas son decisiones iniciales del proyecto, no firmas garantizadas de un SDK. B00.3 las convierte en modelos y schemas. Si se cambia un contrato, actualizar consumidor, productor, tests y ADR en la misma entrega o acordar antes la migración.

## Entidades y valores comunes

| Contrato | Campos mínimos y reglas |
|---|---|
| ActorContext | tenant_id, subject_id, actor_type user/service, client_id, scopes, app_roles y memberships resueltas por servidor. Nunca argumento libre del modelo. |
| Money | amount como decimal serializado en string y currency=EUR. Cantidades, impuestos, descuentos y transporte son campos separados; desconocido no significa cero. |
| Quote / QuoteLine | id estable, supplier_id, project_id, fecha/vigencia, cantidades, precios, condiciones, fuente y versión. |
| EvidenceRef | artifact_id, content_hash, página o celda, extractor_version y fecha de extracción. No URLs firmadas duraderas. |
| PurchaseRequest | project_id, requester_id, quote_version_ids, total, status, version y justification. |
| Run | id, thread_id, tenant_id, owner_id, project_id, status, version y referencias a configuración/versiones. |
| PendingAction | id, run_id, interrupt_id, type, esquema de respuesta, destinatario/rol permitido, argumentos canónicos, hashes y expires_at. |
| ActionApproval | pending_action_id, decisión humana, actor, argumento/artefacto exacto, destino, caducidad y consumo idempotente. |
| PurchaseDecision | purchase_request_id, expected_version, approve/reject, actor y comentario; rol y separación de funciones comprobados en dominio. |
| Artifact | id, proyecto, ubicación interna, hash, MIME, tamaño, visibilidad y source_run. |
| ExecutionCommand | schema_version, command_id, environment_id, run_id, thread_id, expected_version, start/resume, response_ref y correlation_id. Sin token ni contenido grande. |
| ToolResult | resultado estructurado, referencias a evidencias y error estable; distinguir error de dominio, autorización y fallo transitorio. |

Estados del run: QUEUED, RUNNING, WAITING_INPUT, WAITING_APPROVAL, WAITING_AUTH, SUCCEEDED, FAILED y CANCELLED. Tipos de espera: QUESTION, TOOL_APPROVAL, PURCHASE_APPROVAL, DELEGATED_TOOL y SUPPLIER_RESPONSE. La proyección de producto se reconcilia con el checkpoint; no asumir que se escriben en una única transacción.

Estados de compra: DRAFT, PENDING_APPROVAL, APPROVED, REJECTED, SUBMITTED y CANCELLED. Una modificación material incrementa version y exige nueva decisión. SUBMITTED significa tramitada en el sistema propio, no compra o pago real.

## Herramientas MCP

| Nombre | Principal | Control |
|---|---|---|
| get_inventory | Servicio | Proyecto autorizado por contexto de ejecución verificado |
| get_purchasing_policy | Servicio | Política publicada de ese proyecto |
| get_project_quotes | Usuario | Membresía del proyecto y scope de lectura |
| compare_quotes | Usuario | Ofertas accesibles al usuario; cálculo determinista en dominio y referencias a evidencias |
| save_comparison_report | Servicio | Artefacto privado en un destino permitido |
| create_purchase_request | Usuario | Dueño real, versión y requisitos completos; crea PENDING_APPROVAL |
| request_supplier_clarification | Usuario | Aprobación de mensaje/destinatario y bandeja de demo por defecto |
| submit_purchase_request | Servicio | Compra aprobada, versión exacta e idempotencia |
| propose_skill_revision | Servicio | Solo candidato; sin permiso de promoción |

approve_purchase_request queda reservado al endpoint humano de la API y a un comando de dominio, no al conjunto de herramientas del LLM. La política de proyecto puede exigir que requester_id y approver_id sean distintos. Un token app-only se rechaza en herramientas que exigen usuario.

El servicio valida el run y su relación con el proyecto. No confiar en un project_id elegido por el modelo solo porque el llamante tiene una UAMI. Usar un registro de ejecución consultable por MCP o un contexto firmado de corta duración emitido por un componente de confianza; no inventar identidad mediante cabeceras sin verificar.

## API mínima

- POST /runs; GET /runs/{id}; GET /runs/{id}/events.
- POST /runs/{id}/answers; POST /runs/{id}/decisions; POST /runs/{id}/cancel.
- POST /delegated-calls/{id}/execute: argumentos recuperados del servidor y respuesta de herramienta obtenida por la API.
- GET /purchase-requests y POST /purchase-requests/{id}/decisions: bandeja y decisión del aprobador, sin acceso implícito a todas las conversaciones.
- GET /artifacts/{id}; POST /runs/{id}/feedback.

El resultado de una decisión de compra se guarda y publica como evento de dominio. El worker del solicitante lo consume sin recibir ni conservar el token del aprobador. No reanudar el hilo con la identidad del último usuario que pulsó un botón.

## Idempotencia y errores

Una operación externa usa action_id/idempotency_key estable, ligado a payload_hash y proyecto. Repetir clave y payload devuelve el resultado previo; misma clave y payload distinto es conflicto. Efectos y diario se coordinan con transacción/outbox o reconciliación cuando hay Blob/cola de por medio.

Errores mínimos: VALIDATION_ERROR, FORBIDDEN, NOT_FOUND, VERSION_CONFLICT, APPROVAL_REQUIRED, APPROVAL_EXPIRED, AUTH_REQUIRED, TRANSIENT_FAILURE y BUDGET_EXCEEDED. Mapear a HTTP/MCP según transporte sin filtrar existencia de objetos ajenos.

## Versiones y seguridad de desarrollo

Guardar commit, image_digest, model_config_hash, skill_set_version, policy_version, dataset_version y schema_version. Aplicar límites de tamaño, timeouts, pasos y concurrencia. La configuración cloud rechaza cualquier proveedor de identidad de desarrollo. Ni tests ni fixtures incluyen credenciales reales.

## Representación implementada en B00.3

Los modelos compartidos están en `packages/contracts/models.py`; los schemas JSON
versionados se regeneran con `python -m scripts.export_contract_schemas`. Los
objetos rechazan campos extra, versiones menores que 1 y errores de enumeración.
`Money` usa EUR, importe no negativo y salida decimal en string; rechaza floats
binarios. Transporte desconocido se representa mediante `null`. `EvidenceRef`
exige exactamente página o celda. Los validadores de Python también comprueban
reglas entre campos que JSON Schema no expresa necesariamente.

`ActionApproval` y `PurchaseDecision` son contratos distintos y exigen un actor
de tipo usuario; esto no verifica su identidad, rol ni permisos. Esa verificación,
la separación de funciones, el consumo idempotente y la reautorización siguen
siendo responsabilidades de los servicios posteriores. Los schemas de entrada
provisionales del catálogo de herramientas no contienen identidad ni credenciales;
no implementan ni publican el transporte MCP. El servidor deberá determinar y
comprobar proyecto y contexto efectivo, incluso si recibe un identificador.

La canonicalización v1 acepta únicamente objetos/listas JSON, strings, enteros,
booleanos y null; rechaza floats, claves no string y objetos Python. Serializar
previamente los modelos con `model_dump(mode="json")`, con importes como strings.
Se ordenan las claves, se conserva el orden de listas y los strings y se codifica
UTF-8 sin espacios; SHA-256 se calcula sobre esos bytes. Distintas representaciones
textuales decimales, como `1.0` y `1.00`, producen hashes distintos: el productor
debe fijar su representación antes de crear o verificar una aprobación. Esta regla
no supone normalización Unicode ni implementa por sí sola el diario idempotente.
El error Pydantic se traduce a `VALIDATION_ERROR` en el transporte futuro; el
contrato `ContractError` define los códigos, no su mapeo HTTP/MCP.
