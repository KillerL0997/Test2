from flask import Blueprint

usuario_bp = Blueprint(
    "usuarios", __name__,
    url_prefix= "/usuarios"
)