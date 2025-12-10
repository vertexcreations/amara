import webview
import sys
import threading
import time
import os
from app import create_app

# Crear la aplicación Flask
app = create_app()

def start_server():
    # Ejecutar Flask en un hilo separado
    # use_reloader=False es importante para que no intente reiniciar en el hilo
    app.run(host='127.0.0.1', port=54321, use_reloader=False)

if __name__ == '__main__':
    # Verificar si ya existe la base de datos en modo "congelado" (exe)
    # En modo exe, sys.executable es el path al exe
    # Queremos que la DB se guarde junto al exe, no dentro de la carpeta temporal _MEIPASS
    # Verificar si estamos en el ejecutable para logs o debugging si fuera necesario
    if getattr(sys, 'frozen', False):
        pass

    # Iniciar el servidor Flask en un hilo
    t = threading.Thread(target=start_server)
    t.daemon = True
    t.start()

    # Esperar un momento para asegurar que el servidor arranque
    time.sleep(1)

    # Iniciar la ventana nativa
    webview.create_window(
        'Mi Tienda PoS', 
        'http://127.0.0.1:54321',
        width=1200,
        height=800,
        resizable=True,
        min_size=(800, 600)
    )
    
    webview.start()
