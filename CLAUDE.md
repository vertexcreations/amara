# Vestra - Estado del Proyecto

## 📍 Dónde estamos (8 de Junio, 2026 - Distribución Lista)

### Módulos Implementados ✅

1. **Módulo Mercadería** - Completamente funcional
   - CRUD de mercaderías (lotes de productos)
   - Cálculo automático de inversión, ganancia, retorno
   - Tabla de resumen por lote

2. **Módulo Inventario** - Rediseño completo
   - Filtros reorganizados (Search, Category, **Merchandise**, Date range)
   - Asignación en bloque (bulk operations) de productos a mercaderías
   - Checkboxes y toolbar de acciones

3. **Módulo Reportes** - Dual-tab redesign
   - **Tab Mercadería**: Resumen agregado por lote con inversión/ganancia/retorno
   - **Tab Items**: Individual product sales con todas las métricas (inversión, ganancia, retorno)
   - Filtros por mes/año (con opción de día específico)
   - Totales al pie de cada tabla

---

## 🔧 Cambios Recientes (Último Session)

### Routes.py (`/api/reports/items-sold`)
**Líneas 512-562**
- Retorna items individuales vendidos (no agrupado)
- Nuevos campos agregados en esta session:
  - `cost_price`: Costo unitario del producto
  - `investment`: costo_unitario × cantidad_vendida
  - `profit`: (precio_venta - costo_unitario) × cantidad_vendida
  - `return`: profit - investment
- Otros campos: id, name, sku, quantity, price_at_sale, total, sale_date, sale_time, merchandise

### Templates/reports.html
**Tab Items (Líneas 92-122)**
- Tabla con 9 columnas: Item | Mercadería | Fecha Venta | Cantidad | Precio | Total | Inversión | Ganancia | Retorno
- Fila de totales con sumas de inversión, ganancia, retorno
- Estilos: ganancia verde, retorno con color condicional (verde/rojo)

**JavaScript renderReport() (Líneas 292-316)**
- Calcula: totalInvestmentItems, totalProfitItems, totalReturnItems
- Renderiza todas las columnas con formatCurrency()
- Fila de totales con estilos consistentes

---

## 📋 Archivos Principales

### Backend
- `models.py` - Modelos: Product (con merchandise_id FK), Merchandise, Sale, SaleItem
- `routes.py` - Endpoints principales:
  - `GET /api/merchandise` - Listar mercaderías
  - `POST /api/merchandise` - Crear mercadería
  - `POST /api/merchandise/assign-products` - Asignar productos en lote
  - `GET /api/reports/merchandise` - Reportes por mercadería
  - `GET /api/reports/items-sold` - Reportes de items individuales

### Frontend
- `templates/reports.html` - Página de reportes (dual-tab)
- `templates/inventory.html` - Página de inventario con bulk operations
- `templates/merchandise.html` - CRUD de mercaderías
- `static/script.js` - API client y utilitarios globales

---

## ✨ Decisiones de Diseño UX

1. **Filtros en Main Toolbar** (no en bulk toolbar)
   - Separación clara: Filtros = lectura, Toolbar = acciones
   - Merchandise filter siempre disponible, no solo al seleccionar items

2. **Modal de Asignación Compacto**
   - Muestra primeros 8 productos
   - Badge con total de items
   - "... y X más" para overflow
   - Evita abrumar al usuario con listas largas

3. **Reportes: Dual-Tab, No Cards**
   - Tab Mercadería: Agregado por lote
   - Tab Items: Granular, por venta individual
   - Totales como fila final de tabla (no cards laterales)
   - Consistente con estilo inventory "list-like"

---

## 🧪 Testing Pendiente / Próximos Pasos

**Inmediato** (probar en navegador después de cambios):
- [ ] Recargar reportes (Ctrl+Shift+R)
- [ ] Tab Items debe mostrar 9 columnas
- [ ] Verificar cálculos de inversión/ganancia/retorno
- [ ] Totales deben sumar correctamente

**Futuro** (Phase 2, opcional según cliente):
- [ ] Exportar reportes a PDF/Excel
- [ ] Gráficos de análisis (tendencias mes a mes)
- [ ] Alertas para mercaderías con retorno negativo
- [ ] Desglose de reportes por categoría

---

## 📌 Notas Importantes

- **Validaciones**: Estrictas en filtros (mes 1-12, año 2020-2099, día 1-31)
- **Datos por Defecto**: Reportes cargan automáticamente mes/año actual
- **Formatos**: Fechas en DD/MM/YYYY, moneda con formatCurrency()
- **FK directo**: Product.merchandise_id (no tabla intermedia)
  - Un producto asignado a UNA mercadería a la vez
  - Se puede reasignar o desvincularse (merchandise_id = NULL)

---

## 🎨 Patrones UI Establecidos

- **Botones primarios**: `.btn.btn-primary` 
- **Acciones destructivas**: Color rojo/gris
- **Colores de datos**: Verde para ganancia/éxito, rojo para retorno negativo
- **Tablas**: Sticky headers, hover effects, border-bottom para totales
- **Espaciado**: Compact (py-3 px-4), sin excesivos paddings

---

---

## 🚀 Distribución Compilada (8 de Junio, 2026)

**Archivo ejecutable:** `dist/amara.exe` (20.51 MB)

### Cambios en esta sesión:
- ✅ Corrección de evento de cierre: Ahora guarda datos al cerrar con "X"
- ✅ Mejora en script de compilación: Validaciones robustas y limpieza automática
- ✅ Botón "Cerrar" mejorado visualmente (más grande, mejor legibilidad)
- ✅ Compilación exitosa de amara.exe

### Características de la distribución:
- **Autónoma**: No requiere Python instalado
- **BD automática**: Crea SQLite en `%APPDATA%\MiTiendaPoS\` (datos persisten)
- **Guardado seguro**: Commit de BD al cerrar (botón o X)
- **Datos locales**: No requiere conexión a internet

---

**Última actualización**: 08/06/2026 - amara.exe compilado y listo para distribución
