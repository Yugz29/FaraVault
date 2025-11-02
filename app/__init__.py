from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'changeme-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vault.db'
    db.init_app(app)

    from .api.v1 import api_v1_bp
    app.register_blueprint(api_v1_bp, url_prefix='/api/v1')

    return app