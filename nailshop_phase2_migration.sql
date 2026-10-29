-- ============================================================
-- Phase 2 migration: เงินเดือน (base salary + commission) + payroll record
--
-- Safe to run multiple times (idempotent, uses native IF [NOT] EXISTS
-- clauses -- see nailshop_phase1_migration.sql for why stored procedures
-- were avoided). Never drops or truncates anything.
-- Run this AFTER nailshop_phase1_migration.sql.
-- ============================================================

-- ------------------------------------------------------------
-- 1. อัตราค่าจ้างต่อพนักงาน (เงินเดือนฐาน + % คอมมิชชั่น, ไม่บังคับ)
-- ------------------------------------------------------------
ALTER TABLE `employee`
  ADD COLUMN IF NOT EXISTS `base_salary` DECIMAL(10,2) NULL DEFAULT NULL
    COMMENT 'เงินเดือนฐานต่อเดือน; NULL = ไม่มีเงินเดือนฐาน' AFTER `current_status_id`;

ALTER TABLE `employee`
  ADD COLUMN IF NOT EXISTS `commission_rate` DECIMAL(5,2) NULL DEFAULT NULL
    COMMENT 'ร้อยละค่าคอมมิชชั่นจากยอดบริการที่ทำสำเร็จ (0-100); NULL = ไม่มีคอมมิชชั่น' AFTER `base_salary`;

-- ------------------------------------------------------------
-- 2. payroll_record -- ผลคำนวณเงินเดือนต่อพนักงานต่อเดือน (DRAFT/CONFIRMED)
--
-- ระบบคำนวณ "ร่าง" ให้อัตโนมัติจากข้อมูลลา/ขาดงาน/คอมมิชชั่น แต่ "ห้ามหักเงิน
-- อัตโนมัติ" -- Admin ต้องตรวจสอบและกดยืนยัน (แก้ยอดได้ก่อนยืนยัน) เท่านั้นจึง
-- จะถือเป็นค่าจริงที่ใช้จ่ายเงินเดือน
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `payroll_record` (
  `payroll_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `employee_id` INT NOT NULL,
  `store_id` INT NOT NULL,
  `period_year` INT NOT NULL,
  `period_month` INT NOT NULL COMMENT '1-12',
  `work_days` DECIMAL(4,1) NOT NULL DEFAULT 0,
  `leave_days` DECIMAL(4,1) NOT NULL DEFAULT 0 COMMENT 'ลาครึ่งวันนับ 0.5',
  `absent_days` INT NOT NULL DEFAULT 0,
  `base_salary` DECIMAL(10,2) NOT NULL DEFAULT 0,
  `commission_amount` DECIMAL(10,2) NOT NULL DEFAULT 0,
  `total_amount` DECIMAL(10,2) NOT NULL DEFAULT 0
    COMMENT 'ยอดที่ Admin ตรวจสอบ/แก้ไขก่อนยืนยัน; ร่างเริ่มต้น = base_salary + commission_amount',
  `status` ENUM('DRAFT','CONFIRMED') NOT NULL DEFAULT 'DRAFT',
  `note` VARCHAR(255) DEFAULT NULL,
  `confirmed_by` VARCHAR(100) DEFAULT NULL,
  `confirmed_at` DATETIME DEFAULT NULL,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY `uq_employee_period` (`employee_id`, `period_year`, `period_month`),
  KEY `idx_payroll_store_period` (`store_id`, `period_year`, `period_month`),
  CONSTRAINT `fk_payroll_employee` FOREIGN KEY (`employee_id`) REFERENCES `employee` (`employee_id`),
  CONSTRAINT `fk_payroll_store` FOREIGN KEY (`store_id`) REFERENCES `store` (`store_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
