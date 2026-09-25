"""
Kisan Web Project - Application Factory & Server Entry Point
Modular Flask application combining Three.js 3D WebGL UI with PostgreSQL backend services.
"""
import os
from flask import Flask, render_template, jsonify
from config import config_by_name
from extensions import db, migrate, jwt

def create_app(config_name=None):
    """Factory to create and configure the Flask application."""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config_by_name.get(config_name, config_by_name['default']))

    # Ensure required directories exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Register blueprints
    from routes.auth_routes import auth_bp
    from routes.crop_routes import crop_bp
    from routes.weather_routes import weather_bp
    from routes.ai_routes import ai_bp
    from routes.assistant_routes import assistant_bp
    from routes.community_routes import community_bp
    from routes.tools_routes import tools_bp
    from routes.schemes_routes import schemes_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(crop_bp)
    app.register_blueprint(weather_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(assistant_bp)
    app.register_blueprint(community_bp)
    app.register_blueprint(tools_bp)
    app.register_blueprint(schemes_bp)

    # Main Web Frontend Route
    @app.route('/')
    def index():
        """Render the master Kisan 3D Web Application interface."""
        return render_template('index.html')

    # API Healthcheck
    @app.route('/health')
    def health():
        return jsonify({
            'status': 'healthy',
            'service': 'Kisan Web Project API',
            'version': '2.0.0',
            'database': 'Connected'
        }), 200

    # Custom CLI commands for database management
    @app.cli.command('init-db')
    def init_db_command():
        """Create database tables."""
        db.create_all()
        print("Database tables created.")

    @app.cli.command('seed-db')
    def seed_db_command():
        """Seed sample agricultural data."""
        from seed_data import seed_database
        seed_database()

    return app


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
        from seed_data import seed_database
        seed_database()

    port = int(os.environ.get('PORT', 5000))
    print(f"\n=======================================================")
    print(f"[*] Kisan Web Project running on http://127.0.0.1:{port}")
    print(f"[*] 3D WebGL Interface & Flask REST APIs Active")
    print(f"=======================================================\n")
    app.run(host="127.0.0.1", port=port, debug=False)
