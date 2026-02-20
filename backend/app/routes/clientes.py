from flask import Blueprint, request
from app.services.cliente_service import ClienteService
from app.utils.responses import success_response

cliente_bp = Blueprint(
    "clientes", __name__,
    url_prefix= "/clientes"
)

@cliente_bp.route("", methods = ["POST"])
def crear_cliente():
    data = request.get_json()
    if not data:
        raise ValueError("JSON invalido o vacio")
        # return jsonify({
        #     "success": False,
        #     "error": "JSON invalido"
        # }), 400
    cliente = ClienteService.crear(data)
    return success_response(
        data = cliente.to_dict(),
        message = "Cliente creado exitosamente", 
        status_code = 201
        )
    # try:
    #     cliente = ClienteService.crear(data)
    #     return jsonify({
    #         "success": True,
    #         "data": {
    #             "id": cliente.id_cliente
    #         },
    #         "messaje": "Cliente creado exitosamente"
    #     }), 201
    # except ValueError as e:
    #     return jsonify({
    #         "success": False,
    #         "error": str(e)
    #     }), 409
    
@cliente_bp.route("", methods = ['GET'])
def listar_clientes():
    page = request.args.get("page", 1, type = int)
    per_page = request.args.get("per_page", 10, type = int)

    tipo = request.args.get("tipo")
    nombre = request.args.get("nombre")
    apellido = request.args.get("apellido")
    razon_social = request.args.get("razon_social")
    filtros = {}

    if tipo:
        filtros["tipo"] = tipo
    if nombre:
        filtros["nombre"] = nombre
    if apellido:
        filtros["apellido"] = apellido
    if razon_social:
        filtros["razon_social"] = razon_social

    paginacion = ClienteService.listar(page,per_page,filtros)

    return success_response(
        data = [c.to_dict() for c in paginacion.items],
        meta= {
            "page": paginacion.page,
            "per_page": paginacion.per_page,
            "total": paginacion.total,
            "pages": paginacion.pages
        }
    )
    
    # return jsonify({
    #     "success": True,
    #     "data": [c.to_dict() for c in paginacion.items],
    #     "meta": {
    #         "page": paginacion.page,
    #         "per_page": paginacion.per_page,
    #         "total": paginacion.total,
    #         "pages": paginacion.pages
    #     }
    # }), 200

@cliente_bp.route("/<int:id_cliente>", methods = ['PUT'])
def actualizar_cliente(id_cliente: int):
    data = request.get_json()
    if not data:
        raise ValueError("JSON invalido o vacio")
        # return jsonify({
        #     "success": False,
        #     "error": "JSON invalido o vacio"
        # }), 400
    cliente = ClienteService.actualizar(id_cliente, data)
    return success_response(
        data= cliente.to_dict(),
        message= "Cliente actualizado correctamente"
    )
    # return jsonify({
    #     "success": True,
    #     "data": cliente.to_dict(),
    #     "message": "Cliente agregado correctamente"
    # }), 200
    #try:
    #    cliente = ClienteService.actualizar(id_cliente,data)
    #    return jsonify({
    #        "success": True,
    #        "data": cliente.to_dict(),
    #        "message": "Cliente actualizado exitosamente"
    #    }), 200
    #except LookupError as e:
    #    return jsonify({
    #        "success": False,
    #        "error": str(e)
    #    }), 404
    #except ValueError as e:
    #    return jsonify({
    #        "success": False,
    #        "error": str(e)
    #    }), 409
    
@cliente_bp.route("/<int:id_cliente>", methods = ['DELETE'])
def eliminar_cliente(id_cliente: int):
    ClienteService.eliminar(id_cliente)
    return "", 204
    # try:
    #     ClienteService.eliminar(id_cliente)
    #     return "", 204
    # except LookupError as e:
    #     return jsonify({
    #         "success": False,
    #         "error": str(e)
    #     }), 404