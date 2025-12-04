import json
from models import Category, Product, Sale

def test_get_categories_empty(client):
    response = client.get('/api/categories')
    assert response.status_code == 200
    assert response.json == []

def test_create_category(client):
    response = client.post('/api/categories', json={'name': 'New Category'})
    assert response.status_code == 201
    assert response.json['name'] == 'New Category'
    
    # Verify persistence
    response = client.get('/api/categories')
    assert len(response.json) == 1

def test_create_product(client, sample_category):
    product_data = {
        'name': 'T-Shirt',
        'sku': 'TSH-001',
        'price': 15.0,
        'stock_quantity': 100,
        'category_id': sample_category.id
    }
    response = client.post('/api/products', json=product_data)
    assert response.status_code == 201
    assert response.json['name'] == 'T-Shirt'

def test_checkout_success(client, sample_category):
    # Setup product
    product_data = {
        'name': 'Jeans',
        'sku': 'JNS-001',
        'price': 50.0,
        'stock_quantity': 10,
        'category_id': sample_category.id
    }
    client.post('/api/products', json=product_data)
    product_id = Product.query.filter_by(sku='JNS-001').first().id
    
    # Perform checkout
    checkout_data = {
        'items': [
            {'id': product_id, 'quantity': 2}
        ]
    }
    response = client.post('/api/checkout', json=checkout_data)
    
    assert response.status_code == 201
    assert response.json['total_amount'] == 100.0
    
    # Verify stock reduction
    updated_product = Product.query.get(product_id)
    assert updated_product.stock_quantity == 8

def test_checkout_insufficient_stock(client, sample_category):
    # Setup product
    product_data = {
        'name': 'Hat',
        'sku': 'HAT-001',
        'price': 25.0,
        'stock_quantity': 1,
        'category_id': sample_category.id
    }
    client.post('/api/products', json=product_data)
    product_id = Product.query.filter_by(sku='HAT-001').first().id
    
    # Try to buy more than stock
    checkout_data = {
        'items': [
            {'id': product_id, 'quantity': 2}
        ]
    }
    response = client.post('/api/checkout', json=checkout_data)
    
    assert response.status_code == 400
    assert 'Insufficient stock' in response.json['error']

def test_update_product(client, sample_category):
    # Create a product first
    product_data = {
        'name': 'Old Name',
        'sku': 'OLD-001',
        'price': 10.0,
        'stock_quantity': 5,
        'category_id': sample_category.id
    }
    client.post('/api/products', json=product_data)
    product_id = Product.query.filter_by(sku='OLD-001').first().id

    # Update the product
    update_data = {
        'name': 'New Name',
        'price': 12.0
    }
    response = client.put(f'/api/products/{product_id}', json=update_data)
    
    assert response.status_code == 200
    assert response.json['name'] == 'New Name'
    assert response.json['price'] == 12.0
    
    # Verify persistence
    updated_product = Product.query.get(product_id)
    assert updated_product.name == 'New Name'
    assert updated_product.price == 12.0

def test_delete_product(client, sample_category):
    # Create a product first
    product_data = {
        'name': 'To Delete',
        'sku': 'DEL-001',
        'price': 10.0,
        'stock_quantity': 5,
        'category_id': sample_category.id
    }
    client.post('/api/products', json=product_data)
    product_id = Product.query.filter_by(sku='DEL-001').first().id

    # Delete the product
    response = client.delete(f'/api/products/{product_id}')
    assert response.status_code == 204
    
    # Verify deletion
    deleted_product = Product.query.get(product_id)
    assert deleted_product is None

def test_checkout_product_not_found(client):
    checkout_data = {
        'items': [
            {'id': 9999, 'quantity': 1}
        ]
    }
    response = client.post('/api/checkout', json=checkout_data)
    
    assert response.status_code == 400
    assert 'not found' in response.json['error']

def test_dashboard_stats(client, sample_category):
    # Create a sale
    product_data = {
        'name': 'Stats Item',
        'sku': 'STS-001',
        'price': 100.0,
        'stock_quantity': 10,
        'category_id': sample_category.id
    }
    client.post('/api/products', json=product_data)
    product_id = Product.query.filter_by(sku='STS-001').first().id
    
    checkout_data = {
        'items': [
            {'id': product_id, 'quantity': 2}
        ]
    }
    client.post('/api/checkout', json=checkout_data)
    
    # Get stats
    response = client.get('/api/dashboard-stats')
    assert response.status_code == 200
    stats = response.json
    
    assert stats['today_sales'] == 200.0
    assert stats['items_sold'] == 2
    assert stats['low_stock'] == 0 # Stock is 8
    
    # Create low stock item
    product_data_low = {
        'name': 'Low Stock Item',
        'sku': 'LOW-001',
        'price': 50.0,
        'stock_quantity': 3,
        'category_id': sample_category.id
    }
    client.post('/api/products', json=product_data_low)
    
    response = client.get('/api/dashboard-stats')
    assert response.json['low_stock'] == 1
