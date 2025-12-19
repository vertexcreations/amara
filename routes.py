from flask import Blueprint, render_template, request, jsonify
from models import db, Product, Sale, SaleItem, Category
from sqlalchemy import func
from datetime import datetime, date

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/inventory')
def inventory_page():
    return render_template('inventory.html')

@main.route('/pos')
def pos_page():
    return render_template('pos.html')

@main.route('/sales')
def sales_page():
    return render_template('sales.html')

@main.route('/categories')
def categories_page():
    return render_template('categories.html')

# API Endpoints

# Categories
@main.route('/api/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([c.to_dict() for c in categories])

@main.route('/api/categories', methods=['POST'])
def add_category():
    data = request.json
    new_category = Category(name=data['name'])
    db.session.add(new_category)
    db.session.commit()
    return jsonify(new_category.to_dict()), 201

@main.route('/api/categories/<int:id>', methods=['PUT'])
def update_category(id):
    category = Category.query.get_or_404(id)
    data = request.json
    category.name = data.get('name', category.name)
    db.session.commit()
    return jsonify(category.to_dict())

@main.route('/api/categories/<int:id>', methods=['DELETE'])
def delete_category(id):
    category = Category.query.get_or_404(id)
    # Optional: Check if products exist in this category before deleting
    db.session.delete(category)
    db.session.commit()
    return '', 204

# Products
@main.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products])

@main.route('/api/products', methods=['POST'])
def add_product():
    data = request.json
    new_product = Product(
        name=data['name'],
        sku=data['sku'],
        price=data['price'],
        cost_price=data.get('cost_price', 0.0),
        stock_quantity=data['stock_quantity'],
        category_id=data.get('category_id')
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify(new_product.to_dict()), 201

@main.route('/api/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.json
    product.name = data.get('name', product.name)
    product.sku = data.get('sku', product.sku)
    product.price = data.get('price', product.price)
    product.cost_price = data.get('cost_price', product.cost_price)
    product.stock_quantity = data.get('stock_quantity', product.stock_quantity)
    product.category_id = data.get('category_id', product.category_id)
    
    db.session.commit()
    return jsonify(product.to_dict())

@main.route('/api/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return '', 204

@main.route('/api/checkout', methods=['POST'])
def checkout():
    data = request.json
    cart_items = data.get('items', [])
    
    if not cart_items:
        return jsonify({'error': 'No items in cart'}), 400
        
    total_amount = 0
    
    # Handle custom date
    sale_date = datetime.now()
    if 'date' in data and data['date']:
        try:
            # Append current time to the selected date to avoid all sales being at 00:00:00
            # or just use the date part if that's preferred. 
            # Let's use the date provided + current time for ordering within the day, 
            # or just the date if we want it strict.
            # User asked: "Poner la opción de poner la fecha de venta y registrar en ese día"
            # Let's parse YYYY-MM-DD
            custom_date = datetime.strptime(data['date'], '%Y-%m-%d')
            # Keep current time for sorting, but on the custom day
            now = datetime.now()
            sale_date = custom_date.replace(hour=now.hour, minute=now.minute, second=now.second)
        except ValueError:
            pass # Fallback to now

    sale = Sale(total_amount=0, timestamp=sale_date) 
    db.session.add(sale)
    
    try:
        for item in cart_items:
            product = Product.query.get(item['id'])
            if not product:
                raise Exception(f"Product {item['id']} not found")
            
            if product.stock_quantity < item['quantity']:
                raise Exception(f"Insufficient stock for {product.name}")
                
            product.stock_quantity -= item['quantity']
            
            # Use custom price if provided, else product price
            price_to_use = float(item.get('custom_price', product.price))
            
            sale_item = SaleItem(
                sale=sale,
                product=product,
                quantity=item['quantity'],
                price_at_sale=price_to_use
            )
            db.session.add(sale_item)
            total_amount += price_to_use * item['quantity']
            
        sale.total_amount = total_amount
        db.session.commit()
        return jsonify(sale.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@main.route('/api/sales', methods=['GET'])
def get_sales():
    sales = Sale.query.order_by(Sale.timestamp.desc()).all()
    return jsonify([s.to_dict() for s in sales])

@main.route('/api/sales/<int:id>', methods=['DELETE'])
def delete_sale(id):
    sale = Sale.query.get_or_404(id)
    
    try:
        # Restore stock
        for item in sale.items:
            product = Product.query.get(item.product_id)
            if product:
                product.stock_quantity += item.quantity
        
        # Delete sale (cascade should handle items if configured, but let's be safe)
        # If cascade is not set in models, we might need to delete items first.
        # SQLAlchemy default relationship usually doesn't cascade delete unless specified.
        # Let's check models.py... items = db.relationship('SaleItem', backref='sale', lazy=True)
        # No cascade specified. We should delete items manually or rely on DB FK cascade (if set).
        # Safest is manual delete here or let SQLAlchemy handle it if we add cascade='all, delete-orphan' to model.
        # Since we didn't edit Sale model relationship, let's manually delete items.
        for item in sale.items:
            db.session.delete(item)
            
        db.session.delete(sale)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/api/dashboard-stats')
def dashboard_stats():
    # Use current date for filtering
    today = datetime.now().date()
    
    # Total sales today
    total_sales = db.session.query(func.sum(Sale.total_amount))\
        .filter(func.date(Sale.timestamp) == today).scalar() or 0.0
        
    # Items sold today
    items_sold = db.session.query(func.sum(SaleItem.quantity))\
        .join(Sale)\
        .filter(func.date(Sale.timestamp) == today).scalar() or 0
        
    # Low stock products (less than 5)
    low_stock = Product.query.filter(Product.stock_quantity < 5).count()
    
    return jsonify({
        'today_sales': total_sales,
        'items_sold': items_sold,
        'low_stock': low_stock
    })
