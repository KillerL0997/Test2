from flask import Flask
from app.extensions import db, migrate
from app.routes.clientes import cliente_bp
from app.routes.usuarios import usuario_bp
from app.errors.handlers import register_error_handlers

def create_app():
    app = Flask(__name__)

    # Cargar configuración
    app.config.from_object("config.Config")

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(cliente_bp)
    app.register_blueprint(usuario_bp)
    register_error_handlers(app)

    from app.models import rol, usuario, cliente

    # Blueprint de prueba (temporal)
    @app.route("/health")
    def health():
        return {"status": "ok"}

    return app