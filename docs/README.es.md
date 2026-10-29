# Cloud Resource Audit CLI

[English](../README.md) | **Español** | [Português](README.pt.md)

Herramienta de línea de comandos desarrollada en Python para auditar inventarios simulados de recursos cloud, detectar problemas de configuración y generar reportes estructurados.

## Descripción general

Cloud Resource Audit CLI es una aplicación ligera de Python diseñada para analizar inventarios de infraestructura cloud almacenados en archivos JSON.

La aplicación valida los datos de los recursos, aplica reglas de auditoría predefinidas, calcula estadísticas del inventario y genera un reporte legible directamente en la terminal.

El proyecto demuestra competencias prácticas de ingeniería de software: desarrollo modular en Python, validación de entradas, manejo de excepciones, pruebas automatizadas y empaquetado de aplicaciones de línea de comandos.

**Alcance actual:** La aplicación utiliza inventarios simulados. No se conecta a Azure ni a otros proveedores cloud.

## Funcionalidades

- Carga de inventarios de recursos cloud desde archivos JSON.
- Validación de la estructura del inventario y los atributos de los recursos.
- Detección de problemas de configuración y costos.
- Clasificación de hallazgos por severidad.
- Cálculo de cantidades de recursos y costos mensuales estimados.
- Generación de reportes legibles en la terminal.
- Manejo de archivos y datos inválidos mediante mensajes de error claros.
- Ejecución de auditorías con el comando `cloud-audit`.
- Pruebas automatizadas con pytest.

## Tecnologías utilizadas

- **Python 3.12+** — Desarrollo de la aplicación.
- **Biblioteca estándar de Python** — Procesamiento de JSON, argumentos de línea de comandos y manejo de errores.
- **pytest** — Pruebas automatizadas.
- **setuptools** — Configuración e instalación del paquete Python.
- **Git y GitHub** — Control de versiones.

## Estructura del proyecto

```text
cloud-resource-audit/
├── data/                     # Inventarios JSON de ejemplo
├── src/
│   └── cloud_audit/
│       ├── loader.py         # Carga de archivos JSON
│       ├── validator.py      # Validación del inventario
│       ├── auditor.py        # Reglas de auditoría
│       ├── statistics.py     # Estadísticas del inventario
│       ├── report.py         # Formato del reporte
│       └── cli.py            # Interfaz de línea de comandos
├── tests/                    # Pruebas automatizadas
├── .gitignore
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Instalación

### 1. Clonar el repositorio

Mediante SSH:

```bash
git clone git@github.com:CloudIAIoT/cloud-resource-audit.git
cd cloud-resource-audit
```

Alternativamente, mediante HTTPS:

```bash
git clone https://github.com/CloudIAIoT/cloud-resource-audit.git
cd cloud-resource-audit
```

### 2. Crear un entorno virtual

En Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

En Linux o macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar el proyecto

```bash
python -m pip install -e .
```

La instalación editable registra el comando `cloud-audit`.

## Uso

Ejecutar una auditoría indicando la ruta del inventario JSON:

```bash
cloud-audit data/inventory_clean.json
```

Analizar un inventario que contiene problemas de configuración:

```bash
cloud-audit data/inventory_findings.json
```

Mostrar la ayuda del comando:

```bash
cloud-audit --help
```

## Tipos de recursos admitidos

| Tipo de recurso | Estados admitidos |
|---|---|
| `virtual_machine` | `running`, `stopped` |
| `storage_account` | `active` |

Cada recurso debe incluir un identificador, tipo, estado, costo mensual y diccionario de etiquetas (`tags`).

El campo `environment` es opcional. Si falta, se genera un hallazgo de auditoría en lugar de considerar inválido el inventario.

Los entornos admitidos son `production`, `development` y `test`.

## Reglas de auditoría

La aplicación implementa cuatro reglas:

| Regla | Severidad | Descripción |
|---|---|---|
| `MISSING_OWNER` | Media | El recurso no tiene la etiqueta `owner`. |
| `MISSING_ENVIRONMENT` | Media | El recurso no tiene definido el entorno. |
| `STOPPED_VM_COST` | Alta | Una máquina virtual detenida tiene un costo mensual positivo. |
| `MISSING_PRODUCTION_TAG` | Alta | Un recurso de producción no tiene la etiqueta `criticality`. |

Un mismo recurso puede generar varios hallazgos.

## Ejemplo de salida

El siguiente ejemplo muestra un reporte de un inventario con problemas de configuración:

```text
INVENTORY SUMMARY
Total resources: 3
Virtual machines: 2
Storage accounts: 1
Total monthly cost: $140.75

AUDIT SUMMARY
Total findings: 5
High severity: 2
Medium severity: 3
Low severity: 0

FINDINGS

[MEDIUM] vm-test-01
Rule: MISSING_OWNER
Resource has no owner tag

[HIGH] vm-test-01
Rule: STOPPED_VM_COST
Stopped virtual machine has a positive monthly cost
```

Los hallazgos adicionales se muestran con el mismo formato. Los mensajes de la CLI permanecen en inglés, independientemente del idioma de la documentación.

Los costos mensuales provienen del inventario de entrada. La aplicación no consulta datos reales de facturación cloud.

## Manejo de errores

La CLI maneja errores comunes, entre ellos:

- Archivos de inventario inexistentes.
- Archivos JSON mal formados.
- Estructura de inventario inválida.
- Ausencia de atributos obligatorios.
- Tipos de recursos o estados no admitidos.
- Valores inválidos de costo mensual.

La aplicación devuelve el código de salida `0` cuando la auditoría se ejecuta correctamente, incluso si detecta hallazgos.

Los errores de entrada devuelven el código `1`.

## Pruebas automatizadas

El proyecto utiliza pytest para comprobar la carga, validación, auditoría, estadísticas y generación de reportes.

Instalar pytest si todavía no está disponible:

```bash
python -m pip install pytest
```

Ejecutar las pruebas desde la raíz del repositorio:

```bash
python -m pytest -v
```

## Limitaciones actuales

- Los inventarios deben proporcionarse mediante archivos JSON locales.
- Los tipos de recursos y las reglas de auditoría están predefinidos.
- Los costos mensuales son estimaciones incluidas en el inventario.
- La aplicación no se conecta a infraestructura cloud real.
- Los reportes se muestran en la terminal y no se exportan a archivos.

## Posibles mejoras

- Integración con inventarios de recursos de Azure.
- Reglas adicionales de seguridad, gobernanza y optimización de costos.
- Políticas de auditoría configurables.
- Exportación de reportes en JSON o CSV.
- Ejecución automatizada mediante flujos CI/CD.

## Licencia

No se ha especificado una licencia para este proyecto.
