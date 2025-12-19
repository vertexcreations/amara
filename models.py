from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'product_count': len(self.products)
        }

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    cost_price = db.Column(db.Float, default=0.0)
    stock_quantity = db.Column(db.Integer, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    
    category = db.relationship('Category', backref='products')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'sku': self.sku,
            'price': self.price,
            'cost_price': self.cost_price,
            'stock_quantity': self.stock_quantity,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else None
        }

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    total_amount = db.Column(db.Float, nullable=False)
    items = db.relationship('SaleItem', backref='sale', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'total_amount': self.total_amount,
            'items': [item.to_dict() for item in self.items]
        }

class SaleItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('sale.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_at_sale = db.Column(db.Float, nullable=False)
    
    product = db.relationship('Product')

    def to_dict(self):
        return {
            'product_name': self.product.name,
            'quantity': self.quantity,
            'price_at_sale': self.price_at_sale,
            'subtotal': self.quantity * self.price_at_sale
        }
