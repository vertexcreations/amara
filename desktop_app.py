import webview
import sys
import threading
import time
import os
import socket
import ctypes
import signal
import atexit
from app import create_app

# Crear la aplicación Flask
app = create_app()

def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]

APP_PORT = get_free_port()

def start_server():
    # Ejecutar Flask en un hilo separado
    # use_reloader=False es importante para que no intente reiniciar en el hilo

    # Log de endpoints registrados
    print(f"[INFO] Servidor iniciado en http://127.0.0.1:{APP_PORT}")
    print(f"[INFO] Endpoints registrados:")
    for rule in app.url_map.iter_rules():
        if '/api/' in rule.rule:
            methods = ','.join(rule.methods - {'HEAD', 'OPTIONS'})
            print(f"  {methods:6} {rule.rule}")

    app.run(host='127.0.0.1', port=APP_PORT, use_reloader=False)

def on_closing():
    """Handle application closing - save data before exit."""
    print("[INFO] Iniciando cierre de aplicación...")
    try:
        from app import db
        db.session.commit()
        db.session.remove()
        db.engine.dispose()
        print("[INFO] Base de datos guardada y conexiones cerradas")
    except Exception as e:
        print(f"[ERROR] Error al guardar datos: {e}")

    # Liberar el mutex
    try:
        global __mutex_handle
        if __mutex_handle:
            kernel32 = ctypes.windll.kernel32
            kernel32.ReleaseMutex(__mutex_handle)
            kernel32.CloseHandle(__mutex_handle)
            print("[INFO] Mutex liberado")
    except Exception as e:
        print(f"[ERROR] Error al liberar mutex: {e}")

class Api:
    def save_backup_dialog(self, filename):
        import shutil
        import os
        from backup_routes import get_backup_dir

        # Obtener ventana activa
        window = webview.windows[0]

        # Mostrar diálogo de guardado
        result = window.create_file_dialog(
            webview.SAVE_DIALOG,
            save_filename=filename
        )

        if result and len(result) > 0:
            target_path = result[0]
            source_path = os.path.join(get_backup_dir(), filename)

            try:
                shutil.copy2(source_path, target_path)
                return {'success': True}
            except Exception as e:
                return {'success': False, 'message': str(e)}
        return {'success': False, 'message': 'Cancelado'}

    def close_app(self):
        """Gracefully close the application with proper cleanup."""
        print("[INFO] Solicitud de cierre desde interfaz")

        try:
            # Save any pending changes and dispose database connections gracefully
            from app import db
            print("[INFO] Guardando cambios en base de datos...")
            db.session.commit()
            db.session.remove()
            db.engine.dispose()
            print("[INFO] Base de datos guardada correctamente")
        except Exception as e:
            print(f"[ERROR] Error al guardar BD: {e}")

        try:
            # Close webview window
            if webview.windows:
                print("[INFO] Cerrando ventana...")
                webview.windows[0].destroy()
        except Exception as e:
            print(f"[ERROR] Error al cerrar ventana: {e}")

        # Graceful exit after cleanup
        def graceful_exit():
            try:
                # Liberar mutex
                global __mutex_handle
                if __mutex_handle:
                    kernel32 = ctypes.windll.kernel32
                    kernel32.ReleaseMutex(__mutex_handle)
                    kernel32.CloseHandle(__mutex_handle)
                    print("[INFO] Mutex liberado")
            except Exception as e:
                print(f"[ERROR] Error al liberar mutex: {e}")

            time.sleep(0.3)
            print("[INFO] Saliendo de aplicación...")
            os._exit(0)

        t = threading.Thread(target=graceful_exit, daemon=True)
        t.start()
        return {'success': True, 'message': 'Closing application...'}

if __name__ == '__main__':
    # Usar un Mutex de Windows para asegurar que solo haya una instancia abierta
    from ctypes.wintypes import HANDLE, LPCWSTR, DWORD
    kernel32 = ctypes.windll.kernel32
    user32 = ctypes.windll.user32

    # Crear un Mutex global con nombre único
    mutex_name = "amara_SingleInstance_Mutex_2026"
    mutex = kernel32.CreateMutexW(None, True, mutex_name)

    if kernel32.GetLastError() == 183:  # ERROR_ALREADY_EXISTS
        user32.MessageBoxW(0, "La aplicación amara ya se encuentra abierta.\n\nCierre la instancia actual antes de abrir una nueva.", "Aplicación en ejecución", 0x30)
        sys.exit(1)

    # Mantener referencia al mutex para evitar que se libere
    __mutex_handle = mutex

    # Configurar logging para modo "congelado" (exe) evitando crashes por consola
    if getattr(sys, 'frozen', False):
        try:
            base = os.environ.get('APPDATA', os.path.expanduser('~'))
            log_dir = os.path.join(base, 'Amara')
            os.makedirs(log_dir, exist_ok=True)
            log_file = open(os.path.join(log_dir, 'app.log'), 'a', encoding='utf-8')
            sys.stdout = log_file
            sys.stderr = log_file
        except Exception:
            pass

    # Iniciar el servidor Flask en un hilo
    t = threading.Thread(target=start_server)
    t.daemon = True
    t.start()

    # Esperar un momento para asegurar que el servidor arranque
    time.sleep(1)

    # Determinar la ruta del icono
    if getattr(sys, 'frozen', False):
        icon_path = os.path.join(sys._MEIPASS, 'static', 'icon.ico')
    else:
        icon_path = os.path.join(os.path.dirname(__file__), 'static', 'icon.ico')

    api = Api()

    # Iniciar la ventana nativa
    window = webview.create_window(
        'Amara',
        f'http://127.0.0.1:{APP_PORT}',
        js_api=api,
        width=1200,
        height=800,
        resizable=True,
        min_size=(800, 600)
    )

    # Registrar handler para cierre de ventana
    window.events.closing += on_closing

    webview.start(icon=icon_path)
