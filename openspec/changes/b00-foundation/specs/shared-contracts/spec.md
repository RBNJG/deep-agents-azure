# Spec Delta

## Purpose

Garantizar un lenguaje compartido entre servicios para identidad, importes, ejecución y decisiones, sin delegar la autoridad al modelo. Trazabilidad: B00.3; fuente normativa de campos: docs/CONTRACTS.md.

## ADDED Requirements

### Requirement: Intercambio estable de contratos v0
Los contratos compartidos SHALL conservar decimales y versiones al serializar y deserializar, y MUST rechazar datos inválidos según los contratos v0 aceptados.

#### Scenario: Importe en un intercambio
- **WHEN** se serializa y deserializa un importe válido
- **THEN** su valor decimal y moneda se conservan sin redondeo binario

#### Scenario: Datos inválidos
- **WHEN** se recibe un estado, importe o campo no permitido por su contrato
- **THEN** la validación rechaza la entrada con un error estable

### Requirement: Identidad y decisiones separadas
Los schemas expuestos al LLM MUST impedir elegir la identidad efectiva. La aprobación de herramienta y la decisión humana de compra MUST ser contratos diferentes.

#### Scenario: Argumentos del modelo
- **WHEN** se inspeccionan los schemas publicados para herramientas
- **THEN** no permiten que el modelo seleccione credenciales o identidad efectiva

#### Scenario: Dos clases de decisión
- **WHEN** se registra una aprobación de herramienta o una decisión de compra
- **THEN** cada decisión se valida con su propio contrato y referencias

### Requirement: Argumentos canónicos para idempotencia
La canonicalización MUST producir el mismo hash para argumentos semánticamente equivalentes y distinguir cambios materiales de payload según las reglas compartidas.

#### Scenario: Orden de campos
- **WHEN** solo cambia el orden de las claves de unos argumentos equivalentes
- **THEN** se obtiene el mismo hash canónico

#### Scenario: Payload diferente
- **WHEN** cambia un valor material de los argumentos
- **THEN** se obtiene un hash diferente
