from models import Category, Product, Sale, SaleItem, db

def test_category_creation(app):
    category = Category(name="Electronics")
    db.session.add(category)
    db.session.commit()
    
    saved_category = Category.query.first()
    assert saved_category.name == "Electronics"
    assert saved_category.id is not None

def test_product_creation(app, sample_category):
    product = Product(
        name="Laptop",
        sku="LPT-001",
        price=999.99,
        stock_quantity=10,
        category_id=sample_category.id
    )
    db.session.add(product)
    db.session.commit()
    
    saved_product = Product.query.first()
    assert saved_product.name == "Laptop"
    assert saved_product.category.name == "Test Category"
    assert saved_product.stock_quantity == 10

def test_sale_creation(app, sample_category):
    # Create product
    product = Product(
        name="Mouse",
        sku="MSE-001",
        price=20.0,
        stock_quantity=50,
        category_id=sample_category.id
    )
    db.session.add(product)
    db.session.commit()
    
    # Create sale
    sale = Sale(total_amount=40.0)
    db.session.add(sale)
    
    sale_item = SaleItem(
        sale=sale,
        product=product,
        quantity=2,
        price_at_sale=20.0
    )
    db.session.add(sale_item)
    db.session.commit()
    
    saved_sale = Sale.query.first()
    assert saved_sale.total_amount == 40.0
    assert len(saved_sale.items) == 1
    assert saved_sale.items[0].product.name == "Mouse"
