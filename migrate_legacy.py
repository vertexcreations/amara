
import sqlite3
import os
from app import create_app
from models import db, Product, Category, Sale, SaleItem
from datetime import datetime

# Paths
LEGACY_DB = 'import_backup/backup_pos.db'
CURRENT_DB_PATH = 'instance/pos.db'

def migrate():
    if not os.path.exists(LEGACY_DB):
        print(f"Legacy DB not found at {LEGACY_DB}")
        return

    print("--- Starting Migration ---")
    
    # 1. Connect to Legacy DB
    old_conn = sqlite3.connect(LEGACY_DB)
    old_conn.row_factory = sqlite3.Row
    old_cur = old_conn.cursor()
    
    # 2. Setup Current App Context
    app = create_app()
    with app.app_context():
        # Clear current DB
        print("Clearing current database...")
        db.drop_all()
        db.create_all()
        
        # 3. Migrate Categories
        print("Migrating Categories...")
        old_cur.execute("SELECT * FROM category")
        categories = old_cur.fetchall()
        cat_map = {} # old_id -> new_instance
        
        for old_cat in categories:
            new_cat = Category(
                id=old_cat['id'],
                name=old_cat['name']
            )
            db.session.add(new_cat)
        db.session.commit()
        print(f"Migrated {len(categories)} categories.")

        # 4. Migrate Products
        print("Migrating Products...")
        # Old columns: id, name, sku, size, color, price, cost_price, stock_quantity, category_id
        old_cur.execute("SELECT * FROM product")
        products = old_cur.fetchall()
        
        for old_prod in products:
            # We ignore size and color
            new_prod = Product(
                id=old_prod['id'],
                name=old_prod['name'],
                sku=old_prod['sku'],
                price=old_prod['price'],
                cost_price=old_prod['cost_price'],
                stock_quantity=old_prod['stock_quantity'],
                category_id=old_prod['category_id']
            )
            db.session.add(new_prod)
        db.session.commit()
        print(f"Migrated {len(products)} products.")

        # 5. Migrate Sales & Items
        print("Migrating Sales...")
        old_cur.execute("SELECT * FROM sale")
        sales = old_cur.fetchall()
        
        for old_sale in sales:
            # Handle timestamp string to datetime
            try:
                ts = datetime.fromisoformat(old_sale['timestamp'])
            except:
                try:
                    ts = datetime.strptime(old_sale['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
                except:
                    ts = datetime.now()

            new_sale = Sale(
                id=old_sale['id'],
                timestamp=ts,
                total_amount=old_sale['total_amount']
            )
            db.session.add(new_sale)
        
        db.session.commit()
        print(f"Migrated {len(sales)} sales.")
        
        print("Migrating Sale Items...")
        old_cur.execute("SELECT * FROM sale_item")
        items = old_cur.fetchall()
        
        for old_item in items:
            new_item = SaleItem(
                id=old_item['id'],
                sale_id=old_item['sale_id'],
                product_id=old_item['product_id'],
                quantity=old_item['quantity'],
                price_at_sale=old_item['price_at_sale']
            )
            db.session.add(new_item)
        
        db.session.commit()
        print(f"Migrated {len(items)} sale items.")
        
    old_conn.close()
    print("--- Migration Complete Successfully ---")

if __name__ == '__main__':
    migrate()
