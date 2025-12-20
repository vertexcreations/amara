
from app import create_app
from models import db, Product, Category

app = create_app()

with app.app_context():
    print("--- Categories ---")
    categories = Category.query.all()
    for c in categories:
        print(f"ID: {c.id}, Name: {c.name}")
    
    print("\n--- Products (to_dict check) ---")
    products = Product.query.all()
    for p in products:
        d = p.to_dict()
        print(f"Product: {d['name']}, CategoryName in dict: {d.get('category_name')}, CategoryID: {d.get('category_id')}")
