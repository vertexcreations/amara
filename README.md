# Mi Tienda PoS

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
cd AppPoS
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
4.  Al finalizar, encontrarás el ejecutable en la carpeta **`dist/MiTiendaPoS.exe`**.

### Opción B: Manualmente

1.  Activa tu entorno virtual.
2.  Instala las herramientas necesarias:
    ```bash
    pip install pyinstaller pywebview
    ```
3.  Ejecuta el comando de compilación:
    ```bash
    # En Windows (usa ; como separador)
    pyinstaller --noconsole --onefile --name "MiTiendaPoS" --add-data "templates;templates" --add-data "static;static" desktop_app.py

    # En Linux/Mac (usa : como separador)
    pyinstaller --noconsole --onefile --name "MiTiendaPoS" --add-data "templates:templates" --add-data "static:static" desktop_app.py
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

## Tecnologías

*   **Backend**: Python, Flask, SQLAlchemy.
*   **Frontend**: HTML5, CSS3 (Vanilla), JavaScript.
*   **Base de Datos**: SQLite.

---

© 2025 Vertex Creations. Todos los derechos reservados.
