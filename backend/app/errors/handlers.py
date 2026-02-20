from flask import jsonify
from sqlalchemy.exc import IntegrityError

def register_error_handlers(app):

    @app.errorhandler(LookupError)
    def handle_not_found(error):
        return jsonify({
            "success": False,
            "error": str(error)
        }), 404
    
    @app.errorhandler(ValueError)
    def handle_value_error(error):
        return jsonify({
            "success": False,
            "error": str(error)
        }), 400
    
    @app.errorhandler(IntegrityError)
    def handle_integrity_error(error):
        return jsonify({
            "success": False,
            "error": "Conflicto de integridad con la base de datos"
        }), 409
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        return jsonify({
            "success": False,
            "error": "Error interno del servidor"
        }), 500
    