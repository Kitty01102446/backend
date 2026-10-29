-- ============================================================
-- Phase 3 migration: ผูกบัญชีเข้าสู่ระบบของช่าง (employee) เข้ากับ `users`
--
-- ให้ช่างสามารถ login ผ่านระบบเดิม (users + role_id) ได้ โดยไม่ต้องสร้างตาราง
-- login แยกต่างหาก -- role_id=3 ("Staff") ที่มีอยู่แล้วใน `role` table คือ
-- role ของช่าง, role_id=2 ("Shop Owner") คือ Admin ของร้าน (ผูกกับ store.user_id
-- อยู่แล้ว)
--
-- Safe to run multiple times (idempotent). Never drops or truncates
-- anything. Run this AFTER nailshop_phase2b_leave_approval_migration.sql.
-- ============================================================

ALTER TABLE `employee`
  ADD COLUMN IF NOT EXISTS `user_id` INT(11) NULL DEFAULT NULL
    COMMENT 'อ้างอิง users.user_id เมื่อช่างคนนี้มีบัญชีเข้าสู่ระบบ; NULL = ยังไม่มีบัญชี'
    AFTER `store_id`;

ALTER TABLE `employee`
  ADD KEY IF NOT EXISTS `idx_employee_user_id` (`user_id`);
