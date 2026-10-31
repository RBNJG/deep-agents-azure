# Spec Delta

## Purpose

Permitir comprobar que cada proceso del producto está vivo y preparado para atender trabajo, con configuración explícita y errores de arranque observables. Trazabilidad: B00.2.

## ADDED Requirements

### Requirement: Arranque con configuración explícita
Cada servicio MUST exigir un identificador de entorno válido antes de arrancar y MUST rechazar configuración inválida sin inventar valores obligatorios ni mostrar secretos.

#### Scenario: Identificador ausente
- **WHEN** se intenta arrancar API, worker o MCP sin identificador de entorno
- **THEN** el proceso termina con error de configuración que identifica el campo obligatorio

#### Scenario: Configuración inválida
- **WHEN** se configura un puerto fuera de rango o un perfil no soportado
- **THEN** el servicio rechaza el arranque y explica el campo incorrecto

### Requirement: Señales diferenciadas de salud y disponibilidad
API, worker y MCP SHALL exponer `/health` para vida del proceso y `/ready` para disponibilidad. `/ready` MUST devolver 503 antes de inicializarse y después del cierre, y 200 cuando se complete el arranque.

#### Scenario: Proceso preparado
- **WHEN** un servicio completa su ciclo de arranque local
- **THEN** `/health` y `/ready` responden 200 e identifican el servicio

#### Scenario: Proceso no preparado
- **WHEN** el proceso está vivo pero aún no se ha inicializado o ya se ha cerrado
- **THEN** `/health` responde 200 y `/ready` responde 503

### Requirement: Entorno reproducible de desarrollo
Un checkout limpio MUST poder instalar el proyecto y herramientas de calidad usando el lockfile, ejecutar comprobaciones locales y arrancar los tres servicios con configuración de ejemplo sin credenciales reales.

#### Scenario: Instalación y comprobación local
- **WHEN** se instala con el lockfile y se ejecuta el comando documentado de comprobaciones
- **THEN** se validan estilo, tipos y escenarios de arranque sin LLM ni Azure

#### Scenario: Arranque en contenedores
- **WHEN** se construyen y arrancan los servicios con Docker siguiendo la guía y su configuración de ejemplo
- **THEN** los tres contenedores ofrecen sus señales de salud en puertos independientes
