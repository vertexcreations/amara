import sqlite3
import os

backup_files = [
    'import_backup/pos (1).db',
    'import_backup/pos.db (3).safety',
    'dist/pos.db',
    'instance/pos.db'
]

for db_path in backup_files:
    if not os.path.exists(db_path):
        print(f"\n[NO EXISTE] {db_path}")
        continue

    print(f"\n{'='*60}")
    print(f"[ANALIZANDO] {db_path}")
    print(f"{'='*60}")

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Get tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        tables = cursor.fetchall()

        if not tables:
            print("[VACIO] No hay tablas en esta BD")
            conn.close()
            continue

        print(f"\n[TABLAS] Total: {len(tables)}")
        total_records = 0

        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cursor.fetchone()[0]
            total_records += count
            status = "[OK]" if count > 0 else "[VACIO]"
            print(f"  {status} {table_name}: {count} registros")

        print(f"\n[TOTAL] {total_records} registros en toda la BD")

        conn.close()

    except Exception as e:
        print(f"[ERROR] {e}")

print("\n" + "="*60)
