from flask import Flask, render_template
from models import db
import os

import sys

def get_data_dir():
    """Returns a stable data directory regardless of where the .exe is located."""
    if getattr(sys, 'frozen', False):
        # Use %APPDATA%\MiTiendaPoS so data persists even if .exe is moved
        base = os.environ.get('APPDATA', os.path.expanduser('~'))
        data_dir = os.path.join(base, 'MiTiendaPoS')
    else:
        data_dir = os.path.join(os.getcwd(), 'instance')
    os.makedirs(data_dir, exist_ok=True)
    return data_dir

def create_app():
    if getattr(sys, 'frozen', False):
        template_folder = os.path.join(sys._MEIPASS, 'templates')
        static_folder = os.path.join(sys._MEIPASS, 'static')
        app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
        db_path = os.path.join(get_data_dir(), 'pos.db')
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    else:
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pos.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        
    from routes import main
    from backup_routes import backup_bp
    
    app.register_blueprint(main)
    app.register_blueprint(backup_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=False)
