from flask import Blueprint, request, jsonify
from app.services.cliente_service import ClienteService

cliente_bp = Blueprint(
    "clientes", __name__,
    url_prefix= "/clientes"
)

@cliente_bp.route("", methods = ["POST"])
def crear_cliente():
    data = request.get_json()
    if not data:
        return jsonify({
            "success": False,
            "error": "JSON invalido"
        }), 400
    
    try:
        cliente = ClienteService.crear(data)
        return jsonify({
            "success": True,
            "data": {
                "id": cliente.id_cliente
            },
            "messaje": "Cliente creado exitosamente"
        }), 201
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 409
    
@cliente_bp.route("", methods = ['GET'])
def listar_clientes():
    pag_ini = request.args.get("page", 1, type = int)
    pag_fin = request.args.get("per_page", 10, type = int)

    paginacion = ClienteService.listar_cliente(pag_ini,pag_fin)
    
    return jsonify({
        "success": True,
        "data": [c.to_dict for c in paginacion.items],
        "meta": {
            "page": paginacion.page,
            "per_page": paginacion.per_page,
            "total": paginacion.total,
            "pages": paginacion.pages
        }
    }), 200