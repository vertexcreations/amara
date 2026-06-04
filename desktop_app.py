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
        try:
            # Dispose database connections gracefully
            from app import db
            db.session.remove()
            db.engine.dispose()
        except Exception as e:
            print(f"Error disposing database: {e}")

        try:
            # Close webview window
            if webview.windows:
                webview.windows[0].destroy()
        except Exception as e:
            print(f"Error closing window: {e}")

        # Graceful exit after cleanup
        def graceful_exit():
            time.sleep(0.5)
            os._exit(0)

        t = threading.Thread(target=graceful_exit, daemon=True)
        t.start()
        return {'success': True, 'message': 'Closing application...'}

if __name__ == '__main__':
    # Usar un Mutex de Windows para asegurar que solo haya una instancia abierta
    from ctypes.wintypes import HANDLE, LPCWSTR, DWORD
    kernel32 = ctypes.windll.kernel32
    # Crear un Mutex global
    mutex = kernel32.CreateMutexW(None, False, "Vestra_SingleInstance_Mutex")
    if kernel32.GetLastError() == 183: # ERROR_ALREADY_EXISTS
        ctypes.windll.user32.MessageBoxW(0, "La aplicación ya se encuentra abierta.", "Error", 0x10)
        sys.exit(0)

    # Configurar logging para modo "congelado" (exe) evitando crashes por consola
    if getattr(sys, 'frozen', False):
        try:
            base = os.environ.get('APPDATA', os.path.expanduser('~'))
            log_dir = os.path.join(base, 'Vestra')
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
    webview.create_window(
        'Vestra',
        f'http://127.0.0.1:{APP_PORT}',
        js_api=api,
        width=1200,
        height=800,
        resizable=True,
        min_size=(800, 600)
    )
    
    webview.start(icon=icon_path)
