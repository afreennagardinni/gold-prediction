import os
from flask import Flask
from flask_migrate import Migrate
from config import Config
from app.extensions import db, login_manager
from app.models import load_model

migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # ✅ user loader
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))

    # Load ML model
    print("Loading ML model...")
    model, scaler, selected_features = load_model()
    app.model = model
    app.scaler = scaler
    app.selected_features = selected_features

    login_manager.login_view = 'main.login'
    login_manager.login_message = 'Please log in to access this page.'

    from app import routes
    app.register_blueprint(routes.bp)

    with app.app_context():
        db.create_all()

    @app.route('/health')
    def health():
        return {
            'status': 'healthy',
            'model_features': app.selected_features
        }

    return app