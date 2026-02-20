from flask import jsonify

def success_response(data = None, message = None, status_code = 200, meta = None):
    response = {"success": True}
    if data is not None:
        response["data"] = data
    if message:
        response["message"] = message
    if meta:
        response["meta"] = meta
    return jsonify(response), status_code