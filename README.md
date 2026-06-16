# Vestra

Sistema de Punto de Venta (PoS) simple y moderno para gestión de inventario y ventas, desarrollado en Python con Flask.

## Requisitos Previos

Antes de comenzar, asegúrate de tener instalado lo siguiente en tu sistema:

1.  **Python 3.8 o superior**:
    *   Descárgalo desde [python.org](https://www.python.org/downloads/).
    *   **IMPORTANTE**: Al instalar, asegúrate de marcar la casilla **"Add Python to PATH"**.
2.  **Git**:
    *   Para clonar el repositorio. Descárgalo desde [git-scm.com](https://git-scm.com/downloads).

## Instalación y Configuración

Sigue estos pasos para obtener una copia del proyecto y ejecutarlo en tu máquina local.

### 1. Clonar el repositorio

Abre tu terminal o línea de comandos y ejecuta:

```bash
git clone <URL_DEL_REPOSITORIO>
cd Vestra
```
*(Reemplaza `<URL_DEL_REPOSITORIO>` con la URL real de tu repositorio Git)*

### 2. Configuración Automática (Windows)

El proyecto incluye un script que facilita la instalación de dependencias y el inicio del sistema.

1.  Busca el archivo **`iniciar_sistema.bat`** en la carpeta del proyecto.
2.  Haz doble clic sobre él.
3.  El script creará automáticamente un entorno virtual, instalará las dependencias necesarias y abrirá la aplicación en tu navegador web predeterminado.

### 3. Configuración Manual (Opcional)

Si prefieres configurar el entorno manualmente, sigue estos pasos en tu terminal:

**Crear un entorno virtual:**

```bash
# En Windows
python -m venv .venv

# En macOS/Linux
python3 -m venv .venv
```

**Activar el entorno virtual:**

```bash
# En Windows
.venv\Scripts\activate

# En macOS/Linux
source .venv/bin/activate
```

**Instalar dependencias:**

```bash
pip install -r requirements.txt
```

## Ejecución del Sistema

Una vez configurado (si lo hiciste manualmente), puedes iniciar la aplicación con:

```bash
python app.py
```

La aplicación estará disponible en `http://127.0.0.1:5000`.

## Crear Ejecutable (.exe)

Si deseas distribuir la aplicación como un archivo ejecutable único (sin necesidad de que el usuario instale Python), sigue estos pasos:

### Opción A: Script Automático (Windows)

1.  Busca el archivo **`crear_ejecutable.bat`**.
2.  Haz doble clic sobre él.
3.  El script instalará `pyinstaller` y generará el archivo `.exe`.
4.  Al finalizar, encontrarás el ejecutable en la carpeta **`dist/Vestra.exe`**.

### Opción B: Manualmente

1.  Activa tu entorno virtual.
2.  Instala las herramientas necesarias:
    ```bash
    pip install pyinstaller pywebview
    ```
3.  Ejecuta el comando de compilación:
    ```bash
    # En Windows (usa ; como separador)
    pyinstaller --noconsole --onefile --name "Vestra" --add-data "templates;templates" --add-data "static;static" desktop_app.py

    # En Linux/Mac (usa : como separador)
    pyinstaller --noconsole --onefile --name "Vestra" --add-data "templates:templates" --add-data "static:static" desktop_app.py
    ```
4.  El archivo generado estará en la carpeta `dist/`.

## Estructura del Proyecto

*   `app.py`: Punto de entrada de la aplicación Flask.
*   `routes.py`: Definición de rutas y lógica del servidor.
*   `models.py`: Modelos de base de datos (SQLAlchemy).
*   `templates/`: Archivos HTML para la interfaz de usuario.
*   `static/`: Archivos CSS, JavaScript e imágenes.
*   `instance/`: Contiene la base de datos SQLite (`pos.db`).
*   `iniciar_sistema.bat`: Script de automatización para Windows.

## Testing

El proyecto incluye tests unitarios y de integración usando `pytest`. Para ejecutar las pruebas:

```bash
# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt

# Ejecutar todos los tests
pytest tests/ -v

# Ejecutar con reporte de cobertura
pytest tests/ --cov=. --cov-report=term-missing
```

Tests disponibles:
- `tests/test_models.py` - Tests de modelos de base de datos
- `tests/test_routes.py` - Tests de rutas y API

## CI/CD - GitHub Actions

Este proyecto está configurado con GitHub Actions para ejecutar tests automáticamente en cada push y pull request a la rama `main`.

### Workflow

El archivo `.github/workflows/ci.yml` define:
- **Trigger**: Push a `main` o PR hacia `main`
- **Environment**: Ubuntu Latest + Python 3.11
- **Steps**:
  1. Checkout del código
  2. Setup de Python 3.11
  3. Instalación de dependencias (requirements.txt + requirements-dev.txt)
  4. Ejecución de tests con pytest
  5. Generación de reporte de cobertura (opcional)

### Para ver el estado de los builds

Dirígete a [GitHub Actions](https://github.com/vertexcreations/amara/actions) para ver:
- Estado de los últimos builds
- Logs detallados de ejecución
- Reportes de cobertura

### Ambiente de Distribución

El binario `.exe` se compila localmente en Windows usando:
```bash
python build_exe.py
```

Output: `dist/amara.exe` (excluido de git mediante `.gitignore`)

Para futuras releases automáticas, se puede agregar un workflow adicional que compile en `windows-latest` runner y publique en GitHub Releases.

## Tecnologías

*   **Backend**: Python, Flask, SQLAlchemy.
*   **Frontend**: HTML5, CSS3 (Vanilla), JavaScript.
*   **Base de Datos**: SQLite.
*   **Testing**: pytest, pytest-flask.
*   **CI/CD**: GitHub Actions.

