-- ============================================================
-- Phase 1 migration: employee status / skill / work-hours / leave&absence
--                     / staff-change history / booking concurrency lock
--
-- Safe to run multiple times (idempotent). Never drops or truncates
-- anything. Does not touch the legacy singular `booking` table.
-- Run this AFTER nailshop.sql has already been imported.
-- ============================================================

-- ------------------------------------------------------------
-- 1. status_employee (mirrors status_booking / status_service / status_store)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `status_employee` (
  `status_employee_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `status_employee_name` VARCHAR(50) NOT NULL,
  `description` VARCHAR(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT IGNORE INTO `status_employee` (`status_employee_id`, `status_employee_name`, `description`) VALUES
  (1, 'available', 'พร้อมให้บริการ'),
  (2, 'working',   'กำลังให้บริการ'),
  (3, 'break',     'พัก'),
  (4, 'leave',     'ลา'),
  (5, 'absent',    'ไม่มาทำงาน'),
  (6, 'off',       'วันหยุด');

-- ------------------------------------------------------------
-- 2. employee_service_skill (per-service skill mapping)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `employee_service_skill` (
  `employee_service_skill_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `employee_id` INT NOT NULL,
  `service_id` INT NOT NULL,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY `uq_employee_service` (`employee_id`, `service_id`),
  KEY `idx_ess_employee` (`employee_id`),
  KEY `idx_ess_service` (`service_id`),
  CONSTRAINT `fk_ess_employee` FOREIGN KEY (`employee_id`) REFERENCES `employee` (`employee_id`),
  CONSTRAINT `fk_ess_service` FOREIGN KEY (`service_id`) REFERENCES `service` (`service_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Backfill: every existing, non-deleted employee is granted skill for every
-- service already offered at their own store, so no currently-bookable
-- employee becomes unbookable the moment this ships.
INSERT IGNORE INTO `employee_service_skill` (`employee_id`, `service_id`)
SELECT e.employee_id, s.service_id
FROM `employee` e
JOIN `service` s ON s.store_id = e.store_id
WHERE e.deleted_at IS NULL;

-- ------------------------------------------------------------
-- 3. employee_work_hours (recurring weekly pattern; NO rows = unrestricted)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `employee_work_hours` (
  `work_hours_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `employee_id` INT NOT NULL,
  `day_of_week` TINYINT NOT NULL COMMENT '1=Monday .. 7=Sunday, matches Python date.isoweekday()',
  `start_time` TIME NOT NULL,
  `end_time` TIME NOT NULL,
  `is_working` TINYINT(1) NOT NULL DEFAULT 1,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY `uq_employee_day` (`employee_id`, `day_of_week`),
  KEY `idx_ewh_employee` (`employee_id`),
  CONSTRAINT `fk_ewh_employee` FOREIGN KEY (`employee_id`) REFERENCES `employee` (`employee_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
-- No seed rows for existing employees: absence of rows means "unrestricted", by design.

-- ------------------------------------------------------------
-- 4. employee_absence (unified LEAVE + ABSENT, date-scoped)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `employee_absence` (
  `absence_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `employee_id` INT NOT NULL,
  `absence_type` ENUM('LEAVE','ABSENT') NOT NULL,
  `leave_scope` ENUM('FULL_DAY','HALF_DAY') DEFAULT NULL
      COMMENT 'meaningful only when absence_type=LEAVE; NULL for ABSENT (rest of day) and LEAVE FULL_DAY',
  `absence_date` DATE NOT NULL,
  `start_time` TIME DEFAULT NULL COMMENT 'set only when leave_scope=HALF_DAY',
  `end_time` TIME DEFAULT NULL COMMENT 'set only when leave_scope=HALF_DAY',
  `reason` VARCHAR(255) DEFAULT NULL,
  `status` ENUM('ACTIVE','CANCELLED') NOT NULL DEFAULT 'ACTIVE',
  `requested_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `created_by` VARCHAR(100) DEFAULT NULL COMMENT 'free-text identifier; no auth system exists yet',
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  KEY `idx_ea_employee_date` (`employee_id`, `absence_date`, `status`),
  CONSTRAINT `fk_ea_employee` FOREIGN KEY (`employee_id`) REFERENCES `employee` (`employee_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ------------------------------------------------------------
-- 5. booking_staff_change_log (staff-reassignment audit trail)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `booking_staff_change_log` (
  `change_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `booking_id` INT NOT NULL,
  `user_id` INT DEFAULT NULL,
  `original_employee_id` INT DEFAULT NULL,
  `new_employee_id` INT DEFAULT NULL,
  `reason` ENUM('STAFF_ABSENT','STAFF_LEAVE','STAFF_UNAVAILABLE','CUSTOMER_REQUEST','ADMIN_CHANGE') NOT NULL,
  `note` VARCHAR(255) DEFAULT NULL,
  `changed_by` VARCHAR(100) DEFAULT NULL,
  `changed_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  KEY `idx_bscl_booking` (`booking_id`),
  CONSTRAINT `fk_bscl_booking` FOREIGN KEY (`booking_id`) REFERENCES `bookings` (`booking_id`),
  CONSTRAINT `fk_bscl_orig_emp` FOREIGN KEY (`original_employee_id`) REFERENCES `employee` (`employee_id`),
  CONSTRAINT `fk_bscl_new_emp` FOREIGN KEY (`new_employee_id`) REFERENCES `employee` (`employee_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ------------------------------------------------------------
-- 6. employee_date_lock (pure mutex table for concurrency control -- no
--    business data lives here; see booking_eligibility_service.py)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `employee_date_lock` (
  `employee_id` INT NOT NULL,
  `lock_date` DATE NOT NULL,
  PRIMARY KEY (`employee_id`, `lock_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ------------------------------------------------------------
-- 7. New columns on existing tables (guarded / idempotent)
--
-- Uses native `IF NOT EXISTS` clauses (MySQL 8.0.29+ / MariaDB 10.0+)
-- instead of a guarded stored procedure: CREATE PROCEDURE writes into the
-- server's internal mysql.proc table, which on some installs (confirmed
-- while testing this migration against a local MariaDB whose system tables
-- were left behind by a version upgrade) is out of sync and rejects any
-- new procedure outright. Plain ALTER TABLE ... IF [NOT] EXISTS avoids that
-- dependency entirely and is supported on both target engines.
-- ------------------------------------------------------------
ALTER TABLE `employee`
  ADD COLUMN IF NOT EXISTS `current_status_id` INT NULL DEFAULT 1
    COMMENT 'FK status_employee.status_employee_id; 1=available' AFTER `position`;

ALTER TABLE `bookings`
  ADD COLUMN IF NOT EXISTS `assignment_type` ENUM('CUSTOMER_CHOICE','SYSTEM_PICK') NULL DEFAULT NULL
    COMMENT 'NULL = legacy row or admin-set, unknown provenance' AFTER `employee_id`;

-- Backfill: every existing employee row explicitly gets current_status_id = 1 (available)
UPDATE `employee` SET `current_status_id` = 1 WHERE `current_status_id` IS NULL;

-- Additive index for the new interval-overlap booking queries (idempotent)
ALTER TABLE `bookings`
  ADD INDEX IF NOT EXISTS `idx_emp_date_time` (`employee_id`, `booking_date`, `booking_time`);

-- Foreign key for employee.current_status_id -> status_employee.
-- NOTE: unlike the statements above this one is NOT re-run-safe (neither
-- MySQL nor MariaDB reliably support a portable "ADD CONSTRAINT IF NOT
-- EXISTS" for foreign keys). Run this migration once per database; if you
-- must re-run it, comment out this ALTER TABLE first if fk_employee_status
-- already exists (it will error with "Duplicate foreign key constraint
-- name", which is harmless and can be ignored).
ALTER TABLE `employee`
  ADD CONSTRAINT `fk_employee_status` FOREIGN KEY (`current_status_id`) REFERENCES `status_employee` (`status_employee_id`);
