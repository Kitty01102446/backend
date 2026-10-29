-- ============================================================
-- Phase 6 migration: System Admin (role_id=4) backoffice
--   - store approval workflow (pending/rejected statuses + audit fields)
--   - user ban/suspend flag
--   - review moderation (hide instead of hard delete)
--   - complaint tickets (new table)
--   - site_content for banners/announcements (new table)
--
-- Safe to run multiple times (idempotent). Never drops or truncates
-- anything. Run this AFTER nailshop.sql and phase1-5 migrations.
-- ============================================================

-- ------------------------------------------------------------
-- 1. status_store: pending/rejected statuses for the store
--    approval workflow (ids land on 4 and 5 since table already has 1-3)
-- ------------------------------------------------------------
INSERT INTO `status_store` (`status_store_name`, `description`)
SELECT * FROM (SELECT 'pending' AS n, 'ร้านรออนุมัติจากผู้ดูแลระบบ' AS d) AS tmp
WHERE NOT EXISTS (SELECT 1 FROM `status_store` WHERE `status_store_name` = 'pending');

INSERT INTO `status_store` (`status_store_name`, `description`)
SELECT * FROM (SELECT 'rejected' AS n, 'ร้านถูกปฏิเสธโดยผู้ดูแลระบบ' AS d) AS tmp
WHERE NOT EXISTS (SELECT 1 FROM `status_store` WHERE `status_store_name` = 'rejected');

-- ------------------------------------------------------------
-- 2. store: admin evaluation/approval audit fields
-- ------------------------------------------------------------
ALTER TABLE `store`
  ADD COLUMN IF NOT EXISTS `admin_note` TEXT DEFAULT NULL AFTER `status_store_id`,
  ADD COLUMN IF NOT EXISTS `approved_by` INT DEFAULT NULL AFTER `admin_note`,
  ADD COLUMN IF NOT EXISTS `approved_at` DATETIME DEFAULT NULL AFTER `approved_by`,
  ADD COLUMN IF NOT EXISTS `rejection_reason` VARCHAR(255) DEFAULT NULL AFTER `approved_at`;

-- ------------------------------------------------------------
-- 3. users: ban/suspend flag
-- ------------------------------------------------------------
ALTER TABLE `users`
  ADD COLUMN IF NOT EXISTS `is_banned` TINYINT(1) NOT NULL DEFAULT 0 AFTER `role_id`,
  ADD COLUMN IF NOT EXISTS `ban_reason` VARCHAR(255) DEFAULT NULL AFTER `is_banned`,
  ADD COLUMN IF NOT EXISTS `banned_at` DATETIME DEFAULT NULL AFTER `ban_reason`,
  ADD COLUMN IF NOT EXISTS `banned_by` INT DEFAULT NULL AFTER `banned_at`;

-- ------------------------------------------------------------
-- 4. review: hide instead of hard-delete (keeps an audit trail)
-- ------------------------------------------------------------
ALTER TABLE `review`
  ADD COLUMN IF NOT EXISTS `is_hidden` TINYINT(1) NOT NULL DEFAULT 0 AFTER `comment`,
  ADD COLUMN IF NOT EXISTS `hidden_reason` VARCHAR(255) DEFAULT NULL AFTER `is_hidden`;

-- ------------------------------------------------------------
-- 5. complaint -- ticket system between customer/store and admin
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `complaint` (
  `complaint_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `booking_id` INT DEFAULT NULL,
  `reporter_user_id` INT NOT NULL,
  `against_store_id` INT DEFAULT NULL,
  `subject` VARCHAR(200) NOT NULL,
  `detail` TEXT DEFAULT NULL,
  `status` ENUM('OPEN','IN_REVIEW','RESOLVED','REJECTED') NOT NULL DEFAULT 'OPEN',
  `resolution_note` TEXT DEFAULT NULL,
  `resolved_by` INT DEFAULT NULL,
  `resolved_at` DATETIME DEFAULT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  KEY `idx_complaint_status` (`status`),
  KEY `idx_complaint_reporter` (`reporter_user_id`),
  KEY `idx_complaint_store` (`against_store_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ------------------------------------------------------------
-- 6. site_content -- banners/announcements/news managed by admin
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `site_content` (
  `content_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `content_type` ENUM('BANNER','ANNOUNCEMENT','NEWS') NOT NULL,
  `title` VARCHAR(200) NOT NULL,
  `body` TEXT DEFAULT NULL,
  `image_url` VARCHAR(255) DEFAULT NULL,
  `link_url` VARCHAR(255) DEFAULT NULL,
  `display_order` INT NOT NULL DEFAULT 0,
  `is_active` TINYINT(1) NOT NULL DEFAULT 1,
  `created_by` INT DEFAULT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  KEY `idx_content_type_active` (`content_type`, `is_active`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
