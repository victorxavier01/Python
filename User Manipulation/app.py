from flask import Flask
from config import Config
from blueprints.home.routes import home_bp
from blueprints.user.routes import user_bp
from blueprints.posts.routes import post_bp
from extensions import db, login_manager
from logger import Logger
from models import User

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Logger
    Logger(app.logger)

    # DB
    db.init_app(app)
    with app.app_context():
        db.create_all()
        
    # Login Manager
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(user_bp, url_prefix="/user")
    app.register_blueprint(post_bp)

    app.logger.info("App iniciado!")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
