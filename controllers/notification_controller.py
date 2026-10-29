from flask import Blueprint, jsonify, g
from services.notification_service import (
    get_notifications,
    get_unread_count,
    mark_read,
    mark_all_read,
)
from services.auth_service import token_required

notification_bp = Blueprint("notification_bp", __name__)


# ============================================================
#   GET /notifications  (แจ้งเตือนของผู้ใช้ปัจจุบัน)
# ============================================================
@notification_bp.route("/notifications", methods=["GET"])
@token_required
def list_notifications():
    rows = get_notifications(g.current_user["user_id"])
    return jsonify(rows), 200


# ============================================================
#   GET /notifications/unread-count
# ============================================================
@notification_bp.route("/notifications/unread-count", methods=["GET"])
@token_required
def unread_count_route():
    count = get_unread_count(g.current_user["user_id"])
    return jsonify({"unread_count": count}), 200


# ============================================================
#   PUT /notifications/<id>/read
# ============================================================
@notification_bp.route("/notifications/<int:notification_id>/read", methods=["PUT"])
@token_required
def mark_notification_read_route(notification_id):
    updated = mark_read(notification_id, g.current_user["user_id"])
    if not updated:
        return jsonify({"error": "Notification not found"}), 404
    return jsonify({"message": "Notification marked as read"}), 200


# ============================================================
#   PUT /notifications/read-all
# ============================================================
@notification_bp.route("/notifications/read-all", methods=["PUT"])
@token_required
def mark_all_notifications_read_route():
    updated_count = mark_all_read(g.current_user["user_id"])
    return jsonify({"message": "Notifications marked as read", "updated_count": updated_count}), 200
