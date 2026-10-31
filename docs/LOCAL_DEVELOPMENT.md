# Desarrollo local — B00.2

## Prerrequisitos y alcance

Python **3.12**, uv **0.13.6**, Git y, para contenedores, Docker con el plugin Compose
(`docker compose`).
El proyecto fija la serie de Python y las dependencias directas; `uv.lock` fija
la resolución transitiva. No se necesitan LLM, tenant, suscripción Azure ni credenciales.

Esta entrega arranca tres procesos con sondas HTTP. El worker aún no consume
colas y el proceso MCP aún no ofrece transporte ni herramientas. B00.3 materializa
contratos; B00.4 prueba el transporte; B01 incorpora PostgreSQL/Azurite.

## Instalar

Desde la raíz del repositorio, instalar uv con el método oficial preferido
([guía de uv](https://docs.astral.sh/uv/getting-started/installation/)), fijando
la versión 0.13.6. Una alternativa con un Python 3.12 disponible es:

```powershell
py -3.12 -m pip install uv==0.13.6
uv sync --locked
Copy-Item .env.example .env
```

Copiar el ejemplo solo si no se tiene ya una configuración local; conservar los
valores propios. `PAW_ENVIRONMENT_ID` es obligatorio. Solo se admite el perfil
`local`; los puertos deben estar entre 1 y 65535. Los campos desconocidos de `.env`
se ignoran para poder compartir configuración con componentes posteriores.
Un identificador de entorno identifica esta instalación, no otorga autorización.

No hace falta activar la venv ni modificar la política de scripts de PowerShell.
Si uv no está en PATH, utilizar el ejecutable de la instalación correspondiente
(por ejemplo `.venv/Scripts/uv.exe` si se instaló dentro de esa venv).

## Arrancar y comprobar

En tres terminales diferentes, desde la raíz:

```powershell
uv run --locked -- paw-api
uv run --locked -- paw-mcp
uv run --locked -- paw-worker
```

Los puertos predeterminados son 8000, 8001 y 8002, respectivamente. Se pueden
cambiar en `.env`; el host local predeterminado es `127.0.0.1`.

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
Invoke-RestMethod http://127.0.0.1:8000/ready
```

Repetir para los otros puertos. Las respuestas solo incluyen `status` y `service`.
`/health` indica que el proceso atiende HTTP; `/ready` responde 503 fuera del
lifespan inicializado y 200 durante él. Ahora no comprueba dependencias inexistentes.
Detener cada proceso con Ctrl+C.

## Comprobaciones económicas

```powershell
uv run --locked -- python -m scripts.check
uv run --locked -- python -m scripts.smoke_services
uv build
```

El primer comando ejecuta Ruff (lint/formato), mypy estricto y pytest. Las pruebas
usan ASGI local y subprocesos para validar arranque y configuración; no sustituyen
servicios de negocio por mocks. El smoke levanta cada proceso con puertos libres,
comprueba HTTP real y los termina incluso si falla. Ignora `.env` y variables
`PAW_` personales. El proyecto debe estar instalado para ejecutarlo fuera de la raíz.

VS Code ofrece tareas `PAW: check`, `PAW: smoke HTTP` y una por servicio, usando
el intérprete seleccionado. Seleccionar la venv del proyecto, que contiene uv
en el grupo de desarrollo. La CI repite las comprobaciones y además construye/arranca Compose;
añadir el workflow no implica haberlo ejecutado ya en GitHub.

## Docker

Con Docker instalado y el motor activo, desde la raíz con `.env` configurado:

```powershell
docker compose config --quiet
docker compose up --build --wait --wait-timeout 120
Invoke-RestMethod http://127.0.0.1:8000/ready
Invoke-RestMethod http://127.0.0.1:8001/ready
Invoke-RestMethod http://127.0.0.1:8002/ready
docker compose down --remove-orphans
```

El contenedor ejecuta un usuario sin root; los tres servicios tienen sistema de
archivos de solo lectura y un temporal separado. Los puertos publicados se ligan
a loopback; dentro del contenedor se escucha en `0.0.0.0`. La imagen solo copia
fuentes, lockfile y metadatos, no `.env`, Git ni configuración personal.

No hay volúmenes ni base de datos en este subbloque. El teardown anterior solo
retira este proyecto Compose. Si Docker falta, dejar constancia en el handoff y
mantener la comprobación de contenedores pendiente.

Tras instalar Docker Desktop, abrirlo y esperar a que el motor Linux esté activo.
Si una terminal ya abierta no encuentra `docker`, abrir una nueva terminal o
reiniciar VS Code para recoger el PATH actualizado. El [handoff B00.2](handoffs/B00.2.md)
registra la prueba real con Docker Desktop 4.97.0 y Compose v5.6.1.

## Versiones y compatibilidad

La selección de Python 3.12 se apoya en los metadatos oficiales de
[Deep Agents](https://pypi.org/project/deepagents/),
[LangGraph](https://pypi.org/project/langgraph/),
[MCP](https://pypi.org/project/mcp/) y
[saver PostgreSQL](https://pypi.org/project/langgraph-checkpoint-postgres/).
La compatibilidad entre sus APIs todavía debe demostrarse en B00.4; estos paquetes
no se instalan aún como runtime de B00.2. Sus restricciones de Python consultadas
el 31/10/2026 admiten 3.12. No se certifican Python 3.13–3.15 con esta entrega.

Las decisiones de empaquetado y ciclo de vida están en
[el diseño B00](../openspec/changes/b00-foundation/design.md). Para continuar con
OpenSpec, consultar [el flujo y mapa del backlog](OPENSPEC_WORKFLOW.md).
