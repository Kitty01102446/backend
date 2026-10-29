-- ============================================================
-- Phase 5 migration: customer booking management
--   - cancellation audit fields on `bookings`
--   - two new booking statuses (reschedule pending, customer/store side)
--   - booking_reschedule_request (also serves as reschedule history)
--   - notification (shared between customer and store recipients)
--
-- Safe to run multiple times (idempotent). Never drops or truncates
-- anything. Run this AFTER nailshop.sql and phase1-4 migrations.
-- ============================================================

-- ------------------------------------------------------------
-- 1. bookings: cancellation audit fields
-- ------------------------------------------------------------
ALTER TABLE `bookings`
  ADD COLUMN IF NOT EXISTS `cancellation_reason` TEXT DEFAULT NULL AFTER `deleted_at`,
  ADD COLUMN IF NOT EXISTS `cancelled_by` ENUM('customer','store') DEFAULT NULL AFTER `cancellation_reason`,
  ADD COLUMN IF NOT EXISTS `cancelled_at` DATETIME DEFAULT NULL AFTER `cancelled_by`;

-- ------------------------------------------------------------
-- 2. status_booking: two new reschedule-pending statuses
--    (table is AUTO_INCREMENT=5 already, so these land on ids 5 and 6)
-- ------------------------------------------------------------
INSERT INTO `status_booking` (`status_booking_name`, `description`)
SELECT * FROM (SELECT 'reschedule_pending_customer' AS n, 'รอร้านพิจารณาการเลื่อนนัด (ลูกค้าขอเลื่อน)' AS d) AS tmp
WHERE NOT EXISTS (SELECT 1 FROM `status_booking` WHERE `status_booking_name` = 'reschedule_pending_customer');

INSERT INTO `status_booking` (`status_booking_name`, `description`)
SELECT * FROM (SELECT 'reschedule_pending_store' AS n, 'ร้านขอเลื่อนนัด รอลูกค้ายืนยัน' AS d) AS tmp
WHERE NOT EXISTS (SELECT 1 FROM `status_booking` WHERE `status_booking_name` = 'reschedule_pending_store');

-- ------------------------------------------------------------
-- 3. booking_reschedule_request
--    rows are never deleted -- status moves pending -> approved/rejected/cancelled,
--    so this table doubles as the reschedule history/audit trail.
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `booking_reschedule_request` (
  `request_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `booking_id` INT NOT NULL,
  `requested_by` ENUM('customer','store') NOT NULL,
  `old_date` DATE NOT NULL,
  `old_time` TIME NOT NULL,
  `proposed_date` DATE NOT NULL,
  `proposed_time` TIME NOT NULL,
  `reason` VARCHAR(500) DEFAULT NULL,
  `status` ENUM('pending','approved','rejected','cancelled') NOT NULL DEFAULT 'pending',
  `response_note` VARCHAR(500) DEFAULT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `responded_at` DATETIME DEFAULT NULL,
  KEY `idx_brr_booking` (`booking_id`),
  KEY `idx_brr_booking_status` (`booking_id`, `status`),
  CONSTRAINT `fk_brr_booking` FOREIGN KEY (`booking_id`) REFERENCES `bookings` (`booking_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ------------------------------------------------------------
-- 4. notification
--    recipient_user_id works for both a customer (users.user_id) and a
--    store owner (also a users.user_id, via store.user_id) -- no separate
--    "recipient type" table needed.
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `notification` (
  `notification_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `recipient_user_id` INT NOT NULL,
  `booking_id` INT DEFAULT NULL,
  `type` VARCHAR(50) NOT NULL,
  `title` VARCHAR(200) NOT NULL,
  `message` VARCHAR(500) NOT NULL,
  `is_read` TINYINT(1) NOT NULL DEFAULT 0,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  KEY `idx_notif_recipient` (`recipient_user_id`, `is_read`),
  CONSTRAINT `fk_notif_booking` FOREIGN KEY (`booking_id`) REFERENCES `bookings` (`booking_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
