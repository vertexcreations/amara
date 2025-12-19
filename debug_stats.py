from app import create_app
from models import db, Sale
from datetime import datetime, timedelta, date, time
from sqlalchemy import func

app = create_app()

with app.app_context():
    print(f"DB URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    now = datetime.now()
    print(f"Current System Time: {now}")
    today = now.date()
    
    # Ensure there is at least one sale for 'today' to test
    # We use range check to see if we have one, as we suspect func.date might be failing
    start_of_day = datetime.combine(today, time.min)
    end_of_day = start_of_day + timedelta(days=1)
    
    sales_today_count = Sale.query.filter(Sale.timestamp >= start_of_day, Sale.timestamp < end_of_day).count()
    
    if sales_today_count == 0:
        print("No sales found for today (by range). Creating a dummy sale for testing.")
        dummy_sale = Sale(total_amount=123.45, timestamp=now)
        db.session.add(dummy_sale)
        db.session.commit()
        print(f"Created Sale ID: {dummy_sale.id} at {dummy_sale.timestamp}")
    
    # Test 1: Original Logic (strings comparison via func.date)
    # Note: Flask-SQLAlchemy/SQLite might behave differently depending on how date is stored.
    original_sales = db.session.query(func.sum(Sale.total_amount))\
        .filter(func.date(Sale.timestamp) == today).scalar() or 0.0
        
    print(f"Original Logic (func.date == today): {original_sales}")
    
    # Test 2: Proposed Logic (Range comparison)
    proposed_sales = db.session.query(func.sum(Sale.total_amount))\
        .filter(Sale.timestamp >= start_of_day)\
        .filter(Sale.timestamp < end_of_day).scalar() or 0.0
        
    print(f"Proposed Logic (Range >= start < end): {proposed_sales}")
    
    # Inspect raw timestamps
    print("\nRecent Sales Timestamps:")
    for s in Sale.query.order_by(Sale.timestamp.desc()).limit(5):
        print(f"ID: {s.id}, TS: {s.timestamp} (Raw type: {type(s.timestamp)})")
        # Check what func.date returns for this
        date_val = db.session.query(func.date(s.timestamp)).scalar()
        print(f"  -> func.date(TS): {date_val} (Type: {type(date_val)})")
