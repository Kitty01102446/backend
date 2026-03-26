from flask import Blueprint, request, jsonify
from services.type_service_service import (
    get_all_type_services,
    get_type_service_by_id,
    insert_type_service,
    update_type_service,
    delete_type_service,
)

type_service_bp = Blueprint("type_service_bp", __name__)

# ============================================================
#   GET /type_service  +  POST /type_service
# ============================================================
@type_service_bp.route("/type_service", methods=["GET"])
def list_type_services():
    rows = get_all_type_services()
    return jsonify(rows), 200


@type_service_bp.route("/type_service", methods=["POST"])
def create_type_service():
    """เพิ่มประเภทบริการ"""

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid or empty JSON payload"}), 400

    required = ["name", "description"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    name = data["name"]
    description = data["description"]

    new_id = insert_type_service(
        name=name,
        description=description
    )

    return jsonify({
        "message": "Type Service created successfully",
        "type_service_id": new_id
    }), 201


# ============================================================
#   GET /type_service/<id>
#   PUT /type_service/<id>
#   DELETE /type_service/<id>
# ============================================================
@type_service_bp.route("/type_service/<int:tid>", methods=["GET"])
def get_type_service(tid: int):
    row = get_type_service_by_id(tid)
    if not row:
        return jsonify({"error": "Type Service not found"}), 404
    return jsonify(row), 200


@type_service_bp.route("/type_service/<int:tid>", methods=["PUT"])
def update_type_service_route(tid: int):
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    updated = update_type_service(tid, data)
    if not updated:
        return jsonify({"error": "Type Service not found"}), 404

    return jsonify({
        "message": "Type Service updated successfully",
        "type_service_id": tid
    }), 200


@type_service_bp.route("/type_service/<int:tid>", methods=["DELETE"])
def delete_type_service_route(tid: int):
    deleted = delete_type_service(tid)
    if not deleted:
        return jsonify({"error": "Type Service not found"}), 404

    return jsonify({"message": "Type Service deleted"}), 200



