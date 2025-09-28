from flask import Flask
from config import Config
from blueprints.home.routes import home_bp
from blueprints.user.routes import user_bp
from extensions import db, login_manager, migrate
from models import User

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(user_bp, url_prefix="/user")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)


