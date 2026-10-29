"""
ผู้ดูแลระบบ (System Admin, role_id=4) -- ทุก route ในไฟล์นี้ต้อง login และผ่าน
require_admin() เท่านั้น ครอบคลุม: แดชบอร์ด, จัดการร้าน, จัดการผู้ใช้,
โปรไฟล์ลูกค้า, กิจกรรมทั้งหมด, สิทธิ์/บัญชี, รีวิว, การเงิน
"""

from flask import Blueprint, request, jsonify, g

from services.auth_service import token_required, require_admin
from services.admin_service import (
    get_dashboard_summary,
    get_stores_for_admin,
    approve_store,
    reject_store,
    set_store_admin_note,
    get_users_for_admin,
    ban_user,
    unban_user,
    get_user_profile_admin,
    update_user_profile_admin,
    get_platform_activity,
    list_roles,
    list_permissions,
    list_role_permissions,
    assign_permission,
    revoke_permission,
    get_platform_finance,
    list_reviews_for_admin,
    set_review_hidden,
)
from services.notification_service import create_notification
from services.store_service import get_store_owner_user_id
from services.booking_service import get_booking_with_services, get_user_bookings
from services.timeutil import bangkok_now

admin_bp = Blueprint("admin_bp", __name__)


# ============================================================
#   GET /admin/dashboard
# ============================================================
@admin_bp.route("/admin/dashboard", methods=["GET"])
@token_required
def dashboard_summary():
    guard = require_admin()
    if guard:
        return guard
    return jsonify(get_dashboard_summary()), 200


# ============================================================
#   STORES -- GET /admin/stores, approve/reject/note/notify
# ============================================================
@admin_bp.route("/admin/stores", methods=["GET"])
@token_required
def list_stores_admin():
    guard = require_admin()
    if guard:
        return guard
    status_store_id = request.args.get("status_store_id")
    rows = get_stores_for_admin(int(status_store_id) if status_store_id else None)
    return jsonify(rows), 200


@admin_bp.route("/admin/stores/<int:store_id>/approve", methods=["PUT"])
@token_required
def approve_store_route(store_id):
    guard = require_admin()
    if guard:
        return guard
    updated = approve_store(store_id, g.current_user["user_id"])
    if not updated:
        return jsonify({"error": "Store not found"}), 404
    return jsonify({"message": "Store approved"}), 200


@admin_bp.route("/admin/stores/<int:store_id>/reject", methods=["PUT"])
@token_required
def reject_store_route(store_id):
    guard = require_admin()
    if guard:
        return guard
    data = request.get_json(silent=True) or {}
    reason = data.get("reason")
    if not reason:
        return jsonify({"error": "Missing reason"}), 400
    updated = reject_store(store_id, g.current_user["user_id"], reason)
    if not updated:
        return jsonify({"error": "Store not found"}), 404
    return jsonify({"message": "Store rejected"}), 200


@admin_bp.route("/admin/stores/<int:store_id>/note", methods=["PUT"])
@token_required
def set_store_note_route(store_id):
    guard = require_admin()
    if guard:
        return guard
    data = request.get_json(silent=True) or {}
    updated = set_store_admin_note(store_id, data.get("note", ""))
    if not updated:
        return jsonify({"error": "Store not found"}), 404
    return jsonify({"message": "Note saved"}), 200


@admin_bp.route("/admin/stores/<int:store_id>/notify", methods=["POST"])
@token_required
def notify_store_route(store_id):
    guard = require_admin()
    if guard:
        return guard
    data = request.get_json(silent=True) or {}
    title = data.get("title")
    message = data.get("message")
    if not title or not message:
        return jsonify({"error": "Missing title or message"}), 400

    owner = get_store_owner_user_id(store_id)
    if not owner or not owner.get("user_id"):
        return jsonify({"error": "Store owner not found"}), 404

    create_notification(owner["user_id"], None, "ADMIN_NOTICE", title, message)
    return jsonify({"message": "Notification sent"}), 201


# ============================================================
#   USERS -- GET /admin/users, ban/unban, notify
# ============================================================
@admin_bp.route("/admin/users", methods=["GET"])
@token_required
def list_users_admin():
    guard = require_admin()
    if guard:
        return guard
    return jsonify(get_users_for_admin()), 200


@admin_bp.route("/admin/users/<int:user_id>/ban", methods=["PUT"])
@token_required
def ban_user_route(user_id):
    guard = require_admin()
    if guard:
        return guard
    data = request.get_json(silent=True) or {}
    reason = data.get("reason")
    if not reason:
        return jsonify({"error": "Missing reason"}), 400
    updated = ban_user(user_id, reason, g.current_user["user_id"])
    if not updated:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User banned"}), 200


@admin_bp.route("/admin/users/<int:user_id>/unban", methods=["PUT"])
@token_required
def unban_user_route(user_id):
    guard = require_admin()
    if guard:
        return guard
    updated = unban_user(user_id)
    if not updated:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User unbanned"}), 200


@admin_bp.route("/admin/users/<int:user_id>/notify", methods=["POST"])
@token_required
def notify_user_route(user_id):
    guard = require_admin()
    if guard:
        return guard
    data = request.get_json(silent=True) or {}
    title = data.get("title")
    message = data.get("message")
    if not title or not message:
        return jsonify({"error": "Missing title or message"}), 400

    create_notification(user_id, None, "ADMIN_NOTICE", title, message)
    return jsonify({"message": "Notification sent"}), 201


# ============================================================
#   CUSTOMER PROFILE -- GET/PUT /admin/users/<id>/profile, bookings
# ============================================================
@admin_bp.route("/admin/users/<int:user_id>/profile", methods=["GET"])
@token_required
def get_user_profile_route(user_id):
    guard = require_admin()
    if guard:
        return guard
    user = get_user_profile_admin(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user), 200


@admin_bp.route("/admin/users/<int:user_id>/profile", methods=["PUT"])
@token_required
def update_user_profile_route(user_id):
    guard = require_admin()
    if guard:
        return guard
    data = request.get_json(silent=True) or {}
    updated = update_user_profile_admin(user_id, data)
    if not updated:
        return jsonify({"error": "User not found or no fields to update"}), 404
    return jsonify({"message": "Profile updated"}), 200


@admin_bp.route("/admin/users/<int:user_id>/bookings", methods=["GET"])
@token_required
def get_user_bookings_route(user_id):
    guard = require_admin()
    if guard:
        return guard
    rows = get_user_bookings(user_id)
    return jsonify(rows), 200


# ============================================================
#   ACTIVITY FEED -- GET /admin/activity, /admin/activity/<booking_id>
# ============================================================
@admin_bp.route("/admin/activity", methods=["GET"])
@token_required
def platform_activity_route():
    guard = require_admin()
    if guard:
        return guard
    return jsonify(get_platform_activity()), 200


@admin_bp.route("/admin/activity/<int:booking_id>", methods=["GET"])
@token_required
def platform_activity_detail_route(booking_id):
    guard = require_admin()
    if guard:
        return guard
    rows = get_booking_with_services(booking_id)
    if not rows:
        return jsonify({"error": "Booking not found"}), 404
    return jsonify(rows), 200


# ============================================================
#   PERMISSIONS -- roles/permissions/role_permission
# ============================================================
@admin_bp.route("/admin/roles", methods=["GET"])
@token_required
def list_roles_route():
    guard = require_admin()
    if guard:
        return guard
    return jsonify(list_roles()), 200


@admin_bp.route("/admin/permissions", methods=["GET"])
@token_required
def list_permissions_route():
    guard = require_admin()
    if guard:
        return guard
    return jsonify(list_permissions()), 200


@admin_bp.route("/admin/role-permissions", methods=["GET"])
@token_required
def list_role_permissions_route():
    guard = require_admin()
    if guard:
        return guard
    return jsonify(list_role_permissions()), 200


@admin_bp.route("/admin/role-permissions", methods=["POST"])
@token_required
def assign_permission_route():
    guard = require_admin()
    if guard:
        return guard
    data = request.get_json(silent=True) or {}
    role_id = data.get("role_id")
    permission_id = data.get("permission_id")
    if not role_id or not permission_id:
        return jsonify({"error": "Missing role_id or permission_id"}), 400
    new_id = assign_permission(role_id, permission_id)
    if new_id is None:
        return jsonify({"error": "Already assigned"}), 409
    return jsonify({"message": "Permission assigned", "role_permission_id": new_id}), 201


@admin_bp.route("/admin/role-permissions/<int:role_permission_id>", methods=["DELETE"])
@token_required
def revoke_permission_route(role_permission_id):
    guard = require_admin()
    if guard:
        return guard
    deleted = revoke_permission(role_permission_id)
    if not deleted:
        return jsonify({"error": "Not found"}), 404
    return jsonify({"message": "Permission revoked"}), 200


# ============================================================
#   FINANCE -- GET /admin/finance?year=&month=
# ============================================================
@admin_bp.route("/admin/finance", methods=["GET"])
@token_required
def finance_route():
    guard = require_admin()
    if guard:
        return guard
    now = bangkok_now()
    year = int(request.args.get("year", now.year))
    month = int(request.args.get("month", now.month))
    return jsonify(get_platform_finance(year, month)), 200


# ============================================================
#   REVIEW MODERATION -- GET /admin/reviews, hide/unhide
# ============================================================
@admin_bp.route("/admin/reviews", methods=["GET"])
@token_required
def list_reviews_route():
    guard = require_admin()
    if guard:
        return guard
    only_hidden = request.args.get("only_hidden") == "1"
    return jsonify(list_reviews_for_admin(only_hidden)), 200


@admin_bp.route("/admin/reviews/<int:review_id>/hide", methods=["PUT"])
@token_required
def hide_review_route(review_id):
    guard = require_admin()
    if guard:
        return guard
    data = request.get_json(silent=True) or {}
    reason = data.get("reason")
    if not reason:
        return jsonify({"error": "Missing reason"}), 400
    updated = set_review_hidden(review_id, True, reason)
    if not updated:
        return jsonify({"error": "Review not found"}), 404
    return jsonify({"message": "Review hidden"}), 200


@admin_bp.route("/admin/reviews/<int:review_id>/unhide", methods=["PUT"])
@token_required
def unhide_review_route(review_id):
    guard = require_admin()
    if guard:
        return guard
    updated = set_review_hidden(review_id, False)
    if not updated:
        return jsonify({"error": "Review not found"}), 404
    return jsonify({"message": "Review unhidden"}), 200
