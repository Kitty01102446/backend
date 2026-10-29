-- ============================================================
-- Phase 2b migration: เพิ่ม workflow อนุมัติการลา (PENDING -> ACTIVE/REJECTED)
--
-- ใช้เฉพาะ absence_type = 'LEAVE' เท่านั้น -- 'ABSENT' (ขาดงานกะทันหัน) ยังคง
-- มีผลทันทีเหมือนเดิม (ไม่ต้องมีใครอนุมัติ เพราะเป็นการรายงานข้อเท็จจริง ไม่ใช่
-- การขอล่วงหน้า)
--
-- Safe to run multiple times. ไม่กระทบแถวเดิมที่เป็น ACTIVE/CANCELLED อยู่แล้ว
-- Run this AFTER nailshop_phase2_migration.sql.
-- ============================================================

ALTER TABLE `employee_absence`
  MODIFY COLUMN `status` ENUM('PENDING','ACTIVE','REJECTED','CANCELLED') NOT NULL DEFAULT 'ACTIVE';
