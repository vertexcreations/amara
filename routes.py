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
    if not data or not data.get('name'):
        return jsonify({'error': 'Category name is required'}), 400
    try:
        new_category = Category(name=data['name'].strip())
        db.session.add(new_category)
        db.session.commit()
        return jsonify(new_category.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

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

    # Check if products exist in this category before deleting
    products_count = Product.query.filter_by(category_id=id).count()
    if products_count > 0:
        return jsonify({'error': f'Cannot delete category with {products_count} product(s)'}), 400

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
    required_fields = ['name', 'sku', 'price', 'stock_quantity']
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': f'Required fields: {", ".join(required_fields)}'}), 400
    try:
        price = float(data['price'])
        cost_price = float(data.get('cost_price', 0.0))
        if price < 0 or cost_price < 0:
            return jsonify({'error': 'Price and cost_price must be >= 0'}), 400
        new_product = Product(
            name=data['name'].strip(),
            sku=data['sku'].strip(),
            price=price,
            cost_price=cost_price,
            stock_quantity=int(data['stock_quantity']),
            category_id=data.get('category_id')
        )
        db.session.add(new_product)
        db.session.commit()
        return jsonify(new_product.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': f'Invalid data type: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@main.route('/api/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.json
    try:
        if 'name' in data:
            product.name = data['name'].strip()
        if 'sku' in data:
            product.sku = data['sku'].strip()
        if 'price' in data:
            price = float(data['price'])
            if price < 0:
                return jsonify({'error': 'Price cannot be negative'}), 400
            product.price = price
        if 'cost_price' in data:
            cost_price = float(data['cost_price'])
            if cost_price < 0:
                return jsonify({'error': 'Cost price cannot be negative'}), 400
            product.cost_price = cost_price
        if 'stock_quantity' in data:
            product.stock_quantity = int(data['stock_quantity'])
        if 'category_id' in data:
            product.category_id = data['category_id']

        db.session.commit()
        return jsonify(product.to_dict())
    except ValueError as e:
        return jsonify({'error': f'Invalid data type: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@main.route('/api/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)

    # Check if product has associated sales
    sales_count = SaleItem.query.filter_by(product_id=id).count()
    if sales_count > 0:
        return jsonify({'error': f'Cannot delete product with {sales_count} sale(s) in history'}), 400

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
            if not item.get('id') or not item.get('quantity'):
                raise Exception("Missing item id or quantity")

            product = Product.query.get(item['id'])
            if not product:
                raise Exception(f"Product {item['id']} not found")

            quantity = int(item['quantity'])
            if quantity <= 0:
                raise Exception("Quantity must be > 0")

            if product.stock_quantity < quantity:
                raise Exception(f"Insufficient stock for {product.name}")

            product.stock_quantity -= quantity

            # Use custom price if provided, else product price
            price_to_use = float(item.get('custom_price', product.price))
            if price_to_use < 0:
                raise Exception("Price cannot be negative")
            
            sale_item = SaleItem(
                sale=sale,
                product=product,
                quantity=quantity,
                price_at_sale=price_to_use
            )
            db.session.add(sale_item)
            total_amount += price_to_use * quantity
            
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

@main.route('/api/sales/<int:id>', methods=['PUT'])
def update_sale(id):
    sale = Sale.query.get_or_404(id)
    data = request.json
    new_items = data.get('items', [])
    
    if not new_items:
        return jsonify({'error': 'No items provided'}), 400

    try:
        # 1. Revert Stock for existing items
        for item in sale.items:
            product = Product.query.get(item.product_id)
            if product:
                product.stock_quantity += item.quantity
        
        # 2. Delete existing items
        # Use simple delete loop as we need to remove them to recreate new state
        SaleItem.query.filter_by(sale_id=sale.id).delete()
        
        # 3. Create new items and deduct stock
        total_amount = 0
        for item_data in new_items:
            product = Product.query.get(item_data['product_id'])
            if not product:
                raise Exception(f"Product {item_data['product_id']} not found")
            
            # Check stock
            if product.stock_quantity < item_data['quantity']:
                raise Exception(f"Insufficient stock for {product.name}. Available: {product.stock_quantity}")
            
            product.stock_quantity -= item_data['quantity']
            
            # Create SaleItem
            # Allow price update if provided, otherwise check if price was sent or fallback
            price = float(item_data.get('price_at_sale', product.price))
            
            new_sale_item = SaleItem(
                sale=sale,
                product=product,
                quantity=item_data['quantity'],
                price_at_sale=price
            )
            db.session.add(new_sale_item)
            total_amount += price * item_data['quantity']
            
        # 4. Update Sale Totals
        sale.total_amount = total_amount
        
        # Optional: Update timestamp if provided, though usually history is preserved
        # if 'date' in data: ...
        
        db.session.commit()
        return jsonify(sale.to_dict())

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@main.route('/api/sales/<int:id>', methods=['DELETE'])
def delete_sale(id):
    sale = Sale.query.get_or_404(id)

    try:
        # Restore stock for all items in the sale
        for item in sale.items:
            product = Product.query.get(item.product_id)
            if product:
                product.stock_quantity += item.quantity

        # Delete sale (cascade='all, delete-orphan' in models handles SaleItem deletion)
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
