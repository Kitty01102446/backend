from flask import Blueprint, request, jsonify
from services.product_service import (
    get_all_products,
    get_product_by_id,
    insert_product,
    update_product,
    delete_product,
)

products_bp = Blueprint("products", __name__, url_prefix="/products")

# ============================================================
#   GET /products (list all) + POST /products (create)
# ============================================================
@products_bp.route("/products", methods=["GET"])
def list_products():
    rows = get_all_products()
    return jsonify(rows), 200

@products_bp.route("/products", methods=["POST"])
def create_product():
    """เพิ่มสินค้าใหม่ลงฐานข้อมูล"""

    # ดึง JSON จาก body
    data = request.get_json(silent=True)

    # ไม่มี / parse ไม่ได้ → 400
    if not data:
        return jsonify({"error": "Invalid or empty JSON payload"}), 400

    # ฟิลด์ที่ต้องมี
    required = ["name", "price"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # แปลงราคาให้เป็นตัวเลข
    try:
        price = float(data["price"])
    except (TypeError, ValueError):
        return jsonify({"error": "Field 'price' must be a number"}), 400

    name = data["name"]
    image = data.get("image", "")

    # เรียก service ไป insert
    new_id = insert_product(
        name=name,
        price=price,
        image=image,
    )

    return jsonify({
        "message": "Product created successfully",
        "product_id": new_id
    }), 201

# ============================================================
#                  GET /products/<id>
#                  PUT /products/<id>
#                DELETE /products/<id>
# ============================================================
@products_bp.route("/products/<int:pid>", methods=["GET"])
def get_product(pid: int):
    row = get_product_by_id(pid)
    if not row:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(row), 200


@products_bp.route("/products/<int:pid>", methods=["PUT"])
def update_product_route(pid: int):
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    updated = update_product(pid, data)

    if not updated:
        return jsonify({"error": "Product not found"}), 404

    return jsonify({
        "message": "Product updated successfully",
        "product_id": pid
    }), 200


@products_bp.route("/products/<int:pid>", methods=["DELETE"])
def delete_product_route(pid: int):
    deleted = delete_product(pid)

    if not deleted:
        return jsonify({"error": "Product not found"}), 404

    return jsonify({"message": "Product deleted"}), 200