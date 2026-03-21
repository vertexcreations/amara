===============================================
        APPPOS v3.0 - SISTEMA DE PUNTO DE VENTA
===============================================

CONTENIDO DEL PAQUETE:
- dist/MiTiendaPoS.exe - Aplicacion principal
- templates/ - Plantillas HTML
- static/ - Archivos de estilos e imagenes
- instance/ - Base de datos (se crea automaticamente)
- dist/backups/ - Respaldos de base de datos

===============================================
        INSTALACION
===============================================

REQUISITOS:
- Windows 7 o superior (64-bit recomendado)
- 500 MB de espacio en disco
- Sin requerimientos adicionales (todo incluido)

PASOS:
1. Copiar carpeta completa a destino deseado
2. Doble-click en: dist/MiTiendaPoS.exe
3. La aplicacion se abrira en el navegador (http://localhost:5000)
4. Al primer inicio, se crea automaticamente la base de datos

===============================================
        USO BASICO
===============================================

SECCION PRINCIPAL:
- Inventario: Gestionar productos y categorias
- POS: Realizar ventas
- Historial: Ver ventas registradas
- Dashboard: Estadisticas del dia

MENU SUPERIOR:
- Crear categoria: Agregar nueva categoria de productos
- Agregar producto: Nuevo producto con precio y stock
- Backup: Respaldar o restaurar base de datos

===============================================
        FUNCIONALIDADES CLAVE
===============================================

PROTECCIONES IMPLEMENTADAS:
- No se puede eliminar productos con ventas registradas
- No se puede eliminar categorias con productos
- El historial de ventas nunca se pierde
- Respaldos automaticos de datos
- Validacion de precios y cantidades

DATOS GUARDADOS:
- Productos: nombre, SKU, precio, costo, stock, categoria
- Ventas: fecha/hora, items vendidos, monto total, ganancia
- Categorias: nombre, cantidad de productos
- Respaldos: historial completo de datos

===============================================
        RESPALDOS Y RECUPERACION
===============================================

CREAR BACKUP:
1. Click en menu "Backup"
2. Click en "Crear respaldo"
3. Se guarda automaticamente en dist/backups/

RESTAURAR BACKUP:
1. Click en menu "Backup"
2. Seleccionar respaldo de la lista
3. Click en "Restaurar"
4. IMPORTANTE: La aplicacion se reiniciara automaticamente
5. Se crea respaldo de seguridad antes de restaurar

UBICACIONES:
- BD Principal: instance/pos.db
- Respaldos: dist/backups/backup_YYYYMMDD_HHMMSS.db
- Respaldo de seguridad: instance/pos.db.safety

===============================================
        TROUBLESHOOTING
===============================================

PROBLEMA: El navegador no se abre
SOLUCION: Abrir manualmente http://localhost:5000

PROBLEMA: La BD se corrupto
SOLUCION:
1. Ir a Menu > Backup
2. Seleccionar respaldo anterior
3. Restaurar
4. Reiniciar aplicacion

PROBLEMA: Stock inconsistente
SOLUCION:
- Verificar que no haya eliminado productos con ventas
- Ver historial de ventas para auditar movimientos

PROBLEMA: Error de permisos
SOLUCION:
- Ejecutar como Administrador: Click derecho > Ejecutar como administrador

===============================================
        DATOS IMPORTANTES
===============================================

UBICACION ARCHIVOS:
- C:\Users\[Usuario]\AppPoS_2\instance\pos.db (BD principal)
- C:\Users\[Usuario]\AppPoS_2\dist\backups\ (Respaldos)

RESPALDO MANUAL:
Para respaldo externo, copiar:
- instance/pos.db
- dist/backups/ (carpeta completa)

===============================================
        SOPORTE
===============================================

Para problemas o consultas, contactar al equipo de desarrollo.

Versión: 3.0
Fecha: Marzo 2026
Estado: Produccion

===============================================
