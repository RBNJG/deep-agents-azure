# Spec Delta

## Purpose

Comprobar que la combinación elegida del runtime agéntico y el transporte de herramientas realiza una llamada local completa antes de ampliar el producto. Trazabilidad: B00.4.

## ADDED Requirements

### Requirement: Llamada de herramienta sobre transporte real
Una prueba local MUST ejecutar un agente con modelo simulado capaz de tool calling, descubrir una herramienta de eco MCP por HTTP, invocarla y devolver su resultado sin sustituir el transporte por una llamada directa a la función.

#### Scenario: Recorrido de eco
- **WHEN** se ejecuta la prueba local con el servidor MCP activo
- **THEN** se observa la llamada HTTP de herramienta y el resultado de eco esperado en el agente

#### Scenario: Transporte indisponible
- **WHEN** el servidor MCP no está disponible
- **THEN** la prueba falla explícitamente y no utiliza un fallback de llamada directa

### Requirement: Compatibilidad documentada con alcance verificable
El informe de compatibilidad MUST registrar versiones fijadas y referencias oficiales. MUST distinguir disponibilidad de paquetes de saver/store PostgreSQL de persistencia realmente probada.

#### Scenario: Informe tras la prueba
- **WHEN** se registra la combinación comprobada
- **THEN** el informe identifica runtime, MCP, cliente, Python, comandos y resultados observados

#### Scenario: Base de datos no probada
- **WHEN** solo se ha comprobado la disponibilidad del paquete PostgreSQL
- **THEN** el informe no afirma haber probado conectividad o recuperación duradera
