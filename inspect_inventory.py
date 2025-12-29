
import sqlite3
import os

db_path = 'import_backup/backup_pos.db'

if not os.path.exists(db_path):
    print(f"File not found: {db_path}")
    exit(1)

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check Product specific count
    cursor.execute("SELECT COUNT(*) FROM product")
    count = cursor.fetchone()[0]
    print(f"Found {count} products in inventory.")
    
    # Show first few products to confirm stock
    print("\nSample Products:")
    cursor.execute("SELECT name, stock_quantity, price FROM product LIMIT 5")
    for row in cursor.fetchall():
        print(f"- {row[0]}: Stock={row[1]}, Price=${row[2]}")

    conn.close()
    
except Exception as e:
    print(f"Error inspecting DB: {e}")
