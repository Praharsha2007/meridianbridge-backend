from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS

# Extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()


def create_app(config_class="app.config.DevelopmentConfig"):
    app = Flask(__name__)

    # Load config
    app.config.from_object(config_class)

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    from flask_cors import CORS

    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
    # ✅ Import ONCE
    from app.routes.auth_routes import auth_bp
    from app.routes.brand_routes import brand_bp
    from app.routes.campaign_routes import campaign_bp
    from app.routes.influencer_routes import influencer_bp

    # ✅ Register ONCE
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(brand_bp, url_prefix="/brand")
    app.register_blueprint(campaign_bp, url_prefix="/campaigns")
    app.register_blueprint(influencer_bp, url_prefix="/influencer")

    # Health check
    @app.route("/")
    def home():
        return {"message": "Backend is running"}

    # Security headers
    @app.after_request
    def add_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        return response

    return app