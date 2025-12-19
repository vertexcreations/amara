from app import create_app
from models import db, Product, Category, Sale, SaleItem
import random

app = create_app()

def seed():
    with app.app_context():
        print("Limpiando base de datos...")
        try:
            # Order matters due to FKs
            db.session.query(SaleItem).delete()
            db.session.query(Sale).delete()
            db.session.query(Product).delete()
            db.session.query(Category).delete()
            db.session.commit()
        except Exception as e:
            print(f"Error limpiando datos (puede ser la primera ejecución): {e}")
            db.create_all()

        print("Creando categorías...")
        categories = [
            "Jeans", "Camisas", "Vestidos", "Poleras", "Accesorios", "Chaquetas", "Faldas"
        ]
        
        cat_objects = {}
        for name in categories:
            cat = Category(name=name)
            db.session.add(cat)
            cat_objects[name] = cat
        
        db.session.commit()

        print("Creando productos...")
        products_data = [
            # Jeans
            ("Jean Skinny Azul", "J001", 180.00, 100.00, "Jeans"),
            ("Jean Mom Fit Negro", "J002", 200.00, 110.00, "Jeans"),
            ("Jean Roto Celeste", "J003", 190.00, 105.00, "Jeans"),
            ("Jean Cargo Beige", "J004", 220.00, 120.00, "Jeans"),
            
            # Camisas
            ("Camisa Blanca Oxford", "C001", 150.00, 80.00, "Camisas"),
            ("Blusa Seda Estampada", "C002", 120.00, 60.00, "Camisas"),
            ("Camisa Leñadora Roja", "C003", 140.00, 75.00, "Camisas"),
            
            # Vestidos
            ("Vestido Verano Floral", "V001", 250.00, 130.00, "Vestidos"),
            ("Vestido Noche Negro", "V002", 350.00, 180.00, "Vestidos"),
            ("Vestido Casual Rayas", "V003", 180.00, 90.00, "Vestidos"),
            
            # Poleras
            ("Polera Básica Blanca", "P001", 80.00, 40.00, "Poleras"),
            ("Polera Estampada Rock", "P002", 100.00, 50.00, "Poleras"),
            ("Polera Oversize Negra", "P003", 110.00, 55.00, "Poleras"),
            
            # Accesorios
            ("Cinturón Cuero Café", "A001", 90.00, 45.00, "Accesorios"),
            ("Bufanda Lana Gris", "A002", 70.00, 30.00, "Accesorios"),
            ("Gorra Urbana Negra", "A003", 85.00, 40.00, "Accesorios"),
            
             # Chaquetas
            ("Chaqueta Jean Clásica", "CH001", 280.00, 150.00, "Chaquetas"),
            ("Chaqueta Cuero Biker", "CH002", 450.00, 250.00, "Chaquetas"),
            
            # Faldas
            ("Falda Plisada Negra", "F001", 160.00, 80.00, "Faldas"),
            ("Minifalda Jean", "F002", 140.00, 70.00, "Faldas"),
        ]

        for name, sku, price, cost, cat_name in products_data:
            p = Product(
                name=name,
                sku=sku,
                price=price,
                cost_price=cost,
                stock_quantity=random.randint(0, 50),
                category=cat_objects[cat_name]
            )
            db.session.add(p)
        
        db.session.commit()
        print("¡Datos de prueba creados exitosamente!")

if __name__ == '__main__':
    seed()
