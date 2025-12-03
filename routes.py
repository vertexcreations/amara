from flask import Blueprint, render_template, request, jsonify
from models import db, Product, Sale, SaleItem, Category

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
        size=data.get('size'),
        color=data.get('color'),
        price=data['price'],
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
    product.size = data.get('size', product.size)
    product.color = data.get('color', product.color)
    product.price = data.get('price', product.price)
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
    sale = Sale(total_amount=0) # Will update total later
    db.session.add(sale)
    
    try:
        for item in cart_items:
            product = Product.query.get(item['id'])
            if not product:
                raise Exception(f"Product {item['id']} not found")
            
            if product.stock_quantity < item['quantity']:
                raise Exception(f"Insufficient stock for {product.name}")
                
            product.stock_quantity -= item['quantity']
            
            sale_item = SaleItem(
                sale=sale,
                product=product,
                quantity=item['quantity'],
                price_at_sale=product.price
            )
            db.session.add(sale_item)
            total_amount += product.price * item['quantity']
            
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
