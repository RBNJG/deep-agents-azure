# ADR 0002: Demo Azure efímera con Terraform

- Estado: Aceptado
- Fecha: 2026-10-03
- Alcance: integración y demos cloud

## Contexto

La demo debe probar identidades y servicios reales de Azure, pero no mantener recursos facturables entre sesiones. El flujo de desarrollo habitual sigue siendo local y económico.

## Decisión

Azure se provisiona solo para pruebas de integración y demostraciones identificadas, y se elimina al acabar. Terraform describe la infraestructura reutilizable. El perfil inicial ejecuta deploy desde el equipo con state local protegido, cifrado y guardado fuera de Git; se conserva el mismo state para `apply` y `destroy`. Backend remoto y OIDC son ampliaciones opcionales, no requisitos iniciales. El proceso incluye preflight, límites/tags, destrucción e inventario de residuos; nunca elimina el state mientras haya recursos pendientes.

## Consecuencias

- El recorrido básico no puede depender de recursos Azure persistentes.
- La identidad de despliegue y el state requieren protección; el state puede contener datos sensibles.
- Hay que validar destroy y posibles recursos retenidos (por ejemplo, soft-delete de Key Vault) como parte del ciclo de demo.
- Las imágenes, código, dataset y resultados seleccionados se conservan fuera de la infraestructura efímera; secretos y state no se publican.
- Tener Terraform no equivale a haber desplegado o destruido correctamente.

## Cuestiones abiertas

La suscripción, tenant, región, cuota, política de nombres, límites de gasto y operador autorizado se confirman antes de B04. Los módulos, recursos mínimos y comandos reproducibles se concretan en B04/B08.

## Referencias

`docs/PROJECT_CONTEXT.md`, `docs/DEVELOPMENT_PLAN.md` y las secciones de coste/despliegue de `docs/ARCHITECTURE_REFERENCE.md`.
