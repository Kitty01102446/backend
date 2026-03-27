-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Mar 27, 2026 at 12:56 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `nailshop`
--

-- --------------------------------------------------------

--
-- Table structure for table `address`
--

CREATE TABLE IF NOT EXISTS `address` (
  `address_id` int(11) NOT NULL,
  `province` varchar(200) DEFAULT NULL,
  `district` varchar(200) DEFAULT NULL,
  `subdistrict` varchar(200) DEFAULT NULL,
  `postal_code` varchar(20) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `deleted_at` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `address`
--

INSERT INTO `address` (`address_id`, `province`, `district`, `subdistrict`, `postal_code`, `user_id`, `created_at`, `updated_at`, `deleted_at`) VALUES
(1, 'Bangkok', 'Lat Phrao', 'Chokchai 4', '10230', 1, '2025-12-13 14:47:00', NULL, NULL),
(2, 'Bangkok', 'Bang Khen', 'Anusawari', '10220', 2, '2025-12-13 14:47:00', NULL, NULL),
(3, 'Nonthaburi', 'Muang', 'Bang Krasor', '11000', 3, '2025-12-13 14:47:00', NULL, NULL),
(4, 'Khon Kaen', 'Mueang', 'Nai Mueang', '40000', 4, '2025-12-13 14:47:00', NULL, NULL),
(5, 'Khon Kaen', 'Mueang', 'Sila', '40000', 5, '2025-12-13 14:47:00', NULL, NULL),
(6, 'Khon Kaen', 'Ban Pet', 'Ban Pet', '40000', 6, '2025-12-13 14:47:00', NULL, NULL),
(7, 'Khon Kaen', 'Chum Phae', 'Chum Phae', '40130', 7, '2025-12-13 14:47:00', NULL, NULL),
(8, 'Khon Kaen', 'Phra Yuen', 'Phra Yuen', '40320', 8, '2025-12-13 14:47:00', NULL, NULL),
(9, 'Khon Kaen', 'Nong Ruea', 'Nong Ruea', '40210', 9, '2025-12-13 14:47:00', NULL, NULL),
(10, 'Khon Kaen', 'Ban Haet', 'Ban Haet', '40110', 10, '2025-12-13 14:47:00', NULL, NULL),
(11, 'Khon Kaen', 'Nam Phong', 'Nam Phong', '40140', 11, '2025-12-13 14:47:00', NULL, NULL),
(12, 'Khon Kaen', 'Samran', 'Samran', '40270', 12, '2025-12-13 14:47:00', NULL, NULL),
(13, 'Khon Kaen', 'Phu Wiang', 'Phu Wiang', '40150', 13, '2025-12-13 14:47:00', NULL, NULL),
(14, 'Khon Kaen', 'Mancha Khiri', 'Mancha Khiri', '40160', 14, '2025-12-13 14:47:00', NULL, NULL),
(15, 'Khon Kaen', 'Waeng Yai', 'Waeng Yai', '40330', 15, '2025-12-13 14:47:00', NULL, NULL),
(16, 'Khon Kaen', 'Waeng Noi', 'Waeng Noi', '40250', 16, '2025-12-13 14:47:00', NULL, NULL),
(17, 'Khon Kaen', 'Ubonrat', 'Ubonrat', '40250', 17, '2025-12-13 14:47:00', NULL, NULL),
(18, 'Khon Kaen', 'Khok Si', 'Khok Si', '40220', 18, '2025-12-13 14:47:00', NULL, NULL),
(19, 'Khon Kaen', 'Khao Suan Kwang', 'Khao Suan Kwang', '40280', 19, '2025-12-13 14:47:00', NULL, NULL),
(20, 'Khon Kaen', 'Kranuan', 'Kranuan', '40170', 20, '2025-12-13 14:47:00', NULL, NULL),
(21, 'Khon Kaen', 'Chonnabot', 'Chonnabot', '40160', 21, '2025-12-13 14:47:00', NULL, NULL),
(22, 'Khon Kaen', 'Ban Phai', 'Ban Phai', '40110', 22, '2025-12-13 14:47:00', NULL, NULL),
(23, 'Khon Kaen', 'Phon', 'Phon', '40120', 23, '2025-12-13 14:47:00', NULL, NULL),
(24, 'Khon Kaen', 'Nong Na Kham', 'Nong Na Kham', '40310', 24, '2025-12-13 14:47:00', NULL, NULL),
(25, 'Khon Kaen', 'Tha Phra', 'Tha Phra', '40260', 25, '2025-12-13 14:47:00', NULL, NULL),
(26, 'Khon Kaen', 'Don Chang', 'Don Chang', '40000', 26, '2025-12-13 14:47:00', NULL, NULL),
(27, 'Khon Kaen', 'Laonadee', 'Laonadee', '40000', 27, '2025-12-13 14:47:00', NULL, NULL),
(28, 'Khon Kaen', 'Bueng Nakhon', 'Bueng Nakhon', '40000', 28, '2025-12-13 14:47:00', NULL, NULL),
(29, 'Khon Kaen', 'Saphan Mit', 'Saphan Mit', '40000', 29, '2025-12-13 14:47:00', NULL, NULL),
(30, 'Khon Kaen', 'Klang Mueang', 'Klang Mueang', '40000', 30, '2025-12-13 14:47:00', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `bill`
--

CREATE TABLE IF NOT EXISTS `bill` (
  `bill_id` INT(11) NOT NULL AUTO_INCREMENT,
  `total_amount` DECIMAL(10,2) DEFAULT 0.00,
  `store_id` INT(11) DEFAULT NULL,
  `status_id` INT(11) DEFAULT NULL,
  PRIMARY KEY (`bill_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `bill`
--

INSERT INTO `bill` (`bill_id`, `total_amount`, `store_id`, `status_id`) VALUES
(1, 450, 1, 1),
(2, 900, 1, 1),
(3, 1200, 2, 1),
(4, 800, 2, 1),
(5, 650, 3, 1);

-- --------------------------------------------------------

--
-- Table structure for table `booking`
--

CREATE TABLE IF NOT EXISTS `booking` (
  `booking_id` int(11) NOT NULL,
  `booking_date` date DEFAULT NULL,
  `booking_time` time DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `employee_id` int(11) DEFAULT NULL,
  `store_id` int(11) DEFAULT NULL,
  `type_booking_id` int(11) DEFAULT NULL,
  `status_id` int(11) DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `booking`
--

INSERT INTO `booking` (`booking_id`, `booking_date`, `booking_time`, `user_id`, `employee_id`, `store_id`, `type_booking_id`, `status_id`, `deleted_at`, `created_at`, `updated_at`) VALUES
(1, '2025-01-10', '11:00:00', 1, 1, 1, 1, 2, NULL, '2026-01-12 20:56:43', '2026-01-12 20:56:43'),
(2, '2025-01-10', '12:00:00', 2, 2, 1, 1, 2, NULL, '2026-01-12 20:56:43', '2026-01-12 20:56:43'),
(3, '2025-01-10', '14:00:00', 3, 4, 2, 2, 1, NULL, '2026-01-12 20:56:43', '2026-01-12 20:56:43'),
(4, '2025-01-11', '10:00:00', 4, 5, 2, 1, 3, NULL, '2026-01-12 20:56:43', '2026-01-12 20:56:43'),
(5, '2025-01-11', '13:00:00', 5, 6, 2, 3, 3, NULL, '2026-01-12 20:56:43', '2026-01-12 20:56:43'),
(6, '2025-01-12', '09:30:00', 6, 7, 3, 1, 2, NULL, '2026-01-12 20:56:43', '2026-01-12 20:56:43'),
(7, '2025-01-12', '15:00:00', 7, 8, 3, 3, 2, NULL, '2026-01-12 20:56:43', '2026-01-12 20:56:43'),
(8, '2025-01-12', '16:00:00', 8, 9, 3, 1, 1, NULL, '2026-01-12 20:56:43', '2026-01-12 20:56:43'),
(9, '2025-01-13', '10:00:00', 9, 10, 3, 2, 2, NULL, '2026-01-12 20:56:43', '2026-01-12 20:56:43'),
(10, '2025-01-13', '11:30:00', 10, 3, 1, 1, 3, NULL, '2026-01-12 20:56:43', '2026-01-12 20:56:43');

-- --------------------------------------------------------

--
-- Table structure for table `bookings`
--

CREATE TABLE IF NOT EXISTS `bookings` (
  `booking_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `store_id` int(11) NOT NULL,
  `employee_id` int(11) DEFAULT NULL,
  `booking_date` date NOT NULL,
  `booking_time` time NOT NULL,
  `customer_name` varchar(100) DEFAULT NULL,
  `customer_phone` varchar(20) DEFAULT NULL,
  `customer_line` varchar(50) DEFAULT NULL,
  `customer_email` varchar(100) DEFAULT NULL,
  `customer_note` text DEFAULT NULL,
  `total_price` decimal(10,2) DEFAULT NULL,
  `total_minutes` int(11) DEFAULT NULL,
  `status_booking_id` int(11) DEFAULT NULL,
  `type_booking_id` int(11) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `bookings`
--

INSERT INTO `bookings` (`booking_id`, `user_id`, `store_id`, `employee_id`, `booking_date`, `booking_time`, `customer_name`, `customer_phone`, `customer_line`, `customer_email`, `customer_note`, `total_price`, `total_minutes`, `status_booking_id`, `type_booking_id`, `created_at`, `updated_at`, `deleted_at`) VALUES
(1, 2, 1, NULL, '2026-01-14', '12:00:00', 'แป้งอ้วน', '0987654321', '', 'noona02@example.com', '', 800.00, 75, 1, 1, '2026-01-14 14:38:02', '2026-01-14 21:38:02', NULL),
(2, 3, 1, 2, '2026-01-30', '18:00:00', 'โบ๊ท', '0812345673', 'kanokwan.j', 'pawat03@example.com', 'asddfgg', 400.00, 45, 2, 1, '2026-01-14 14:40:32', '2026-02-19 15:20:55', NULL),
(3, 3, 1, 2, '2026-01-30', '18:00:00', 'โบ๊ท', '0812345673', 'kanokwan.j', 'pawat03@example.com', 'asddfgg', 400.00, 45, 2, 1, '2026-01-14 14:46:51', '2026-02-19 15:20:56', NULL),
(4, 3, 1, 2, '2026-01-30', '18:00:00', 'โบ๊ท', '0812345673', 'kanokwan.j', 'pawat03@example.com', 'asddfgg', 400.00, 45, 2, 1, '2026-01-14 14:47:38', '2026-02-19 15:20:56', NULL),
(5, 3, 1, 2, '2026-01-30', '18:00:00', 'โบ๊ท', '0812345673', 'kanokwan.j', 'pawat03@example.com', 'asddfgg', 400.00, 45, 2, 1, '2026-01-14 14:47:40', '2026-02-19 15:20:57', NULL),
(6, 3, 1, 2, '2026-01-30', '18:00:00', 'โบ๊ท', '0812345673', 'kanokwan.j', 'pawat03@example.com', 'asddfgg', 400.00, 45, 2, 1, '2026-01-14 14:48:48', '2026-02-19 15:31:25', NULL),
(7, 3, 1, 2, '2026-01-30', '18:00:00', 'โบ๊ท', '0812345673', 'kanokwan.j', 'pawat03@example.com', 'asddfgg', 400.00, 45, 2, 1, '2026-01-14 14:49:44', '2026-02-19 15:31:27', NULL),
(8, 3, 1, 2, '2026-01-30', '18:00:00', 'โบ๊ท', '0812345673', 'kanokwan.j', 'pawat03@example.com', 'asddfgg', 400.00, 45, 2, 1, '2026-01-14 14:50:35', '2026-02-19 15:32:01', NULL),
(9, 3, 1, 2, '2026-01-30', '18:00:00', 'โบ๊ท', '0812345673', 'kanokwan.j', 'pawat03@example.com', 'asddfgg', 400.00, 45, 2, 1, '2026-01-14 14:50:38', '2026-02-19 15:34:57', NULL),
(10, 3, 1, 2, '2026-01-30', '18:00:00', 'โบ๊ท', '0812345673', 'kanokwan.j', 'pawat03@example.com', 'asddfgg', 400.00, 45, 1, 1, '2026-01-14 14:52:22', '2026-01-14 21:52:22', NULL),
(11, 3, 1, 2, '2026-01-30', '18:00:00', 'โบ๊ท', '0812345673', 'kanokwan.j', 'pawat03@example.com', 'asddfgg', 400.00, 45, 1, 1, '2026-01-14 14:52:25', '2026-01-14 21:52:25', NULL),
(12, 3, 1, 2, '2026-01-30', '18:00:00', 'โบ๊ท', '0812345673', 'kanokwan.j', 'pawat03@example.com', 'asddfgg', 400.00, 45, 1, 1, '2026-01-14 14:53:46', '2026-01-14 21:53:46', NULL),
(13, 3, 1, 2, '2026-01-30', '18:00:00', 'โบ๊ท', '0812345673', 'kanokwan.j', 'pawat03@example.com', 'asddfgg', 400.00, 45, 1, 1, '2026-01-14 14:53:57', '2026-01-14 21:53:57', NULL),
(14, 3, 1, 2, '2026-01-30', '18:00:00', 'โบ๊ท', '0812345673', 'kanokwan.j', 'pawat03@example.com', 'asddfgg', 400.00, 45, 1, 1, '2026-01-14 14:54:39', '2026-01-14 21:54:39', NULL),
(15, 3, 1, 2, '2026-01-30', '18:00:00', 'โบ๊ท', '0812345673', 'kanokwan.j', 'pawat03@example.com', 'asddfgg', 400.00, 45, 1, 1, '2026-01-14 14:55:31', '2026-01-14 21:55:31', NULL),
(16, 3, 1, 2, '2026-01-30', '18:00:00', 'โบ๊ท', '0812345673', 'kanokwan.j', 'pawat03@example.com', 'asddfgg', 400.00, 45, 1, 1, '2026-01-14 14:55:35', '2026-01-14 21:55:35', NULL),
(17, 4, 1, 2, '2026-02-05', '14:00:00', 'เด็กดี', '0123456789', 'kitty', 'noona02@example.com', 'xcxcxcccxcxcxx', 1550.00, 110, 2, 1, '2026-01-15 08:02:39', '2026-02-19 15:29:14', NULL),
(18, 4, 1, 1, '2026-01-16', '10:00:00', 'แพน', '0812345674', '', 'nan04@example.com', '', 1550.00, 110, 1, 1, '2026-01-16 11:47:46', '2026-01-16 18:47:46', NULL),
(19, 4, 1, 1, '2026-01-16', '10:00:00', 'แพน', '0812345674', '', 'nan04@example.com', '', 1550.00, 110, 1, 1, '2026-01-16 12:19:51', '2026-01-16 19:19:51', NULL),
(20, 4, 1, 2, '2026-01-16', '11:00:00', 'แพน', '0812345674', '', 'nan04@example.com', '', 1550.00, 110, 1, 1, '2026-01-16 13:58:58', '2026-01-16 20:58:58', NULL),
(21, 1, 1, 1, '2026-01-23', '16:00:00', 'กอล์ฟ', '081234567', '', 'golf01@example.com', '', 1550.00, 110, 1, 1, '2026-01-17 14:25:32', '2026-01-17 21:25:32', NULL),
(22, 1, 1, 1, '2026-01-18', '13:00:00', 'กอล์ฟ', '081234567', '', 'golf01@example.com', '', 1550.00, 110, 1, 1, '2026-01-17 19:52:49', '2026-01-18 02:52:49', NULL),
(23, 1, 1, 1, '2026-01-27', '15:00:00', 'กอล์ฟ', '081234567', '', 'golf01@example.com', '', 1550.00, 110, 1, 1, '2026-01-17 19:53:31', '2026-01-18 02:53:31', NULL),
(24, 1, 1, 1, '2026-01-18', '12:00:00', 'กอล์ฟ', '081234567', '', 'golf01@example.com', '', 1600.00, 135, 1, 1, '2026-01-17 20:08:30', '2026-01-18 03:08:30', NULL),
(25, 1, 44, 131, '2026-01-18', '12:00:00', 'กอล์ฟ', '081234567', '', 'golf01@example.com', '', 798.00, 75, 1, 1, '2026-01-17 22:12:39', '2026-01-18 05:12:39', NULL),
(26, 1, 8, 23, '2026-01-28', '12:00:00', 'กอล์ฟ', '081234567', '', 'golf01@example.com', '', 598.00, 60, 1, 1, '2026-01-17 22:13:25', '2026-01-18 05:13:25', NULL),
(27, 1, 39, 116, '2026-01-19', '13:00:00', 'กอล์ฟ', '081234567', '', 'golf01@example.com', '', 598.00, 80, 1, 1, '2026-01-17 22:14:22', '2026-01-18 05:14:22', NULL),
(28, 1, 39, 116, '2026-01-19', '12:00:00', 'กอล์ฟ', '081234567', '', 'golf01@example.com', '', 598.00, 80, 1, 1, '2026-01-17 22:16:20', '2026-01-18 05:16:20', NULL),
(29, 1, 7, 20, '2026-01-20', '15:00:00', 'กอล์ฟ', '081234567', '', 'golf01@example.com', '', 796.00, 135, 1, 1, '2026-01-17 22:16:55', '2026-01-18 05:16:55', NULL),
(30, 1, 30, 89, '2026-01-20', '13:00:00', 'กอล์ฟ', '081234567', '', 'golf01@example.com', '', 1197.00, 110, 1, 1, '2026-01-17 22:17:32', '2026-01-18 05:17:32', NULL),
(31, 2, 1, NULL, '2026-01-27', '13:00:00', 'แป้งอ้วน', '0987654321', '', 'noona02@example.com', '', 598.00, 75, 1, 1, '2026-01-18 02:13:52', '2026-01-18 09:13:52', NULL),
(32, 2, 1, 1, '2026-01-20', '11:00:00', 'แป้งอ้วน', '0987654321', '', 'noona02@example.com', '', 299.00, 45, 1, 1, '2026-01-18 15:05:13', '2026-01-18 22:05:13', NULL),
(33, 25, 1, 1, '2026-01-20', '11:00:00', 'พลอย', '0812345685', '', 'ploy24@example.com', '', 598.00, 75, 1, 1, '2026-01-19 10:14:42', '2026-01-19 17:14:42', NULL),
(34, 10, 2, 4, '2026-01-19', '14:00:00', 'พีช', '0812345680', '', 'pit10@example.com', '', 798.00, 75, 2, 1, '2026-01-19 10:53:43', '2026-02-19 15:37:53', NULL),
(35, 50, 1, 2, '2026-02-16', '11:00:00', 'kitty44', '0675834567', '', 'sdfghj@gmail.com', '', 598.00, 105, 2, 1, '2026-02-13 13:21:37', '2026-02-19 15:31:18', NULL),
(36, 1, 2, 4, '2026-02-24', '14:00:00', 'คิตตี้', '081234567', '', 'golf01@example.com', '', 798.00, 75, 1, 1, '2026-02-24 15:35:43', '2026-02-24 22:35:43', NULL),
(37, 1, 2, NULL, '2026-02-25', '13:00:00', 'คิตตี้', '081234567', '', 'golf01@example.com', '', 399.00, 60, 2, 1, '2026-02-24 17:01:26', '2026-02-25 02:22:20', NULL),
(38, 4, 2, 4, '2026-02-25', '11:00:00', 'แพน', '0812345674', '', 'nan04@example.com', '', 1197.00, 135, 1, 1, '2026-02-24 17:19:11', '2026-02-25 00:19:11', NULL),
(39, 4, 2, 5, '2026-02-24', '14:00:00', 'แพน', '0812345674', '', 'nan04@example.com', '', 798.00, 75, 1, 1, '2026-02-24 18:25:21', '2026-02-25 01:25:21', NULL),
(40, 4, 2, NULL, '2026-02-24', '18:00:00', 'แพน', '0812345674', '', 'nan04@example.com', '', 798.00, 105, 1, 1, '2026-02-24 18:28:49', '2026-02-25 01:28:49', NULL),
(41, 4, 1, 3, '2026-02-24', '18:00:00', 'แพน', '0812345674', '', 'nan04@example.com', '', 299.00, 30, 2, 1, '2026-02-25 06:49:13', '2026-03-11 13:18:42', NULL),
(42, 4, 1, 1, '2026-02-24', '13:00:00', 'แพน', '0812345674', '', 'nan04@example.com', '', 299.00, 123, 1, 1, '2026-02-25 06:54:44', '2026-02-25 13:54:44', NULL),
(43, 4, 1, 1, '2026-02-24', '15:00:00', 'แพน', '0812345674', '', 'nan04@example.com', '', 299.00, 45, 1, 1, '2026-02-25 07:08:43', '2026-02-25 14:08:43', NULL),
(44, 4, 1, 3, '2026-02-24', '17:00:00', 'แพน', '0812345674', '', 'nan04@example.com', '', 598.00, 173, 1, 1, '2026-02-25 07:09:59', '2026-02-25 14:09:59', NULL),
(45, 1, 2, 6, '2026-03-11', '12:00:00', 'คิตตี้', '081234567', '', 'golf01@example.com', '', 399.00, 30, 2, 1, '2026-03-11 06:25:37', '2026-03-11 13:26:09', NULL),
(46, 1, 3, 10, '2026-03-11', '13:00:00', 'คิตตี้', '081234567', '', 'golf01@example.com', '', 499.00, 90, 2, 1, '2026-03-11 06:32:36', '2026-03-11 13:33:20', NULL),
(47, 1, 3, 9, '2026-03-18', '13:00:00', 'คิตตี้', '081234567', '', 'golf01@example.com', '', 499.00, 90, 2, 1, '2026-03-11 06:33:11', '2026-03-11 13:33:23', NULL),
(48, 1, 2, 6, '2026-03-11', '10:00:00', 'คิตตี้', '081234567', '', 'golf01@example.com', '', 399.00, 45, 1, 1, '2026-03-12 08:48:15', '2026-03-12 15:48:15', NULL),
(49, 1, 2, 6, '2026-03-11', '17:00:00', 'คิตตี้', '081234567', '', 'golf01@example.com', '', 399.00, 45, 1, 1, '2026-03-12 09:19:15', '2026-03-12 16:19:15', NULL),
(50, 1, 2, 6, '2026-03-11', '18:00:00', 'คิตตี้', '081234567', '', 'golf01@example.com', '', 399.00, 30, 1, 1, '2026-03-12 09:19:59', '2026-03-12 16:19:59', NULL),
(51, 1, 1, 3, '2026-03-11', '10:00:00', 'คิตตี้', '081234567', '', 'golf01@example.com', '', 299.00, 30, 1, 1, '2026-03-12 09:29:27', '2026-03-12 16:29:27', NULL),
(52, 1, 1, 3, '2026-03-19', '11:00:00', 'คิตตี้', '081234567', '', 'golf01@example.com', '', 1495.00, 308, 1, 1, '2026-03-13 14:46:24', '2026-03-13 21:46:24', NULL),
(53, 1, 1, 2, '2026-03-15', '11:00:00', 'คิตตี้', '081234567', '', 'golf01@example.com', '', 897.00, 135, 1, 1, '2026-03-13 14:47:26', '2026-03-13 21:47:26', NULL),
(54, 1, 1, NULL, '2026-03-15', '11:00:00', 'คิตตี้', '081234567', '', 'golf01@example.com', '', 897.00, 135, 1, 1, '2026-03-13 14:47:37', '2026-03-13 21:47:37', NULL),
(55, 1, 1, 3, '2026-03-12', '10:00:00', 'คิตตี้', '081234567', '', 'golf01@example.com', '', 299.00, 45, 1, 1, '2026-03-13 14:48:04', '2026-03-13 21:48:04', NULL),
(56, 57, 1, 2, '2026-03-26', '11:00:00', 'Chakrit', '0981231234', '', 'gg@gmail.com', '', 598.00, 110, 1, 1, '2026-03-25 15:51:20', '2026-03-25 22:51:20', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `booking_services`
--

CREATE TABLE IF NOT EXISTS `booking_services` (
  `booking_service_id` int(11) NOT NULL,
  `booking_id` int(11) NOT NULL,
  `service_id` int(11) NOT NULL,
  `service_name` varchar(100) DEFAULT NULL,
  `service_price` decimal(10,2) DEFAULT NULL,
  `service_minutes` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `booking_services`
--

INSERT INTO `booking_services` (`booking_service_id`, `booking_id`, `service_id`, `service_name`, `service_price`, `service_minutes`) VALUES
(1, 1, 5, 'Basic Pedicure', 300.00, 30),
(2, 1, 6, 'Gel Polish Feet', 500.00, 45),
(3, 2, 1, 'Basic Manicure', 250.00, 30),
(4, 2, 10, 'Nail Repair', 150.00, 15),
(5, 3, 1, 'Basic Manicure', 250.00, 30),
(6, 3, 10, 'Nail Repair', 150.00, 15),
(7, 4, 1, 'Basic Manicure', 250.00, 30),
(8, 4, 10, 'Nail Repair', 150.00, 15),
(9, 5, 1, 'Basic Manicure', 250.00, 30),
(10, 5, 10, 'Nail Repair', 150.00, 15),
(11, 6, 1, 'Basic Manicure', 250.00, 30),
(12, 6, 10, 'Nail Repair', 150.00, 15),
(13, 7, 1, 'Basic Manicure', 250.00, 30),
(14, 7, 10, 'Nail Repair', 150.00, 15),
(15, 8, 1, 'Basic Manicure', 250.00, 30),
(16, 8, 10, 'Nail Repair', 150.00, 15),
(17, 9, 1, 'Basic Manicure', 250.00, 30),
(18, 9, 10, 'Nail Repair', 150.00, 15),
(19, 10, 1, 'Basic Manicure', 250.00, 30),
(20, 10, 10, 'Nail Repair', 150.00, 15),
(21, 11, 1, 'Basic Manicure', 250.00, 30),
(22, 11, 10, 'Nail Repair', 150.00, 15),
(23, 12, 1, 'Basic Manicure', 250.00, 30),
(24, 12, 10, 'Nail Repair', 150.00, 15),
(25, 13, 1, 'Basic Manicure', 250.00, 30),
(26, 13, 10, 'Nail Repair', 150.00, 15),
(27, 14, 1, 'Basic Manicure', 250.00, 30),
(28, 14, 10, 'Nail Repair', 150.00, 15),
(29, 15, 1, 'Basic Manicure', 250.00, 30),
(30, 15, 10, 'Nail Repair', 150.00, 15),
(31, 16, 1, 'Basic Manicure', 250.00, 30),
(32, 16, 10, 'Nail Repair', 150.00, 15),
(33, 17, 3, 'Gel Art Premium', 900.00, 60),
(34, 17, 4, 'Spa Hand Treatment', 650.00, 50),
(35, 18, 3, 'Gel Art Premium', 900.00, 60),
(36, 18, 4, 'Spa Hand Treatment', 650.00, 50),
(37, 19, 3, 'Gel Art Premium', 900.00, 60),
(38, 19, 4, 'Spa Hand Treatment', 650.00, 50),
(39, 20, 3, 'Gel Art Premium', 900.00, 60),
(40, 20, 4, 'Spa Hand Treatment', 650.00, 50),
(41, 21, 3, 'Gel Art Premium', 900.00, 60),
(42, 21, 4, 'Spa Hand Treatment', 650.00, 50),
(43, 22, 3, 'Gel Art Premium', 900.00, 60),
(44, 22, 4, 'Spa Hand Treatment', 650.00, 50),
(45, 23, 3, 'Gel Art Premium', 900.00, 60),
(46, 23, 4, 'Spa Hand Treatment', 650.00, 50),
(47, 24, 1, 'Basic Manicure', 250.00, 30),
(48, 24, 2, 'Gel Polish Hands', 450.00, 45),
(49, 24, 3, 'Gel Art Premium', 900.00, 60),
(50, 25, 251, 'Gel Polish Hands', 399.00, 45),
(51, 25, 252, 'Basic Manicure', 399.00, 30),
(52, 26, 36, 'Hand Massage', 299.00, 20),
(53, 26, 37, 'Paraffin Wax', 299.00, 40),
(54, 27, 221, 'Gel Removal', 299.00, 20),
(55, 27, 222, 'Spa Pedicure', 299.00, 60),
(56, 28, 221, 'Gel Removal', 299.00, 20),
(57, 28, 222, 'Spa Pedicure', 299.00, 60),
(58, 29, 30, 'Basic Manicure', 199.00, 30),
(59, 29, 31, 'Organic Scrub', 199.00, 25),
(60, 29, 32, 'Hand Massage', 199.00, 20),
(61, 29, 33, 'Nail Art Premium', 199.00, 60),
(62, 30, 167, 'Hand Massage', 399.00, 20),
(63, 30, 168, 'Nail Art Premium', 399.00, 60),
(64, 30, 169, 'Callus Treatment', 399.00, 30),
(65, 31, 1, 'Basic Manicure', 299.00, 30),
(66, 31, 2, 'Gel Polish Hands', 299.00, 45),
(67, 32, 2, 'Gel Polish Hands', 299.00, 45),
(68, 33, 1, 'Basic Manicure', 299.00, 30),
(69, 33, 2, 'Gel Polish Hands', 299.00, 45),
(70, 34, 5, 'Basic Pedicure', 399.00, 30),
(71, 34, 6, 'Gel Polish Feet', 399.00, 45),
(72, 35, 2, 'Gel Polish Hands', 299.00, 45),
(73, 35, 3, 'Gel Art Premium', 299.00, 60),
(74, 36, 5, 'Basic Pedicure', 399.00, 30),
(75, 36, 6, 'Gel Polish Feet', 399.00, 45),
(76, 37, 7, 'Foot Spa Deluxe', 399.00, 60),
(77, 38, 5, 'Basic Pedicure', 399.00, 30),
(78, 38, 6, 'Gel Polish Feet', 399.00, 45),
(79, 38, 7, 'Foot Spa Deluxe', 399.00, 60),
(80, 39, 5, 'Basic Pedicure', 399.00, 30),
(81, 39, 6, 'Gel Polish Feet', 399.00, 45),
(82, 40, 6, 'Gel Polish Feet', 399.00, 45),
(83, 40, 7, 'Foot Spa Deluxe', 399.00, 60),
(84, 41, 1, 'ฟหกอ่ีัะพำกแอ่', 299.00, 30),
(85, 42, 530, 'หำเะพ้ั่ะีเ้เกด', 299.00, 123),
(86, 43, 2, 'Gel Polish Hands', 299.00, 45),
(87, 44, 4, 'Spa deemak', 299.00, 50),
(88, 44, 530, 'หำเะพ้ั่ะีเ้เกด', 299.00, 123),
(89, 45, 5, 'Basic Pedicure', 399.00, 30),
(90, 46, 8, 'Combo Gel Hand + Foot', 499.00, 90),
(91, 47, 9, 'Acrylic Extension', 499.00, 90),
(92, 48, 6, 'Gel Polish Feet', 399.00, 45),
(93, 49, 6, 'Gel Polish Feet', 399.00, 45),
(94, 50, 5, 'Basic Pedicure', 399.00, 30),
(95, 51, 1, 'ฟหกอ่ีัะพำกแอ่', 299.00, 30),
(96, 52, 1, 'ฟหกอ่ีัะพำกแอ่', 299.00, 30),
(97, 52, 2, 'Gel Polish Hands', 299.00, 45),
(98, 52, 3, 'Gel Art Premium', 299.00, 60),
(99, 52, 4, 'Spa deemak', 299.00, 50),
(100, 52, 530, 'หำเะพ้ั่ะีเ้เกด', 299.00, 123),
(101, 53, 1, 'ฟหกอ่ีัะพำกแอ่', 299.00, 30),
(102, 53, 2, 'Gel Polish Hands', 299.00, 45),
(103, 53, 3, 'Gel Art Premium', 299.00, 60),
(104, 54, 1, 'ฟหกอ่ีัะพำกแอ่', 299.00, 30),
(105, 54, 2, 'Gel Polish Hands', 299.00, 45),
(106, 54, 3, 'Gel Art Premium', 299.00, 60),
(107, 55, 2, 'Gel Polish Hands', 299.00, 45),
(108, 56, 3, 'Gel Art Premium', 299.00, 60),
(109, 56, 4, 'Spa deemak', 299.00, 50);

-- --------------------------------------------------------

--
-- Table structure for table `click_log`
--

CREATE TABLE IF NOT EXISTS `click_log` (
  `click_log_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `store_id` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `click_log`
--

INSERT INTO `click_log` (`click_log_id`, `user_id`, `store_id`, `created_at`, `updated_at`, `deleted_at`) VALUES
(1, 1, 1, '2025-12-10 13:41:17', NULL, NULL),
(2, 1, 2, '2025-12-10 13:41:17', NULL, NULL),
(3, 2, 1, '2025-12-10 13:41:17', NULL, NULL),
(4, 3, 3, '2025-12-10 13:41:17', NULL, NULL),
(5, 4, 2, '2025-12-10 13:41:17', NULL, NULL),
(6, 6, 3, '2025-12-10 13:45:17', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `employee`
--

CREATE TABLE IF NOT EXISTS `employee` (
  `employee_id` int(11) NOT NULL,
  `fullname` varchar(200) DEFAULT NULL,
  `phone` varchar(50) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `position` varchar(200) DEFAULT NULL,
  `store_id` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `deleted_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `employee`
--

INSERT INTO `employee` (`employee_id`, `fullname`, `phone`, `email`, `position`, `store_id`, `created_at`, `updated_at`, `deleted_at`) VALUES
(1, 'Amm Chutima', '0891112222', NULL, 'Nail Artist', 1, '2026-01-12 21:17:12', '2026-01-12 21:17:12', NULL),
(2, 'Bam Ratchada', '0891113333', 'ddcvtrv@gmail.com', 'Nail Artist', 1, '2026-01-12 21:17:12', '2026-02-25 00:53:05', NULL),
(3, 'Mild Kanokwan', '0891114444', NULL, 'Cashier', 1, '2026-01-12 21:17:12', '2026-01-12 21:17:12', NULL),
(4, 'ส้มจี๊ด', '0892221111', 'fdsxcgfd@gmail.com', 'Nail Artist', 2, '2026-01-12 21:17:12', '2026-02-25 01:54:46', NULL),
(5, 'Gift Supawadee', '0892222222', NULL, 'Nail Artist', 2, '2026-01-12 21:17:12', '2026-01-12 21:17:12', NULL),
(6, 'Tarn Warisa', '0892223333', NULL, 'Receptionist', 2, '2026-01-12 21:17:12', '2026-01-12 21:17:12', NULL),
(7, 'View Oranicha', '0893331111', NULL, 'Nail Artist', 3, '2026-01-12 21:17:12', '2026-01-12 21:17:12', NULL),
(8, 'Praew Nattida', '0893332222', NULL, 'Spa Therapist', 3, '2026-01-12 21:17:12', '2026-01-12 21:17:12', NULL),
(9, 'Nin Thanchanok', '0893333333', NULL, 'Nail Artist', 3, '2026-01-12 21:17:12', '2026-01-12 21:17:12', NULL),
(10, 'Dream Sirinya', '0893334444', NULL, 'Cashier', 3, '2026-01-12 21:17:12', '2026-01-12 21:17:12', NULL),
(11, 'Kanya Rakdee', '0840041001', NULL, 'Nail Artist', 4, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(12, 'Chaiwat Somboon', '0840041002', NULL, 'Spa Therapist', 4, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(13, 'Suda Siri', '0840041003', NULL, 'Receptionist', 4, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(14, 'Mana Chuenjai', '0850051001', NULL, 'Nail Artist', 5, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(15, 'Wanee Sook', '0850051002', NULL, 'Nail Artist', 5, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(16, 'Piti Ruen', '0850051003', NULL, 'Cashier', 5, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(17, 'Aree Ya', '0860061001', NULL, 'Nail Artist', 6, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(18, 'Sombat Dee', '0860061002', NULL, 'Spa Therapist', 6, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(19, 'Napa Sky', '0860061003', NULL, 'Receptionist', 6, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(20, 'View Oranicha', '0870071001', NULL, 'Nail Artist', 7, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(21, 'Praew Nattida', '0870071002', NULL, 'Spa Therapist', 7, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(22, 'Nin Thanchanok', '0870071003', NULL, 'Nail Artist', 7, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(23, 'Siriwan Jan', '0810081001', NULL, 'Nail Artist', 8, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(24, 'Tanawat Dee', '0810081002', NULL, 'Receptionist', 8, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(25, 'Pimploy Sook', '0810081003', NULL, 'Nail Artist', 8, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(26, 'Wichai Bold', '0810091001', NULL, 'Spa Therapist', 9, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(27, 'Nalin Sky', '0810091002', NULL, 'Nail Artist', 9, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(28, 'Korn Rawi', '0810091003', NULL, 'Cashier', 9, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(29, 'Dream Sirinya', '0810101001', NULL, 'Cashier', 10, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(30, 'Aom Amm', '0810101002', NULL, 'Nail Artist', 10, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(31, 'Jib Jaba', '0810101003', NULL, 'Nail Artist', 10, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(32, 'Pathama Wong', '0810111001', NULL, 'Nail Artist', 11, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(33, 'Santi Rak', '0810111002', NULL, 'Spa Therapist', 11, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(34, 'Ubol Siri', '0810111003', NULL, 'Receptionist', 11, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(35, 'Vipa Kaset', '0810121001', NULL, 'Nail Artist', 12, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(36, 'Sakda Muang', '0810121002', NULL, 'Nail Artist', 12, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(37, 'Malee Suan', '0810121003', NULL, 'Cashier', 12, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(38, 'Ananda Jai', '0810131001', NULL, 'Nail Artist', 13, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(39, 'Boonma Mee', '0810131002', NULL, 'Spa Therapist', 13, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(40, 'Chulee Porn', '0810131003', NULL, 'Receptionist', 13, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(41, 'Dara Rat', '0810141001', NULL, 'Nail Artist', 14, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(42, 'Ekkachai Wang', '0810141002', NULL, 'Nail Artist', 14, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(43, 'Fahใส Glow', '0810141003', NULL, 'Cashier', 14, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(44, 'Ganda Bloom', '0810151001', NULL, 'Nail Artist', 15, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(45, 'Hathaichanok L', '0810151002', NULL, 'Spa Therapist', 15, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(46, 'Ittipol Run', '0810151003', NULL, 'Receptionist', 15, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(47, 'Jariya Moon', '0810161001', NULL, 'Nail Artist', 16, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(48, 'Kwan Jai', '0810161002', NULL, 'Nail Artist', 16, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(49, 'Ladda Land', '0810161003', NULL, 'Cashier', 16, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(50, 'Manee Mark', '0810171001', NULL, 'Nail Artist', 17, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(51, 'Noppadon Best', '0810171002', NULL, 'Spa Therapist', 17, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(52, 'Orawan Sun', '0810171003', NULL, 'Receptionist', 17, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(53, 'Pailin Blue', '0810181001', NULL, 'Nail Artist', 18, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(54, 'Q-Taro San', '0810181002', NULL, 'Nail Artist', 18, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(55, 'Rattana Pearl', '0810181003', NULL, 'Cashier', 18, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(56, 'Somsak Power', '0810191001', NULL, 'Nail Artist', 19, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(57, 'Tida Thai', '0810191002', NULL, 'Spa Therapist', 19, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(58, 'Usa Star', '0810191003', NULL, 'Receptionist', 19, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(59, 'Veera Win', '0810201001', NULL, 'Nail Artist', 20, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(60, 'Wandee Full', '0810201002', NULL, 'Nail Artist', 20, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(61, 'X-Man Strong', '0810201003', NULL, 'Cashier', 20, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(62, 'Yupa Queen', '0810211001', NULL, 'Nail Artist', 21, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(63, 'Zaza Zoom', '0810211002', NULL, 'Spa Therapist', 21, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(64, 'Araya Shine', '0810211003', NULL, 'Receptionist', 21, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(65, 'Banyat Law', '0810221001', NULL, 'Nail Artist', 22, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(66, 'Chatchai Fast', '0810221002', NULL, 'Nail Artist', 22, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(67, 'Duang Jai', '0810221003', NULL, 'Cashier', 22, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(68, 'Ekarat Gold', '0810231001', NULL, 'Nail Artist', 23, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(69, 'Fonthip Rain', '0810231002', NULL, 'Spa Therapist', 23, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(70, 'Gumpol Great', '0810231003', NULL, 'Receptionist', 23, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(71, 'Hansa Happy', '0810241001', NULL, 'Nail Artist', 24, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(72, 'Itsara Free', '0810241002', NULL, 'Nail Artist', 24, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(73, 'Jinda Jewel', '0810241003', NULL, 'Cashier', 24, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(74, 'Kamon Heart', '0810251001', NULL, 'Nail Artist', 25, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(75, 'Likit Write', '0810251002', NULL, 'Spa Therapist', 25, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(76, 'Mayuree Bird', '0810251003', NULL, 'Receptionist', 25, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(77, 'Naruemol Soft', '0810261001', NULL, 'Nail Artist', 26, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(78, 'Ong-art Brave', '0810261002', NULL, 'Nail Artist', 26, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(79, 'Pornthip Gift', '0810261003', NULL, 'Cashier', 26, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(80, 'Roong Sky', '0810271001', NULL, 'Nail Artist', 27, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(81, 'Suda Sweet', '0810271002', NULL, 'Spa Therapist', 27, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(82, 'Tawatchai Vic', '0810271003', NULL, 'Receptionist', 27, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(83, 'Urai Spark', '0810281001', NULL, 'Nail Artist', 28, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(84, 'Vichit Victory', '0810281002', NULL, 'Nail Artist', 28, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(85, 'Wipada Wide', '0810281003', NULL, 'Cashier', 28, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(86, 'Ying Luck', '0810291001', NULL, 'Nail Artist', 29, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(87, 'Zinny Cute', '0810291002', NULL, 'Spa Therapist', 29, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(88, 'Amara Love', '0810291003', NULL, 'Receptionist', 29, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(89, 'Boon-ear Kind', '0810301001', NULL, 'Nail Artist', 30, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(90, 'Chaiyo Cheers', '0810301002', NULL, 'Nail Artist', 30, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(91, 'Danai Smart', '0810301003', NULL, 'Cashier', 30, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(92, 'Em-on Soft', '0810311001', NULL, 'Nail Artist', 31, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(93, 'Fuang-fa Flow', '0810311002', NULL, 'Spa Therapist', 31, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(94, 'Gai-thong Gold', '0810311003', NULL, 'Receptionist', 31, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(95, 'Harin Hope', '0810321001', NULL, 'Nail Artist', 32, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(96, 'In-thira Inside', '0810321002', NULL, 'Nail Artist', 32, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(97, 'Janjira June', '0810321003', NULL, 'Cashier', 32, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(98, 'Kitti Key', '0810331001', NULL, 'Nail Artist', 33, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(99, 'Lamyai Fruit', '0810331002', NULL, 'Spa Therapist', 33, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(100, 'Mon-chai Peak', '0810331003', NULL, 'Receptionist', 33, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(101, 'Niran Ever', '0810341001', NULL, 'Nail Artist', 34, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(102, 'Orasa Rose', '0810341002', NULL, 'Nail Artist', 34, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(103, 'Piti Peak', '0810341003', NULL, 'Cashier', 34, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(104, 'Rung-rat Shine', '0810351001', NULL, 'Nail Artist', 35, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(105, 'Siri-wan Silk', '0810351002', NULL, 'Spa Therapist', 35, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(106, 'Thana Wealth', '0810351003', NULL, 'Receptionist', 35, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(107, 'U-then Ultra', '0810361001', NULL, 'Nail Artist', 36, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(108, 'Vina Vine', '0810361002', NULL, 'Nail Artist', 36, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(109, 'Wuthichai Work', '0810361003', NULL, 'Cashier', 36, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(110, 'Yada Young', '0810371001', NULL, 'Nail Artist', 37, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(111, 'Zeen Fine', '0810371002', NULL, 'Spa Therapist', 37, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(112, 'A-khit Art', '0810371003', NULL, 'Receptionist', 37, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(113, 'Boon-mee Bless', '0810381001', NULL, 'Nail Artist', 38, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(114, 'Chom-poo Pink', '0810381002', NULL, 'Nail Artist', 38, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(115, 'Duan-pen Moon', '0810381003', NULL, 'Cashier', 38, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(116, 'Erawan Elephant', '0810391001', NULL, 'Nail Artist', 39, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(117, 'Fai-kham Yarn', '0810391002', NULL, 'Spa Therapist', 39, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(118, 'Gade-kaew Glass', '0810391003', NULL, 'Receptionist', 39, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(119, 'หอมหวน Scent', '0810401001', NULL, 'Nail Artist', 40, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(120, 'อุ่นใจ Warm', '0810401002', NULL, 'Nail Artist', 40, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(121, 'เพียงพอ Enough', '0810401003', NULL, 'Cashier', 40, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(122, 'ขวัญข้าว Rice', '0810411001', NULL, 'Nail Artist', 41, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(123, 'เจ้าคุณ Noble', '0810411002', NULL, 'Spa Therapist', 41, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(124, 'น้ำริน Stream', '0810411003', NULL, 'Receptionist', 41, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(125, 'ปิ่นมณี Pin', '0810421001', NULL, 'Nail Artist', 42, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(126, 'ฟ้าลั่น Thunder', '0810421002', NULL, 'Nail Artist', 42, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(127, 'เมฆา Cloud', '0810421003', NULL, 'Cashier', 42, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(128, 'รักชาติ Patriot', '0810431001', NULL, 'Nail Artist', 43, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(129, 'สายรุ้ง Rainbow', '0810431002', NULL, 'Spa Therapist', 43, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(130, 'ทอฝัน Dreamer', '0810431003', NULL, 'Receptionist', 43, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(131, 'อุ้มบุญ Merit', '0810441001', NULL, 'Nail Artist', 44, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(132, 'วรพจน์ Word', '0810441002', NULL, 'Nail Artist', 44, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(133, 'โฉมฉาย Beauty', '0810441003', NULL, 'Cashier', 44, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(134, 'กึกก้อง Loud', '0810451001', NULL, 'Nail Artist', 45, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(135, 'จันทร์เจ้า Moon-Girl', '0810451002', NULL, 'Spa Therapist', 45, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(136, 'ดาวเด่น Celeb', '0810451003', NULL, 'Receptionist', 45, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(137, 'พริ้งพราว Proud', '0810461001', NULL, 'Nail Artist', 46, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(138, 'แวววาว Shiny', '0810461002', NULL, 'Spa Therapist', 46, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(139, 'กังวาน Ring', '0810461003', NULL, 'Receptionist', 46, '2026-01-18 05:11:04', '2026-01-18 05:11:04', NULL),
(140, 'Kitty', '0646785822', 'dsfgfb@gmail.com', 'ทาสี', 2, '2026-02-25 01:51:25', '2026-02-25 01:51:52', '2026-02-25 01:51:52');

-- --------------------------------------------------------

--
-- Table structure for table `favorite`
--

CREATE TABLE IF NOT EXISTS `favorite` (
  `favorite_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `store_id` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `favorite`
--

INSERT INTO `favorite` (`favorite_id`, `user_id`, `store_id`, `created_at`, `updated_at`) VALUES
(1, 1, 1, '2025-12-10 13:40:47', NULL),
(2, 2, 1, '2025-12-10 13:40:47', NULL),
(3, 3, 2, '2025-12-10 13:40:47', NULL),
(4, 4, 3, '2025-12-10 13:40:47', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `payment`
--

CREATE TABLE IF NOT EXISTS `payment` (
  `payment_id` int(11) NOT NULL,
  `method` varchar(200) DEFAULT NULL,
  `payment_date` varchar(200) DEFAULT NULL,
  `amount` float DEFAULT NULL,
  `booking_id` int(11) DEFAULT NULL,
  `bill_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `payment`
--

INSERT INTO `payment` (`payment_id`, `method`, `payment_date`, `amount`, `booking_id`, `bill_id`) VALUES
(1, 'cash', '2025-01-10', 450, 1, 1),
(2, 'credit_card', '2025-01-10', 900, 2, 2),
(3, 'qr_payment', '2025-01-11', 1200, 4, 3),
(4, 'cash', '2025-01-11', 800, 5, 4),
(5, 'credit_card', '2025-01-12', 650, 6, 5);

-- --------------------------------------------------------

--
-- Table structure for table `permission`
--

CREATE TABLE IF NOT EXISTS `permission` (
  `permission_id` int(11) NOT NULL,
  `code` varchar(200) DEFAULT NULL,
  `name` varchar(200) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `permission`
--

INSERT INTO `permission` (`permission_id`, `code`, `name`, `created_at`, `updated_at`) VALUES
(1, 'USER_VIEW', 'View User List', '2025-12-10 13:30:43', NULL),
(2, 'USER_EDIT', 'Edit User', '2025-12-10 13:30:43', NULL),
(3, 'STORE_MANAGE', 'Manage Store', '2025-12-10 13:30:43', NULL),
(4, 'BOOKING_MANAGE', 'Manage Booking', '2025-12-10 13:30:43', NULL),
(5, 'PAYMENT_VIEW', 'View Payments', '2025-12-10 13:30:43', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `promotion`
--

CREATE TABLE IF NOT EXISTS `promotion` (
  `promo_id` int(11) NOT NULL,
  `name` varchar(200) DEFAULT NULL,
  `discount` float DEFAULT NULL,
  `store_id` int(11) DEFAULT NULL,
  `type_promo_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `promotion`
--

INSERT INTO `promotion` (`promo_id`, `name`, `discount`, `store_id`, `type_promo_id`) VALUES
(1, 'New Year Sale', 10, 1, 1),
(2, 'Spa Combo Discount', 15, 2, 1),
(3, 'Happy Hour Promo', 100, 3, 2);

-- --------------------------------------------------------

--
-- Table structure for table `review`
--

CREATE TABLE IF NOT EXISTS `review` (
  `review_id` int(11) NOT NULL,
  `rating` int(11) DEFAULT NULL,
  `comment` varchar(300) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `store_id` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `review`
--

INSERT INTO `review` (`review_id`, `rating`, `comment`, `user_id`, `store_id`, `created_at`) VALUES
(1, 5, 'บริการดีมาก ทำเล็บสวยค่ะ', 1, 1, '2025-12-10 13:38:19'),
(2, 4, 'งานละเอียด พนักงานน่ารัก', 2, 1, '2025-12-10 13:38:19'),
(3, 3, 'ดีค่ะ แต่รอนานนิดนึง', 3, 1, '2025-12-10 13:38:19'),
(4, 5, 'ประทับใจมากค่ะ', 4, 2, '2025-12-10 13:38:19'),
(5, 4, 'สีสวย ทนดีค่ะ', 5, 2, '2025-12-10 13:38:19'),
(6, 5, 'บริการเยี่ยม', 6, 3, '2025-12-10 13:38:19'),
(7, 5, 'งานดีแบบสุดๆ', 7, 3, '2025-12-10 13:38:19'),
(8, 4, 'โอเคเลยค่ะ', 8, 3, '2025-12-10 13:38:19'),
(9, 3, 'เฉยๆ ค่ะ', 9, 2, '2025-12-10 13:38:19'),
(10, 5, 'แนะนำเลยค่ะร้านนี้', 10, 1, '2025-12-10 13:38:19'),
(11, 5, 'บริการดีมาก ประทับใจสุดๆ', 1, 1, '2026-01-07 20:45:48'),
(12, 4, 'ช่างสุภาพ งานเรียบร้อย', 2, 1, '2026-01-07 20:45:48'),
(13, 3, 'งานโอเค แต่รอนานนิดนึง', 3, 1, '2026-01-07 20:45:48'),
(14, 5, 'ร้านสะอาดมาก', 4, 2, '2026-01-07 20:45:48'),
(15, 4, 'สีเล็บสวยตรงเรฟ', 5, 2, '2026-01-07 20:45:48'),
(16, 5, 'ประทับใจมาก จะกลับมาอีก', 6, 2, '2026-01-07 20:45:48'),
(17, 2, 'รอคิวนานไปหน่อย', 7, 3, '2026-01-07 20:45:48'),
(18, 3, 'งานโอเคตามราคา', 8, 3, '2026-01-07 20:45:48'),
(19, 4, 'พนักงานบริการดี', 9, 3, '2026-01-07 20:45:48'),
(20, 5, 'ช่างมืออาชีพมาก', 10, 1, '2026-01-07 20:45:48'),
(21, 4, 'ลายเล็บสวย', 1, 1, '2026-01-07 20:45:48'),
(22, 5, 'บริการเร็วทันใจ', 2, 1, '2026-01-07 20:45:48'),
(23, 3, 'ราคาค่อนข้างสูง', 3, 2, '2026-01-07 20:45:48'),
(24, 4, 'คุณภาพดี', 4, 2, '2026-01-07 20:45:48'),
(25, 5, 'ประทับใจตั้งแต่ครั้งแรก', 5, 2, '2026-01-07 20:45:48'),
(26, 4, 'ร้านน่ารัก บรรยากาศดี', 6, 3, '2026-01-07 20:45:48'),
(27, 5, 'แนะนำร้านนี้เลย', 7, 3, '2026-01-07 20:45:48'),
(28, 3, 'งานโอเค แต่สีหลุดเร็ว', 8, 3, '2026-01-07 20:45:48'),
(29, 5, 'ช่างใส่ใจรายละเอียด', 9, 1, '2026-01-07 20:45:48'),
(30, 4, 'โดยรวมดีมาก', 10, 1, '2026-01-07 20:45:48'),
(31, 5, 'ทำเล็บสวยมาก', 1, 1, '2026-01-07 20:45:48'),
(32, 2, 'ไม่ค่อยประทับใจ', 2, 2, '2026-01-07 20:45:48'),
(33, 3, 'กลางๆ', 3, 2, '2026-01-07 20:45:48'),
(34, 4, 'โอเคเลย', 4, 2, '2026-01-07 20:45:48'),
(35, 5, 'ดีที่สุดที่เคยทำมา', 5, 3, '2026-01-07 20:45:48'),
(36, 4, 'งานละเอียด', 6, 3, '2026-01-07 20:45:48'),
(37, 5, 'ช่างน่ารักมาก', 7, 3, '2026-01-07 20:45:48'),
(38, 3, 'รอคิวนาน', 8, 1, '2026-01-07 20:45:48'),
(39, 4, 'โอเคเลย', 9, 1, '2026-01-07 20:45:48'),
(40, 5, 'ประทับใจสุด', 10, 1, '2026-01-07 20:45:48'),
(41, 4, 'สีสวย งานดี', 1, 2, '2026-01-07 20:45:48'),
(42, 5, 'จะมาใช้บริการอีก', 2, 2, '2026-01-07 20:45:48'),
(43, 3, 'งานพอใช้ได้', 3, 2, '2026-01-07 20:45:48'),
(44, 4, 'บริการดีตามมาตรฐาน', 4, 3, '2026-01-07 20:45:48'),
(45, 5, 'ร้านประจำไปแล้ว', 5, 3, '2026-01-07 20:45:48'),
(46, 4, 'ช่างเก่งมาก', 6, 3, '2026-01-07 20:45:48'),
(119, 4, 'ประทับใจ จะกลับมาอีก', 2, 1, '2026-01-10 22:12:46'),
(120, 5, 'ร้านสะอาด บรรยากาศดี', 8, 1, '2026-01-10 22:12:46'),
(121, 5, 'พนักงานสุภาพ งานละเอียด', 7, 1, '2026-01-10 22:12:46'),
(122, 3, 'พนักงานสุภาพ งานละเอียด', 7, 2, '2026-01-10 22:12:46'),
(123, 3, 'ร้านสะอาด บรรยากาศดี', 10, 2, '2026-01-10 22:12:46'),
(124, 4, 'ร้านสะอาด บรรยากาศดี', 7, 2, '2026-01-10 22:12:46'),
(125, 3, 'สีสวยตรงเรฟ', 4, 3, '2026-01-10 22:12:46'),
(126, 4, 'ประทับใจ จะกลับมาอีก', 10, 3, '2026-01-10 22:12:46'),
(127, 4, 'บริการดีมาก', 10, 3, '2026-01-10 22:12:46'),
(128, 5, 'สีสวยตรงเรฟ', 7, 4, '2026-01-10 22:12:46'),
(129, 3, 'ร้านสะอาด บรรยากาศดี', 8, 4, '2026-01-10 22:12:46'),
(130, 4, 'พนักงานสุภาพ งานละเอียด', 9, 4, '2026-01-10 22:12:46'),
(131, 3, 'บริการดีมาก', 6, 5, '2026-01-10 22:12:46'),
(132, 4, 'พนักงานสุภาพ งานละเอียด', 4, 5, '2026-01-10 22:12:46'),
(133, 5, 'ร้านสะอาด บรรยากาศดี', 6, 5, '2026-01-10 22:12:46'),
(134, 4, 'ร้านสะอาด บรรยากาศดี', 3, 6, '2026-01-10 22:12:46'),
(135, 5, 'สีสวยตรงเรฟ', 8, 6, '2026-01-10 22:12:46'),
(136, 4, 'ร้านสะอาด บรรยากาศดี', 10, 6, '2026-01-10 22:12:46'),
(137, 3, 'สีสวยตรงเรฟ', 1, 7, '2026-01-10 22:12:46'),
(138, 4, 'สีสวยตรงเรฟ', 4, 7, '2026-01-10 22:12:46'),
(139, 5, 'ร้านสะอาด บรรยากาศดี', 8, 7, '2026-01-10 22:12:46'),
(140, 5, 'สีสวยตรงเรฟ', 6, 8, '2026-01-10 22:12:46'),
(141, 4, 'ร้านสะอาด บรรยากาศดี', 8, 8, '2026-01-10 22:12:46'),
(142, 3, 'บริการดีมาก', 8, 8, '2026-01-10 22:12:46'),
(143, 3, 'บริการดีมาก', 8, 9, '2026-01-10 22:12:46'),
(144, 4, 'ร้านสะอาด บรรยากาศดี', 6, 9, '2026-01-10 22:12:46'),
(145, 4, 'ประทับใจ จะกลับมาอีก', 6, 9, '2026-01-10 22:12:46'),
(146, 3, 'พนักงานสุภาพ งานละเอียด', 3, 10, '2026-01-10 22:12:46'),
(147, 3, 'ร้านสะอาด บรรยากาศดี', 4, 10, '2026-01-10 22:12:46'),
(148, 5, 'พนักงานสุภาพ งานละเอียด', 8, 10, '2026-01-10 22:12:46'),
(149, 4, 'ร้านสะอาด บรรยากาศดี', 10, 11, '2026-01-10 22:12:46'),
(150, 3, 'ร้านสะอาด บรรยากาศดี', 5, 11, '2026-01-10 22:12:46'),
(151, 5, 'สีสวยตรงเรฟ', 2, 11, '2026-01-10 22:12:46'),
(152, 4, 'พนักงานสุภาพ งานละเอียด', 8, 12, '2026-01-10 22:12:46'),
(153, 3, 'ประทับใจ จะกลับมาอีก', 4, 12, '2026-01-10 22:12:46'),
(154, 5, 'ร้านสะอาด บรรยากาศดี', 3, 12, '2026-01-10 22:12:46'),
(155, 3, 'ประทับใจ จะกลับมาอีก', 5, 13, '2026-01-10 22:12:46'),
(156, 4, 'พนักงานสุภาพ งานละเอียด', 7, 13, '2026-01-10 22:12:46'),
(157, 4, 'ประทับใจ จะกลับมาอีก', 8, 13, '2026-01-10 22:12:46'),
(158, 3, 'ร้านสะอาด บรรยากาศดี', 2, 14, '2026-01-10 22:12:46'),
(159, 4, 'พนักงานสุภาพ งานละเอียด', 1, 14, '2026-01-10 22:12:46'),
(160, 5, 'พนักงานสุภาพ งานละเอียด', 1, 14, '2026-01-10 22:12:46'),
(161, 5, 'พนักงานสุภาพ งานละเอียด', 8, 15, '2026-01-10 22:12:46'),
(162, 5, 'พนักงานสุภาพ งานละเอียด', 5, 15, '2026-01-10 22:12:46'),
(163, 3, 'ประทับใจ จะกลับมาอีก', 10, 15, '2026-01-10 22:12:46'),
(164, 5, 'พนักงานสุภาพ งานละเอียด', 10, 16, '2026-01-10 22:12:46'),
(165, 5, 'ประทับใจ จะกลับมาอีก', 7, 16, '2026-01-10 22:12:46'),
(166, 4, 'ประทับใจ จะกลับมาอีก', 7, 16, '2026-01-10 22:12:46'),
(167, 5, 'ประทับใจ จะกลับมาอีก', 10, 17, '2026-01-10 22:12:46'),
(168, 4, 'สีสวยตรงเรฟ', 7, 17, '2026-01-10 22:12:46'),
(169, 3, 'บริการดีมาก', 5, 17, '2026-01-10 22:12:46'),
(170, 5, 'สีสวยตรงเรฟ', 1, 18, '2026-01-10 22:12:46'),
(171, 4, 'พนักงานสุภาพ งานละเอียด', 2, 18, '2026-01-10 22:12:46'),
(172, 5, 'บริการดีมาก', 1, 18, '2026-01-10 22:12:46'),
(173, 3, 'พนักงานสุภาพ งานละเอียด', 8, 19, '2026-01-10 22:12:46'),
(174, 5, 'พนักงานสุภาพ งานละเอียด', 2, 19, '2026-01-10 22:12:46'),
(175, 3, 'ร้านสะอาด บรรยากาศดี', 10, 19, '2026-01-10 22:12:46'),
(176, 5, 'ประทับใจ จะกลับมาอีก', 8, 20, '2026-01-10 22:12:46'),
(177, 5, 'ประทับใจ จะกลับมาอีก', 1, 20, '2026-01-10 22:12:46'),
(178, 5, 'บริการดีมาก', 10, 20, '2026-01-10 22:12:46'),
(179, 5, 'บริการดีมาก', 9, 21, '2026-01-10 22:12:46'),
(180, 5, 'บริการดีมาก', 8, 21, '2026-01-10 22:12:46'),
(181, 3, 'ประทับใจ จะกลับมาอีก', 6, 21, '2026-01-10 22:12:46'),
(182, 3, 'บริการดีมาก', 9, 22, '2026-01-10 22:12:46'),
(183, 3, 'พนักงานสุภาพ งานละเอียด', 8, 22, '2026-01-10 22:12:46'),
(184, 5, 'ประทับใจ จะกลับมาอีก', 4, 22, '2026-01-10 22:12:46'),
(185, 3, 'บริการดีมาก', 3, 23, '2026-01-10 22:12:46'),
(186, 3, 'ร้านสะอาด บรรยากาศดี', 2, 23, '2026-01-10 22:12:46'),
(187, 4, 'สีสวยตรงเรฟ', 9, 23, '2026-01-10 22:12:46'),
(188, 3, 'ประทับใจ จะกลับมาอีก', 8, 24, '2026-01-10 22:12:46'),
(189, 5, 'พนักงานสุภาพ งานละเอียด', 7, 24, '2026-01-10 22:12:46'),
(190, 4, 'พนักงานสุภาพ งานละเอียด', 1, 24, '2026-01-10 22:12:46'),
(191, 4, 'พนักงานสุภาพ งานละเอียด', 9, 25, '2026-01-10 22:12:46'),
(192, 4, 'พนักงานสุภาพ งานละเอียด', 2, 25, '2026-01-10 22:12:46'),
(193, 5, 'บริการดีมาก', 5, 25, '2026-01-10 22:12:46'),
(194, 4, 'พนักงานสุภาพ งานละเอียด', 8, 26, '2026-01-10 22:12:46'),
(195, 4, 'บริการดีมาก', 1, 26, '2026-01-10 22:12:46'),
(196, 5, 'ร้านสะอาด บรรยากาศดี', 5, 26, '2026-01-10 22:12:46'),
(197, 3, 'สีสวยตรงเรฟ', 3, 27, '2026-01-10 22:12:46'),
(198, 3, 'พนักงานสุภาพ งานละเอียด', 1, 27, '2026-01-10 22:12:46'),
(199, 3, 'พนักงานสุภาพ งานละเอียด', 4, 27, '2026-01-10 22:12:46'),
(200, 5, 'ร้านสะอาด บรรยากาศดี', 1, 28, '2026-01-10 22:12:46'),
(201, 3, 'ร้านสะอาด บรรยากาศดี', 10, 28, '2026-01-10 22:12:46'),
(202, 3, 'สีสวยตรงเรฟ', 3, 28, '2026-01-10 22:12:46'),
(203, 3, 'ร้านสะอาด บรรยากาศดี', 10, 29, '2026-01-10 22:12:46'),
(204, 4, 'พนักงานสุภาพ งานละเอียด', 4, 29, '2026-01-10 22:12:46'),
(205, 5, 'ประทับใจ จะกลับมาอีก', 6, 29, '2026-01-10 22:12:46'),
(206, 5, 'บริการดีมาก', 8, 30, '2026-01-10 22:12:46'),
(207, 4, 'พนักงานสุภาพ งานละเอียด', 4, 30, '2026-01-10 22:12:46'),
(208, 4, 'สีสวยตรงเรฟ', 8, 30, '2026-01-10 22:12:46'),
(209, 5, 'ประทับใจ จะกลับมาอีก', 3, 31, '2026-01-10 22:12:46'),
(210, 3, 'พนักงานสุภาพ งานละเอียด', 1, 31, '2026-01-10 22:12:46'),
(211, 3, 'ร้านสะอาด บรรยากาศดี', 4, 31, '2026-01-10 22:12:46'),
(212, 3, 'ประทับใจ จะกลับมาอีก', 8, 32, '2026-01-10 22:12:46'),
(213, 3, 'บริการดีมาก', 8, 32, '2026-01-10 22:12:46'),
(214, 4, 'พนักงานสุภาพ งานละเอียด', 4, 32, '2026-01-10 22:12:46'),
(215, 4, 'ประทับใจ จะกลับมาอีก', 4, 33, '2026-01-10 22:12:46'),
(216, 3, 'สีสวยตรงเรฟ', 9, 33, '2026-01-10 22:12:46'),
(217, 4, 'ร้านสะอาด บรรยากาศดี', 3, 33, '2026-01-10 22:12:46'),
(218, 5, 'สีสวยตรงเรฟ', 9, 34, '2026-01-10 22:12:46'),
(219, 3, 'ร้านสะอาด บรรยากาศดี', 1, 34, '2026-01-10 22:12:46'),
(220, 4, 'บริการดีมาก', 10, 34, '2026-01-10 22:12:46'),
(221, 5, 'ประทับใจ จะกลับมาอีก', 4, 35, '2026-01-10 22:12:46'),
(222, 5, 'พนักงานสุภาพ งานละเอียด', 2, 35, '2026-01-10 22:12:46'),
(223, 5, 'สีสวยตรงเรฟ', 8, 35, '2026-01-10 22:12:46'),
(224, 4, 'บริการดีมาก', 4, 36, '2026-01-10 22:12:46'),
(225, 4, 'ประทับใจ จะกลับมาอีก', 10, 36, '2026-01-10 22:12:46'),
(226, 5, 'ร้านสะอาด บรรยากาศดี', 2, 36, '2026-01-10 22:12:46'),
(227, 5, 'ร้านสะอาด บรรยากาศดี', 9, 37, '2026-01-10 22:12:46'),
(228, 4, 'ประทับใจ จะกลับมาอีก', 3, 37, '2026-01-10 22:12:46'),
(229, 4, 'บริการดีมาก', 6, 37, '2026-01-10 22:12:46'),
(230, 5, 'สีสวยตรงเรฟ', 8, 38, '2026-01-10 22:12:46'),
(231, 3, 'พนักงานสุภาพ งานละเอียด', 9, 38, '2026-01-10 22:12:46'),
(232, 4, 'บริการดีมาก', 5, 38, '2026-01-10 22:12:46'),
(233, 5, 'ร้านสะอาด บรรยากาศดี', 8, 39, '2026-01-10 22:12:46'),
(234, 3, 'สีสวยตรงเรฟ', 3, 39, '2026-01-10 22:12:46'),
(235, 3, 'ร้านสะอาด บรรยากาศดี', 7, 39, '2026-01-10 22:12:46'),
(236, 4, 'บริการดีมาก', 7, 40, '2026-01-10 22:12:46'),
(237, 3, 'บริการดีมาก', 7, 40, '2026-01-10 22:12:46'),
(238, 5, 'สีสวยตรงเรฟ', 8, 40, '2026-01-10 22:12:46'),
(239, 5, 'ร้านสะอาด บรรยากาศดี', 4, 41, '2026-01-10 22:12:46'),
(240, 3, 'ร้านสะอาด บรรยากาศดี', 10, 41, '2026-01-10 22:12:46'),
(241, 4, 'พนักงานสุภาพ งานละเอียด', 7, 41, '2026-01-10 22:12:46'),
(242, 5, 'ร้านสะอาด บรรยากาศดี', 6, 42, '2026-01-10 22:12:46'),
(243, 5, 'สีสวยตรงเรฟ', 3, 42, '2026-01-10 22:12:46'),
(244, 3, 'ร้านสะอาด บรรยากาศดี', 1, 42, '2026-01-10 22:12:46'),
(245, 4, 'สีสวยตรงเรฟ', 9, 43, '2026-01-10 22:12:46'),
(246, 3, 'ประทับใจ จะกลับมาอีก', 2, 43, '2026-01-10 22:12:46'),
(247, 3, 'ประทับใจ จะกลับมาอีก', 9, 43, '2026-01-10 22:12:46'),
(248, 4, 'สีสวยตรงเรฟ', 9, 44, '2026-01-10 22:12:46'),
(249, 4, 'สีสวยตรงเรฟ', 6, 44, '2026-01-10 22:12:46'),
(250, 3, 'พนักงานสุภาพ งานละเอียด', 3, 44, '2026-01-10 22:12:46'),
(251, 3, 'สีสวยตรงเรฟ', 4, 45, '2026-01-10 22:12:46'),
(252, 5, 'พนักงานสุภาพ งานละเอียด', 3, 45, '2026-01-10 22:12:46'),
(253, 3, 'ร้านสะอาด บรรยากาศดี', 5, 45, '2026-01-10 22:12:46'),
(254, 5, 'พนักงานสุภาพ งานละเอียด', 4, 46, '2026-01-10 22:12:46'),
(255, 3, 'ประทับใจ จะกลับมาอีก', 2, 46, '2026-01-10 22:12:46'),
(256, 4, 'ร้านสะอาด บรรยากาศดี', 1, 46, '2026-01-10 22:12:46');

-- --------------------------------------------------------

--
-- Table structure for table `role`
--

CREATE TABLE IF NOT EXISTS `role` (
  `role_id` int(11) NOT NULL,
  `role_name` varchar(200) NOT NULL,
  `description` varchar(200) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `role`
--

INSERT INTO `role` (`role_id`, `role_name`, `description`, `created_at`) VALUES
(1, 'User', 'ผู้ใช้ทั่วไป ใช้งานระบบทั่วไป เช่น จองคิว', '2025-12-03 13:35:28'),
(2, 'Shop Owner', 'เจ้าของร้าน จัดการร้านและข้อมูลสำคัญ', '2025-12-03 13:35:28'),
(3, 'Staff', 'พนักงานร้าน ช่วยงานและบริการลูกค้า', '2025-12-03 13:35:28'),
(4, 'Admin', 'ผู้ดูแลระบบ มีสิทธิ์จัดการทุกส่วน', '2025-12-03 13:35:28');

-- --------------------------------------------------------

--
-- Table structure for table `role_permission`
--

CREATE TABLE IF NOT EXISTS `role_permission` (
  `role_permission_id` int(11) NOT NULL,
  `permission_id` int(11) DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `role_permission`
--

INSERT INTO `role_permission` (`role_permission_id`, `permission_id`, `role_id`, `created_at`, `updated_at`) VALUES
(1, 1, 1, '2025-12-10 13:43:16', NULL),
(2, 2, 1, '2025-12-10 13:43:16', NULL),
(3, 3, 1, '2025-12-10 13:43:16', NULL),
(4, 4, 1, '2025-12-10 13:43:16', NULL),
(5, 5, 1, '2025-12-10 13:43:16', NULL),
(6, 1, 2, '2025-12-10 13:43:16', NULL),
(7, 4, 2, '2025-12-10 13:43:16', NULL),
(8, 5, 2, '2025-12-10 13:43:16', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `service`
--

CREATE TABLE IF NOT EXISTS `service` (
  `service_id` int(11) NOT NULL,
  `service_name` varchar(200) DEFAULT NULL,
  `price` float DEFAULT NULL,
  `duration_minutes` int(11) DEFAULT NULL,
  `description` varchar(200) DEFAULT NULL,
  `type_id` int(11) DEFAULT NULL,
  `store_id` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `service`
--

INSERT INTO `service` (`service_id`, `service_name`, `price`, `duration_minutes`, `description`, `type_id`, `store_id`, `created_at`) VALUES
(1, 'ฟหกอ่ีัะพำกแอ่', 250, 30, '', 1, 1, '2026-02-18 14:14:38'),
(2, 'Gel Polish Hands', 450, 45, 'Gel polish single color', 3, 1, '2026-02-18 14:14:38'),
(3, 'Gel Art Premium', 900, 60, 'Premium nail art', 3, 1, '2026-02-18 14:14:38'),
(4, 'Spa deemak', 599, 50, '', 1, 1, '2026-02-18 14:14:38'),
(5, 'Basic Pedicure', 300, 30, 'Pedicure cleaning', 2, 2, '2026-02-18 14:14:38'),
(6, 'Gel Polish Feet', 500, 45, 'Gel polish for feet', 3, 2, '2026-02-18 14:14:38'),
(7, 'Foot Spa Deluxe', 800, 60, '', 1, 2, '2026-02-18 14:14:38'),
(8, 'Combo Gel Hand + Foot', 1200, 90, 'Gel hand and foot combo', 3, 3, '2026-02-18 14:14:38'),
(9, 'Acrylic Extension', 1500, 90, 'Acrylic nail extension', 3, 3, '2026-02-18 14:14:38'),
(10, 'Nail Repair', 150, 15, 'Fix broken nail', 1, 3, '2026-02-18 14:14:38'),
(11, 'Callus Treatment', 400, 30, 'Foot skin softening', 2, 4, '2026-02-18 14:14:38'),
(12, 'Gel Polish Hands', 450, 45, 'Gel polish single color', 3, 4, '2026-02-18 14:14:38'),
(13, 'Basic Manicure', 250, 30, 'Basic cleaning and trimming', 1, 4, '2026-02-18 14:14:38'),
(14, 'Gel Removal', 150, 20, 'Professional gel removal', 3, 4, '2026-02-18 14:14:38'),
(15, 'Organic Scrub', 450, 25, 'Natural salt and oil scrub', 4, 4, '2026-02-18 14:14:38'),
(16, 'Nail Art Premium', 900, 60, 'Custom hand-painted designs', 3, 4, '2026-02-18 14:14:38'),
(17, 'Organic Scrub', 450, 25, 'Natural salt and oil scrub', 4, 5, '2026-02-18 14:14:38'),
(18, 'Acrylic Extension', 1500, 90, 'Full set acrylic extension', 3, 5, '2026-02-18 14:14:38'),
(19, 'Gel Removal', 150, 20, 'Professional gel removal', 3, 5, '2026-02-18 14:14:38'),
(20, 'Callus Treatment', 400, 30, 'Foot skin softening', 2, 5, '2026-02-18 14:14:38'),
(21, 'Hand Massage', 300, 20, 'Relaxing hand massage with oil', 4, 5, '2026-02-18 14:14:38'),
(22, 'Basic Manicure', 250, 30, 'Basic cleaning and trimming', 1, 5, '2026-02-18 14:14:38'),
(23, 'Gel Polish Hands', 450, 45, 'Gel polish single color', 3, 6, '2026-02-18 14:14:38'),
(24, 'French Manicure', 350, 45, 'Classic white tip style', 3, 6, '2026-02-18 14:14:38'),
(25, 'Nail Repair', 100, 15, 'Fix broken or chipped nail', 1, 6, '2026-02-18 14:14:38'),
(26, 'Basic Manicure', 250, 30, 'Basic cleaning and trimming', 1, 6, '2026-02-18 14:14:38'),
(27, 'Acrylic Extension', 1500, 90, 'Full set acrylic extension', 3, 6, '2026-02-18 14:14:38'),
(28, 'Paraffin Wax', 550, 40, 'Deep moisturizing treatment', 4, 6, '2026-02-18 14:14:38'),
(29, 'Acrylic Extension', 1500, 90, 'Full set acrylic extension', 3, 7, '2026-02-18 14:14:38'),
(30, 'Basic Manicure', 250, 30, 'Basic cleaning and trimming', 1, 7, '2026-02-18 14:14:38'),
(31, 'Organic Scrub', 450, 25, 'Natural salt and oil scrub', 4, 7, '2026-02-18 14:14:38'),
(32, 'Hand Massage', 300, 20, 'Relaxing hand massage with oil', 4, 7, '2026-02-18 14:14:38'),
(33, 'Nail Art Premium', 900, 60, 'Custom hand-painted designs', 3, 7, '2026-02-18 14:14:38'),
(34, 'Paraffin Wax', 550, 40, 'Deep moisturizing treatment', 4, 7, '2026-02-18 14:14:38'),
(35, 'Spa Pedicure', 600, 60, 'Full foot spa and pedicure', 2, 8, '2026-02-18 14:14:38'),
(36, 'Hand Massage', 300, 20, 'Relaxing hand massage with oil', 4, 8, '2026-02-18 14:14:38'),
(37, 'Paraffin Wax', 550, 40, 'Deep moisturizing treatment', 4, 8, '2026-02-18 14:14:38'),
(38, 'Nail Art Premium', 900, 60, 'Custom hand-painted designs', 3, 8, '2026-02-18 14:14:38'),
(39, 'Acrylic Extension', 1500, 90, 'Full set acrylic extension', 3, 8, '2026-02-18 14:14:38'),
(40, 'Basic Manicure', 250, 30, 'Basic cleaning and trimming', 1, 8, '2026-02-18 14:14:38'),
(41, 'Nail Art Premium', 900, 60, 'Custom hand-painted designs', 3, 9, '2026-02-18 14:14:38'),
(42, 'Gel Removal', 150, 20, 'Professional gel removal', 3, 9, '2026-02-18 14:14:38'),
(43, 'Basic Manicure', 250, 30, 'Basic cleaning and trimming', 1, 9, '2026-02-18 14:14:38'),
(44, 'Gel Polish Hands', 450, 45, 'Gel polish single color', 3, 9, '2026-02-18 14:14:38'),
(45, 'Organic Scrub', 450, 25, 'Natural salt and oil scrub', 4, 9, '2026-02-18 14:14:38'),
(46, 'Acrylic Extension', 1500, 90, 'Full set acrylic extension', 3, 9, '2026-02-18 14:14:38'),
(47, 'Hand Massage', 300, 20, 'Relaxing hand massage with oil', 4, 10, '2026-02-18 14:14:38'),
(48, 'Gel Polish Hands', 450, 45, 'Gel polish single color', 3, 10, '2026-02-18 14:14:38'),
(49, 'Paraffin Wax', 550, 40, 'Deep moisturizing treatment', 4, 10, '2026-02-18 14:14:38'),
(50, 'Spa Pedicure', 600, 60, 'Full foot spa and pedicure', 2, 10, '2026-02-18 14:14:38'),
(51, 'Basic Manicure', 250, 30, 'Basic cleaning and trimming', 1, 10, '2026-02-18 14:14:38'),
(52, 'Gel Removal', 150, 20, 'Professional gel removal', 3, 10, '2026-02-18 14:14:38'),
(53, 'Gel Polish Hands', 450, 45, 'Gel polish single color', 3, 11, '2026-02-18 14:14:38'),
(54, 'Spa Pedicure', 600, 60, 'Full foot spa and pedicure', 2, 11, '2026-02-18 14:14:38'),
(55, 'Callus Treatment', 400, 30, 'Foot skin softening', 2, 11, '2026-02-18 14:14:38'),
(56, 'Basic Manicure', 250, 30, 'Basic cleaning and trimming', 1, 11, '2026-02-18 14:14:38'),
(57, 'Hand Massage', 300, 20, 'Relaxing hand massage with oil', 4, 11, '2026-02-18 14:14:38'),
(58, 'Paraffin Wax', 550, 40, 'Deep moisturizing treatment', 4, 11, '2026-02-18 14:14:38'),
(59, 'French Manicure', 350, 45, 'Classic white tip style', 3, 12, '2026-02-18 14:14:38'),
(60, 'Gel Removal', 150, 20, 'Professional gel removal', 3, 12, '2026-02-18 14:14:38'),
(61, 'Spa Pedicure', 600, 60, 'Full foot spa and pedicure', 2, 12, '2026-02-18 14:14:38'),
(62, 'Acrylic Extension', 1500, 90, 'Full set acrylic extension', 3, 12, '2026-02-18 14:14:38'),
(63, 'Nail Art Premium', 900, 60, 'Custom hand-painted designs', 3, 12, '2026-02-18 14:14:38'),
(64, 'Nail Repair', 100, 15, 'Fix broken or chipped nail', 1, 12, '2026-02-18 14:14:38'),
(65, 'Gel Removal', 150, 20, 'Professional gel removal', 3, 13, '2026-02-18 14:14:38'),
(66, 'Nail Art Premium', 900, 60, 'Custom hand-painted designs', 3, 13, '2026-02-18 14:14:38'),
(67, 'Callus Treatment', 400, 30, 'Foot skin softening', 2, 13, '2026-02-18 14:14:38'),
(68, 'Nail Repair', 100, 15, 'Fix broken or chipped nail', 1, 13, '2026-02-18 14:14:38'),
(69, 'Acrylic Extension', 1500, 90, 'Full set acrylic extension', 3, 13, '2026-02-18 14:14:38'),
(70, 'Hand Massage', 300, 20, 'Relaxing hand massage with oil', 4, 13, '2026-02-18 14:14:38'),
(71, 'Nail Art Premium', 900, 60, 'Custom hand-painted designs', 3, 14, '2026-02-18 14:14:38'),
(72, 'Hand Massage', 300, 20, 'Relaxing hand massage with oil', 4, 14, '2026-02-18 14:14:38'),
(73, 'French Manicure', 350, 45, 'Classic white tip style', 3, 14, '2026-02-18 14:14:38'),
(74, 'Nail Repair', 100, 15, 'Fix broken or chipped nail', 1, 14, '2026-02-18 14:14:38'),
(75, 'Acrylic Extension', 1500, 90, 'Full set acrylic extension', 3, 14, '2026-02-18 14:14:38'),
(76, 'Organic Scrub', 450, 25, 'Natural salt and oil scrub', 4, 14, '2026-02-18 14:14:38'),
(77, 'Acrylic Extension', 1500, 90, 'Full set acrylic extension', 3, 15, '2026-02-18 14:14:38'),
(78, 'Callus Treatment', 400, 30, 'Foot skin softening', 2, 15, '2026-02-18 14:14:38'),
(79, 'Gel Polish Hands', 450, 45, 'Gel polish single color', 3, 15, '2026-02-18 14:14:38'),
(80, 'Spa Pedicure', 600, 60, 'Full foot spa and pedicure', 2, 15, '2026-02-18 14:14:38'),
(81, 'Nail Repair', 100, 15, 'Fix broken or chipped nail', 1, 15, '2026-02-18 14:14:38'),
(82, 'Organic Scrub', 450, 25, 'Natural salt and oil scrub', 4, 15, '2026-02-18 14:14:38'),
(83, 'Gel Removal', 150, 20, 'Professional gel removal', 3, 16, '2026-02-18 14:14:38'),
(84, 'Callus Treatment', 400, 30, 'Foot skin softening', 2, 16, '2026-02-18 14:14:38'),
(85, 'Gel Polish Hands', 450, 45, 'Gel polish single color', 3, 16, '2026-02-18 14:14:38'),
(86, 'Paraffin Wax', 550, 40, 'Deep moisturizing treatment', 4, 16, '2026-02-18 14:14:38'),
(87, 'Basic Manicure', 250, 30, 'Basic cleaning and trimming', 1, 16, '2026-02-18 14:14:38'),
(88, 'Acrylic Extension', 1500, 90, 'Full set acrylic extension', 3, 16, '2026-02-18 14:14:38'),
(89, 'Nail Art Premium', 900, 60, 'Custom hand-painted designs', 3, 17, '2026-02-18 14:14:38'),
(90, 'Nail Repair', 100, 15, 'Fix broken or chipped nail', 1, 17, '2026-02-18 14:14:38'),
(91, 'Basic Manicure', 250, 30, 'Basic cleaning and trimming', 1, 17, '2026-02-18 14:14:38'),
(92, 'Callus Treatment', 400, 30, 'Foot skin softening', 2, 17, '2026-02-18 14:14:38'),
(93, 'Spa Pedicure', 600, 60, 'Full foot spa and pedicure', 2, 17, '2026-02-18 14:14:38'),
(94, 'Acrylic Extension', 1500, 90, 'Full set acrylic extension', 3, 17, '2026-02-18 14:14:38'),
(95, 'Paraffin Wax', 550, 40, 'Deep moisturizing treatment', 4, 18, '2026-02-18 14:14:38'),
(96, 'French Manicure', 350, 45, 'Classic white tip style', 3, 18, '2026-02-18 14:14:38'),
(97, 'Nail Art Premium', 900, 60, 'Custom hand-painted designs', 3, 18, '2026-02-18 14:14:38'),
(98, 'Acrylic Extension', 1500, 90, 'Full set acrylic extension', 3, 18, '2026-02-18 14:14:38'),
(99, 'Spa Pedicure', 600, 60, 'Full foot spa and pedicure', 2, 18, '2026-02-18 14:14:38'),
(100, 'Organic Scrub', 450, 25, 'Natural salt and oil scrub', 4, 18, '2026-02-18 14:14:38'),
(101, 'Gel Polish Hands', 450, 45, 'Gel polish single color', 3, 19, '2026-02-18 14:14:38'),
(102, 'French Manicure', 350, 45, 'Classic white tip style', 3, 19, '2026-02-18 14:14:38'),
(103, 'Acrylic Extension', 1500, 90, 'Full set acrylic extension', 3, 19, '2026-02-18 14:14:38'),
(104, 'Gel Removal', 150, 20, 'Professional gel removal', 3, 19, '2026-02-18 14:14:38'),
(105, 'Basic Manicure', 250, 30, 'Basic cleaning and trimming', 1, 19, '2026-02-18 14:14:38'),
(106, 'Spa Pedicure', 600, 60, 'Full foot spa and pedicure', 2, 19, '2026-02-18 14:14:38'),
(107, 'Gel Removal', 150, 20, 'Professional gel removal', 3, 20, '2026-02-18 14:14:38'),
(108, 'Spa Pedicure', 600, 60, 'Full foot spa and pedicure', 2, 20, '2026-02-18 14:14:38'),
(109, 'Paraffin Wax', 550, 40, 'Deep moisturizing treatment', 4, 20, '2026-02-18 14:14:38'),
(110, 'Gel Polish Hands', 450, 45, 'Gel polish single color', 3, 20, '2026-02-18 14:14:38'),
(111, 'Nail Repair', 100, 15, 'Fix broken or chipped nail', 1, 20, '2026-02-18 14:14:38'),
(112, 'Basic Manicure', 250, 30, 'Basic cleaning and trimming', 1, 20, '2026-02-18 14:14:38'),
(113, 'Hand Massage', 300, 20, 'Relaxing hand massage with oil', 4, 21, '2026-02-18 14:14:38'),
(114, 'Organic Scrub', 450, 25, 'Natural salt and oil scrub', 4, 21, '2026-02-18 14:14:38'),
(115, 'French Manicure', 350, 45, 'Classic white tip style', 3, 21, '2026-02-18 14:14:38'),
(116, 'Callus Treatment', 400, 30, 'Foot skin softening', 2, 21, '2026-02-18 14:14:38'),
(117, 'Gel Removal', 150, 20, 'Professional gel removal', 3, 21, '2026-02-18 14:14:38'),
(118, 'Nail Repair', 100, 15, 'Fix broken or chipped nail', 1, 21, '2026-02-18 14:14:38'),
(119, 'Paraffin Wax', 550, 40, 'Deep moisturizing treatment', 4, 22, '2026-02-18 14:14:38'),
(120, 'Gel Polish Hands', 450, 45, 'Gel polish single color', 3, 22, '2026-02-18 14:14:38'),
(121, 'Acrylic Extension', 1500, 90, 'Full set acrylic extension', 3, 22, '2026-02-18 14:14:38'),
(122, 'Nail Art Premium', 900, 60, 'Custom hand-painted designs', 3, 22, '2026-02-18 14:14:38'),
(123, 'Gel Removal', 150, 20, 'Professional gel removal', 3, 22, '2026-02-18 14:14:38'),
(124, 'Nail Repair', 100, 15, 'Fix broken or chipped nail', 1, 22, '2026-02-18 14:14:38'),
(125, 'French Manicure', 350, 45, 'Classic white tip style', 3, 23, '2026-02-18 14:14:38'),
(126, 'Nail Repair', 100, 15, 'Fix broken or chipped nail', 1, 23, '2026-02-18 14:14:38'),
(127, 'Acrylic Extension', 1500, 90, 'Full set acrylic extension', 3, 23, '2026-02-18 14:14:38'),
(128, 'Gel Polish Hands', 450, 45, 'Gel polish single color', 3, 23, '2026-02-18 14:14:38'),
(129, 'Spa Pedicure', 600, 60, 'Full foot spa and pedicure', 2, 23, '2026-02-18 14:14:38'),
(130, 'Organic Scrub', 450, 25, 'Natural salt and oil scrub', 4, 23, '2026-02-18 14:14:38'),
(131, 'Hand Massage', 300, 20, 'Relaxing hand massage with oil', 4, 24, '2026-02-18 14:14:38'),
(132, 'Organic Scrub', 450, 25, 'Natural salt and oil scrub', 4, 24, '2026-02-18 14:14:38'),
(133, 'Basic Manicure', 250, 30, 'Basic cleaning and trimming', 1, 24, '2026-02-18 14:14:38'),
(134, 'Nail Repair', 100, 15, 'Fix broken or chipped nail', 1, 24, '2026-02-18 14:14:38'),
(135, 'Paraffin Wax', 550, 40, 'Deep moisturizing treatment', 4, 24, '2026-02-18 14:14:38'),
(136, 'Acrylic Extension', 1500, 90, 'Full set acrylic extension', 3, 24, '2026-02-18 14:14:38'),
(137, 'Nail Art Premium', 900, 60, 'Custom hand-painted designs', 3, 25, '2026-02-18 14:14:38'),
(138, 'Paraffin Wax', 550, 40, 'Deep moisturizing treatment', 4, 25, '2026-02-18 14:14:38'),
(139, 'French Manicure', 350, 45, 'Classic white tip style', 3, 25, '2026-02-18 14:14:38'),
(140, 'Organic Scrub', 450, 25, 'Natural salt and oil scrub', 4, 25, '2026-02-18 14:14:38'),
(141, 'Basic Manicure', 250, 30, 'Basic cleaning and trimming', 1, 25, '2026-02-18 14:14:38'),
(142, 'Callus Treatment', 400, 30, 'Foot skin softening', 2, 25, '2026-02-18 14:14:38'),
(143, 'French Manicure', 350, 45, 'Classic white tip style', 3, 26, '2026-02-18 14:14:38'),
(144, 'Spa Pedicure', 600, 60, 'Full foot spa and pedicure', 2, 26, '2026-02-18 14:14:38'),
(145, 'Gel Removal', 150, 20, 'Professional gel removal', 3, 26, '2026-02-18 14:14:38'),
(146, 'Nail Repair', 100, 15, 'Fix broken or chipped nail', 1, 26, '2026-02-18 14:14:38'),
(147, 'Nail Art Premium', 900, 60, 'Custom hand-painted designs', 3, 26, '2026-02-18 14:14:38'),
(148, 'Basic Manicure', 250, 30, 'Basic cleaning and trimming', 1, 26, '2026-02-18 14:14:38'),
(149, 'Nail Art Premium', 900, 60, 'Custom hand-painted designs', 3, 27, '2026-02-18 14:14:38'),
(150, 'Acrylic Extension', 1500, 90, 'Full set acrylic extension', 3, 27, '2026-02-18 14:14:38'),
(151, 'Paraffin Wax', 550, 40, 'Deep moisturizing treatment', 4, 27, '2026-02-18 14:14:38'),
(152, 'Organic Scrub', 450, 25, 'Natural salt and oil scrub', 4, 27, '2026-02-18 14:14:38'),
(153, 'Gel Removal', 150, 20, 'Professional gel removal', 3, 27, '2026-02-18 14:14:38'),
(154, 'Spa Pedicure', 600, 60, 'Full foot spa and pedicure', 2, 27, '2026-02-18 14:14:38'),
(155, 'Gel Polish Hands', 450, 45, 'Gel polish single color', 3, 28, '2026-02-18 14:14:38'),
(156, 'Nail Art Premium', 900, 60, 'Custom hand-painted designs', 3, 28, '2026-02-18 14:14:38'),
(157, 'Paraffin Wax', 550, 40, 'Deep moisturizing treatment', 4, 28, '2026-02-18 14:14:38'),
(158, 'French Manicure', 350, 45, 'Classic white tip style', 3, 28, '2026-02-18 14:14:38'),
(159, 'Basic Manicure', 250, 30, 'Basic cleaning and trimming', 1, 28, '2026-02-18 14:14:38'),
(160, 'Spa Pedicure', 600, 60, 'Full foot spa and pedicure', 2, 28, '2026-02-18 14:14:38'),
(161, 'Gel Removal', 150, 20, 'Professional gel removal', 3, 29, '2026-02-18 14:14:38'),
(162, 'Gel Polish Hands', 450, 45, 'Gel polish single color', 3, 29, '2026-02-18 14:14:38'),
(163, 'Basic Manicure', 250, 30, 'Basic cleaning and trimming', 1, 29, '2026-02-18 14:14:38'),
(164, 'Acrylic Extension', 1500, 90, 'Full set acrylic extension', 3, 29, '2026-02-18 14:14:38'),
(165, 'French Manicure', 350, 45, 'Classic white tip style', 3, 29, '2026-02-18 14:14:38'),
(166, 'Paraffin Wax', 550, 40, 'Deep moisturizing treatment', 4, 29, '2026-02-18 14:14:38'),
(167, 'Hand Massage', 300, 20, 'Relaxing hand massage with oil', 4, 30, '2026-02-18 14:14:38'),
(168, 'Nail Art Premium', 900, 60, 'Custom hand-painted designs', 3, 30, '2026-02-18 14:14:38'),
(169, 'Callus Treatment', 400, 30, 'Foot skin softening', 2, 30, '2026-02-18 14:14:38'),
(170, 'Gel Polish Hands', 450, 45, 'Gel polish single color', 3, 30, '2026-02-18 14:14:38'),
(171, 'French Manicure', 350, 45, 'Classic white tip style', 3, 30, '2026-02-18 14:14:38'),
(172, 'Acrylic Extension', 1500, 90, 'Full set acrylic extension', 3, 30, '2026-02-18 14:14:38'),
(173, 'Gel Polish Hands', 450, 45, 'Gel polish single color', 3, 31, '2026-02-18 14:14:38'),
(174, 'Paraffin Wax', 550, 40, 'Deep moisturizing treatment', 4, 31, '2026-02-18 14:14:38'),
(175, 'Nail Art Premium', 900, 60, 'Custom hand-painted designs', 3, 31, '2026-02-18 14:14:38'),
(176, 'Organic Scrub', 450, 25, 'Natural salt and oil scrub', 4, 31, '2026-02-18 14:14:38'),
(177, 'Gel Removal', 150, 20, 'Professional gel removal', 3, 31, '2026-02-18 14:14:38'),
(178, 'Acrylic Extension', 1500, 90, 'Full set acrylic extension', 3, 31, '2026-02-18 14:14:38'),
(179, 'Paraffin Wax', 550, 40, 'Deep moisturizing treatment', 4, 32, '2026-02-18 14:14:38'),
(180, 'Nail Art Premium', 900, 60, 'Custom hand-painted designs', 3, 32, '2026-02-18 14:14:38'),
(181, 'Acrylic Extension', 1500, 90, 'Full set acrylic extension', 3, 32, '2026-02-18 14:14:38'),
(182, 'Gel Removal', 150, 20, 'Professional gel removal', 3, 32, '2026-02-18 14:14:38'),
(183, 'Callus Treatment', 400, 30, 'Foot skin softening', 2, 32, '2026-02-18 14:14:38'),
(184, 'Hand Massage', 300, 20, 'Relaxing hand massage with oil', 4, 32, '2026-02-18 14:14:38'),
(185, 'Acrylic Extension', 1500, 90, 'Full set acrylic extension', 3, 33, '2026-02-18 14:14:38'),
(186, 'Hand Massage', 300, 20, 'Relaxing hand massage with oil', 4, 33, '2026-02-18 14:14:38'),
(187, 'Basic Manicure', 250, 30, 'Basic cleaning and trimming', 1, 33, '2026-02-18 14:14:38'),
(188, 'Paraffin Wax', 550, 40, 'Deep moisturizing treatment', 4, 33, '2026-02-18 14:14:38'),
(189, 'Callus Treatment', 400, 30, 'Foot skin softening', 2, 33, '2026-02-18 14:14:38'),
(190, 'Gel Removal', 150, 20, 'Professional gel removal', 3, 33, '2026-02-18 14:14:38'),
(191, 'Callus Treatment', 400, 30, 'Foot skin softening', 2, 34, '2026-02-18 14:14:38'),
(192, 'Acrylic Extension', 1500, 90, 'Full set acrylic extension', 3, 34, '2026-02-18 14:14:38'),
(193, 'Spa Pedicure', 600, 60, 'Full foot spa and pedicure', 2, 34, '2026-02-18 14:14:38'),
(194, 'Basic Manicure', 250, 30, 'Basic cleaning and trimming', 1, 34, '2026-02-18 14:14:38'),
(195, 'Nail Art Premium', 900, 60, 'Custom hand-painted designs', 3, 34, '2026-02-18 14:14:38'),
(196, 'Organic Scrub', 450, 25, 'Natural salt and oil scrub', 4, 34, '2026-02-18 14:14:38'),
(197, 'Organic Scrub', 450, 25, 'Natural salt and oil scrub', 4, 35, '2026-02-18 14:14:38'),
(198, 'Nail Art Premium', 900, 60, 'Custom hand-painted designs', 3, 35, '2026-02-18 14:14:38'),
(199, 'Paraffin Wax', 550, 40, 'Deep moisturizing treatment', 4, 35, '2026-02-18 14:14:38'),
(200, 'Basic Manicure', 250, 30, 'Basic cleaning and trimming', 1, 35, '2026-02-18 14:14:38'),
(201, 'Spa Pedicure', 600, 60, 'Full foot spa and pedicure', 2, 35, '2026-02-18 14:14:38'),
(202, 'Acrylic Extension', 1500, 90, 'Full set acrylic extension', 3, 35, '2026-02-18 14:14:38'),
(203, 'Gel Polish Hands', 450, 45, 'Gel polish single color', 3, 36, '2026-02-18 14:14:38'),
(204, 'Acrylic Extension', 1500, 90, 'Full set acrylic extension', 3, 36, '2026-02-18 14:14:38'),
(205, 'Paraffin Wax', 550, 40, 'Deep moisturizing treatment', 4, 36, '2026-02-18 14:14:38'),
(206, 'Organic Scrub', 450, 25, 'Natural salt and oil scrub', 4, 36, '2026-02-18 14:14:38'),
(207, 'Nail Art Premium', 900, 60, 'Custom hand-painted designs', 3, 36, '2026-02-18 14:14:38'),
(208, 'Hand Massage', 300, 20, 'Relaxing hand massage with oil', 4, 36, '2026-02-18 14:14:38'),
(209, 'Nail Repair', 100, 15, 'Fix broken or chipped nail', 1, 37, '2026-02-18 14:14:38'),
(210, 'French Manicure', 350, 45, 'Classic white tip style', 3, 37, '2026-02-18 14:14:38'),
(211, 'Basic Manicure', 250, 30, 'Basic cleaning and trimming', 1, 37, '2026-02-18 14:14:38'),
(212, 'Paraffin Wax', 550, 40, 'Deep moisturizing treatment', 4, 37, '2026-02-18 14:14:38'),
(213, 'Spa Pedicure', 600, 60, 'Full foot spa and pedicure', 2, 37, '2026-02-18 14:14:38'),
(214, 'Callus Treatment', 400, 30, 'Foot skin softening', 2, 37, '2026-02-18 14:14:38'),
(215, 'Spa Pedicure', 600, 60, 'Full foot spa and pedicure', 2, 38, '2026-02-18 14:14:38'),
(216, 'Basic Manicure', 250, 30, 'Basic cleaning and trimming', 1, 38, '2026-02-18 14:14:38'),
(217, 'Gel Removal', 150, 20, 'Professional gel removal', 3, 38, '2026-02-18 14:14:38'),
(218, 'Gel Polish Hands', 450, 45, 'Gel polish single color', 3, 38, '2026-02-18 14:14:38'),
(219, 'Hand Massage', 300, 20, 'Relaxing hand massage with oil', 4, 38, '2026-02-18 14:14:38'),
(220, 'Nail Art Premium', 900, 60, 'Custom hand-painted designs', 3, 38, '2026-02-18 14:14:38'),
(221, 'Gel Removal', 150, 20, 'Professional gel removal', 3, 39, '2026-02-18 14:14:38'),
(222, 'Spa Pedicure', 600, 60, 'Full foot spa and pedicure', 2, 39, '2026-02-18 14:14:38'),
(223, 'French Manicure', 350, 45, 'Classic white tip style', 3, 39, '2026-02-18 14:14:38'),
(224, 'Paraffin Wax', 550, 40, 'Deep moisturizing treatment', 4, 39, '2026-02-18 14:14:38'),
(225, 'Acrylic Extension', 1500, 90, 'Full set acrylic extension', 3, 39, '2026-02-18 14:14:38'),
(226, 'Callus Treatment', 400, 30, 'Foot skin softening', 2, 39, '2026-02-18 14:14:38'),
(227, 'Gel Removal', 150, 20, 'Professional gel removal', 3, 40, '2026-02-18 14:14:38'),
(228, 'Nail Repair', 100, 15, 'Fix broken or chipped nail', 1, 40, '2026-02-18 14:14:38'),
(229, 'Callus Treatment', 400, 30, 'Foot skin softening', 2, 40, '2026-02-18 14:14:38'),
(230, 'Spa Pedicure', 600, 60, 'Full foot spa and pedicure', 2, 40, '2026-02-18 14:14:38'),
(231, 'Acrylic Extension', 1500, 90, 'Full set acrylic extension', 3, 40, '2026-02-18 14:14:38'),
(232, 'Hand Massage', 300, 20, 'Relaxing hand massage with oil', 4, 40, '2026-02-18 14:14:38'),
(233, 'Gel Removal', 150, 20, 'Professional gel removal', 3, 41, '2026-02-18 14:14:38'),
(234, 'Callus Treatment', 400, 30, 'Foot skin softening', 2, 41, '2026-02-18 14:14:38'),
(235, 'Organic Scrub', 450, 25, 'Natural salt and oil scrub', 4, 41, '2026-02-18 14:14:38'),
(236, 'Nail Art Premium', 900, 60, 'Custom hand-painted designs', 3, 41, '2026-02-18 14:14:38'),
(237, 'French Manicure', 350, 45, 'Classic white tip style', 3, 41, '2026-02-18 14:14:38'),
(238, 'Hand Massage', 300, 20, 'Relaxing hand massage with oil', 4, 41, '2026-02-18 14:14:38'),
(239, 'Paraffin Wax', 550, 40, 'Deep moisturizing treatment', 4, 42, '2026-02-18 14:14:38'),
(240, 'Nail Art Premium', 900, 60, 'Custom hand-painted designs', 3, 42, '2026-02-18 14:14:38'),
(241, 'Gel Polish Hands', 450, 45, 'Gel polish single color', 3, 42, '2026-02-18 14:14:38'),
(242, 'Basic Manicure', 250, 30, 'Basic cleaning and trimming', 1, 42, '2026-02-18 14:14:38'),
(243, 'Spa Pedicure', 600, 60, 'Full foot spa and pedicure', 2, 42, '2026-02-18 14:14:38'),
(244, 'Acrylic Extension', 1500, 90, 'Full set acrylic extension', 3, 42, '2026-02-18 14:14:38'),
(245, 'Spa Pedicure', 600, 60, 'Full foot spa and pedicure', 2, 43, '2026-02-18 14:14:38'),
(246, 'Gel Polish Hands', 450, 45, 'Gel polish single color', 3, 43, '2026-02-18 14:14:38'),
(247, 'Callus Treatment', 400, 30, 'Foot skin softening', 2, 43, '2026-02-18 14:14:38'),
(248, 'French Manicure', 350, 45, 'Classic white tip style', 3, 43, '2026-02-18 14:14:38'),
(249, 'Paraffin Wax', 550, 40, 'Deep moisturizing treatment', 4, 43, '2026-02-18 14:14:38'),
(250, 'Basic Manicure', 250, 30, 'Basic cleaning and trimming', 1, 43, '2026-02-18 14:14:38'),
(251, 'Gel Polish Hands', 450, 45, 'Gel polish single color', 3, 44, '2026-02-18 14:14:38'),
(252, 'Basic Manicure', 250, 30, 'Basic cleaning and trimming', 1, 44, '2026-02-18 14:14:38'),
(253, 'French Manicure', 350, 45, 'Classic white tip style', 3, 44, '2026-02-18 14:14:38'),
(254, 'Gel Removal', 150, 20, 'Professional gel removal', 3, 44, '2026-02-18 14:14:38'),
(255, 'Nail Art Premium', 900, 60, 'Custom hand-painted designs', 3, 44, '2026-02-18 14:14:38'),
(256, 'Hand Massage', 300, 20, 'Relaxing hand massage with oil', 4, 44, '2026-02-18 14:14:38'),
(257, 'Acrylic Extension', 1500, 90, 'Full set acrylic extension', 3, 45, '2026-02-18 14:14:38'),
(258, 'Nail Art Premium', 900, 60, 'Custom hand-painted designs', 3, 45, '2026-02-18 14:14:38'),
(259, 'Hand Massage', 300, 20, 'Relaxing hand massage with oil', 4, 45, '2026-02-18 14:14:38'),
(260, 'Basic Manicure', 250, 30, 'Basic cleaning and trimming', 1, 45, '2026-02-18 14:14:38'),
(261, 'Paraffin Wax', 550, 40, 'Deep moisturizing treatment', 4, 45, '2026-02-18 14:14:38'),
(262, 'French Manicure', 350, 45, 'Classic white tip style', 3, 45, '2026-02-18 14:14:38'),
(263, 'Nail Art Premium', 900, 60, 'Custom hand-painted designs', 3, 46, '2026-02-18 14:14:38'),
(264, 'Acrylic Extension', 1500, 90, 'Full set acrylic extension', 3, 46, '2026-02-18 14:14:38'),
(265, 'Hand Massage', 300, 20, 'Relaxing hand massage with oil', 4, 46, '2026-02-18 14:14:38'),
(266, 'Nail Repair', 100, 15, 'Fix broken or chipped nail', 1, 46, '2026-02-18 14:14:38'),
(267, 'Gel Polish Hands', 450, 45, 'Gel polish single color', 3, 46, '2026-02-18 14:14:38'),
(268, 'Organic Scrub', 450, 25, 'Natural salt and oil scrub', 4, 46, '2026-02-18 14:14:38'),
(522, 'สปามือ', 100, 5, '', NULL, 49, '2026-02-18 14:14:38'),
(523, 'ห้อง Smart Classroom 732', 455, 30, '', NULL, 50, '2026-02-18 14:14:38'),
(524, 'hvikg', 568, 86, '', NULL, 50, '2026-02-18 14:14:38'),
(528, 'dshb', 1234, 34, '', 1, 85, '2026-02-18 14:14:38'),
(529, 'dfg', 455, 45, '', 1, 86, '2026-02-18 14:14:38'),
(530, 'หำเะพ้ั่ะีเ้เกด', 1234, 123, '', 1, 1, '2026-02-18 14:14:44');

-- --------------------------------------------------------

--
-- Table structure for table `status_booking`
--

CREATE TABLE IF NOT EXISTS `status_booking` (
  `status_booking_id` int(11) NOT NULL,
  `status_booking_name` varchar(200) DEFAULT NULL,
  `description` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `status_booking`
--

INSERT INTO `status_booking` (`status_booking_id`, `status_booking_name`, `description`) VALUES
(1, 'pending', 'Waiting for confirmation'),
(2, 'confirmed', 'Booking confirmed'),
(3, 'completed', 'Service completed'),
(4, 'cancelled', 'Customer cancelled');

-- --------------------------------------------------------

--
-- Table structure for table `status_service`
--

CREATE TABLE IF NOT EXISTS `status_service` (
  `status_service_id` int(11) NOT NULL,
  `status_service_name` varchar(200) DEFAULT NULL,
  `description` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `status_service`
--

INSERT INTO `status_service` (`status_service_id`, `status_service_name`, `description`) VALUES
(1, 'available', 'Service available'),
(2, 'unavailable', 'Service temporarily unavailable');

-- --------------------------------------------------------

--
-- Table structure for table `status_store`
--

CREATE TABLE IF NOT EXISTS `status_store` (
  `status_store_id` int(11) NOT NULL,
  `status_store_name` varchar(200) DEFAULT NULL,
  `description` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `status_store`
--

INSERT INTO `status_store` (`status_store_id`, `status_store_name`, `description`) VALUES
(1, 'active', 'Store is operating normally'),
(2, 'closed', 'Store is temporarily closed'),
(3, 'renovation', 'Store under renovation');

-- --------------------------------------------------------

--
-- Table structure for table `store`
--

CREATE TABLE IF NOT EXISTS `store` (
  `store_id` int(11) NOT NULL,
  `store_name` varchar(200) DEFAULT NULL,
  `price` decimal(10,2) NOT NULL DEFAULT 0.00,
  `phone` varchar(50) DEFAULT NULL,
  `email` varchar(200) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `image` varchar(200) DEFAULT NULL,
  `status_store_id` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `store`
--

INSERT INTO `store` (`store_id`, `store_name`, `price`, `phone`, `email`, `user_id`, `address`, `image`, `status_store_id`, `created_at`, `updated_at`, `deleted_at`) VALUES
(1, 'NailBar Central Plaza', 299.00, '0811111111', 'central@nailbar.com', 1, 'Central Plaza Floor 2', 'central.jpg', 1, '2025-12-10 13:35:31', NULL, NULL),
(2, 'NailBar The Mall', 399.00, '0822222222', 'themall@nailbar.com', 2, 'The Mall Floor 1', 'themall.jpg', 1, '2025-12-10 13:35:31', NULL, NULL),
(3, 'NailBar Terminal 21', 499.00, '0833333333', 't21@nailbar.com', 3, 'Terminal 21 Floor 3', 't21.jpg', 1, '2025-12-10 13:35:31', NULL, NULL),
(4, 'NailBar Central Khon Kaen', 299.00, '0860000001', 'central_khonkaen@nailbar.com', 4, 'Central Khon Kaen Floor 2', 'kk_central.jpg', 1, '2025-12-10 13:45:10', NULL, NULL),
(5, 'NailBar Fairy Plaza', 399.00, '0860000002', 'fairy@nailbar.com', 5, 'Fairy Plaza Floor 1', 'fairy.jpg', 1, '2025-12-10 13:45:10', NULL, NULL),
(6, 'NailBar Tukcom Khon Kaen', 299.00, '0860000003', 'tukcom@nailbar.com', 6, 'Tukcom Khon Kaen Floor 3', 'tukcom.jpg', 1, '2025-12-10 13:45:10', NULL, NULL),
(7, 'NailBar Ton Tann Market', 199.00, '0860000004', 'tontan@nailbar.com', 7, 'Ton Tann Night Market Zone B', 'tontan.jpg', 1, '2025-12-10 13:45:10', NULL, NULL),
(8, 'NailBar Khon Kaen University - Complex', 299.00, '0860000005', 'kku_complex@nailbar.com', 8, 'KKU Complex Zone A', 'kku_complex.jpg', 1, '2025-12-10 13:45:10', NULL, NULL),
(9, 'NailBar Khon Kaen University - Nursing Fac.', 299.00, '0860000006', 'kku_nursing@nailbar.com', 9, 'KKU Nursing Faculty', 'kku_nursing.jpg', 1, '2025-12-10 13:45:10', NULL, NULL),
(10, 'NailBar Khon Kaen University - Engineering', 399.00, '0860000007', 'kku_engineer@nailbar.com', 10, 'KKU Faculty of Engineering', 'kku_engineer.jpg', 1, '2025-12-10 13:45:10', NULL, NULL),
(11, 'NailBar Khon Kaen University - Agriculture', 299.00, '0860000008', 'kku_agri@nailbar.com', 11, 'KKU Faculty of Agriculture', 'kku_agri.jpg', 1, '2025-12-10 13:45:10', NULL, NULL),
(12, 'NailBar Khon Kaen Hospital Zone', 399.00, '0860000009', 'kku_hospital@nailbar.com', 12, 'Khon Kaen Hospital Gate 1', 'hospital.jpg', 1, '2025-12-10 13:45:10', NULL, NULL),
(13, 'NailBar Srinagarind Hospital', 299.00, '0860000010', 'srina@nailbar.com', 13, 'Srinagarind Hospital Entrance', 'srina.jpg', 1, '2025-12-10 13:45:10', NULL, NULL),
(14, 'NailBar Big C Khon Kaen', 399.00, '0860000011', 'bigc@nailbar.com', 14, 'Big C Supercenter Floor 1', 'bigc.jpg', 1, '2025-12-10 13:45:10', NULL, NULL),
(15, 'NailBar Lotus Khon Kaen', 299.00, '0860000012', 'lotus@nailbar.com', 15, 'Lotus Khon Kaen Ground Floor', 'lotus.jpg', 1, '2025-12-10 13:45:10', NULL, NULL),
(16, 'NailBar Lotus Kaen Nakhon', 399.00, '0860000013', 'lotus_kku@nailbar.com', 16, 'Lotus Kaen Nakhon Branch', 'lotus_kku.jpg', 1, '2025-12-10 13:45:10', NULL, NULL),
(17, 'NailBar HomePro Khon Kaen', 299.00, '0860000014', 'homepro@nailbar.com', 17, 'HomePro Khon Kaen', 'homepro.jpg', 1, '2025-12-10 13:45:10', NULL, NULL),
(18, 'NailBar Index Living Mall', 399.00, '0860000015', 'index@nailbar.com', 18, 'Index Living Mall Khon Kaen', 'index.jpg', 1, '2025-12-10 13:45:10', NULL, NULL),
(19, 'NailBar Khon Kaen Bus Terminal 3', 199.00, '0860000016', 'bus3@nailbar.com', 19, 'Bus Terminal 3 Zone A', 'bus3.jpg', 1, '2025-12-10 13:45:10', NULL, NULL),
(20, 'NailBar Mittraphap Road - Hugz Mall', 299.00, '0860000017', 'hugz@nailbar.com', 20, 'Hugz Mall Mittraphap Road', 'hugz.jpg', 1, '2025-12-10 13:45:10', NULL, NULL),
(21, 'NailBar Ruamchok Market', 299.00, '0860000018', 'ruamchok@nailbar.com', 21, 'Ruamchok Market Zone 2', 'ruamchok.jpg', 1, '2025-12-10 13:45:10', NULL, NULL),
(22, 'NailBar Ban Pet', 399.00, '0860000019', 'banpet@nailbar.com', 22, 'Ban Pet Main Road', 'banpet.jpg', 1, '2025-12-10 13:45:10', NULL, NULL),
(23, 'NailBar Thai Samakkhi', 299.00, '0860000020', 'samakki@nailbar.com', 23, 'Thai Samakkhi Market', 'samakki.jpg', 1, '2025-12-10 13:45:10', NULL, NULL),
(24, 'NailBar Ban Kok', 399.00, '0860000021', 'bankok@nailbar.com', 24, 'Ban Kok Village Road', 'bankok.jpg', 1, '2025-12-10 13:45:10', NULL, NULL),
(25, 'NailBar Sila', 299.00, '0860000022', 'sila@nailbar.com', 25, 'Sila Subdistrict', 'sila.jpg', 1, '2025-12-10 13:45:10', NULL, NULL),
(26, 'NailBar Don Chang', 399.00, '0860000023', 'donchang@nailbar.com', 26, 'Don Chang Community', 'donchang.jpg', 1, '2025-12-10 13:45:10', NULL, NULL),
(27, 'NailBar Bueng Kaen Nakhon', 299.00, '0860000024', 'bkn@nailbar.com', 27, 'Bueng Kaen Nakhon Park Zone', 'bkn.jpg', 1, '2025-12-10 13:45:10', NULL, NULL),
(28, 'NailBar Chumphon Market', 399.00, '0860000025', 'chumphon@nailbar.com', 28, 'Chumphon Market, Floor 1', 'chumphon.jpg', 1, '2025-12-10 13:45:10', NULL, NULL),
(29, 'NailBar Ban Phai', 299.00, '0860000026', 'banphai@nailbar.com', 29, 'Ban Phai District Plaza', 'banphai.jpg', 1, '2025-12-10 13:45:10', NULL, NULL),
(30, 'NailBar Chonnabot', 399.00, '0860000027', 'chonnabot@nailbar.com', 30, 'Chonnabot Silk Market', 'chonnabot.jpg', 1, '2025-12-10 13:45:10', NULL, NULL),
(31, 'NailBar Mancha Khiri', 299.00, '0860000028', 'mancha@nailbar.com', 1, 'Mancha Khiri District', 'mancha.jpg', 1, '2025-12-10 13:45:10', NULL, NULL),
(32, 'NailBar Phra Yuen', 399.00, '0860000029', 'phrayuen@nailbar.com', 1, 'Phra Yuen Market', 'phrayuen.jpg', 1, '2025-12-10 13:45:10', NULL, NULL),
(33, 'NailBar Phu Wiang', 299.00, '0860000030', 'phuwiang@nailbar.com', 1, 'Phu Wiang District', 'phuwiang.jpg', 1, '2025-12-10 13:45:10', NULL, NULL),
(34, 'NailBar Nong Ruea', 399.00, '0860000031', 'nongruea@nailbar.com', 1, 'Nong Ruea Plaza', 'nongruea.jpg', 1, '2025-12-10 13:45:10', NULL, NULL),
(35, 'NailBar Kranuan', 299.00, '0860000032', 'kranuan@nailbar.com', 1, 'Kranuan Market', 'kranuan.jpg', 1, '2025-12-10 13:45:10', NULL, NULL),
(36, 'NailBar Khok Si', 399.00, '0860000033', 'khoksi@nailbar.com', 1, 'Khok Si Subdistrict', 'khoksi.jpg', 1, '2025-12-10 13:45:10', NULL, NULL),
(37, 'NailBar Ban Haet', 299.00, '0860000034', 'banhaet@nailbar.com', 1, 'Ban Haet Road', 'banhaet.jpg', 1, '2025-12-10 13:45:10', NULL, NULL),
(38, 'NailBar Waeng Noi', 399.00, '0860000035', 'waengnoi@nailbar.com', 1, 'Waeng Noi District', 'waengnoi.jpg', 1, '2025-12-10 13:45:10', NULL, NULL),
(39, 'NailBar Waeng Yai', 299.00, '0860000036', 'waengyai@nailbar.com', 1, 'Waeng Yai District', 'waengyai.jpg', 1, '2025-12-10 13:45:10', NULL, NULL),
(40, 'NailBar Nong Na Kham', 399.00, '0860000037', 'nongnakham@nailbar.com', 1, 'Nong Na Kham Rural Road', 'nongnakham.jpg', 1, '2025-12-10 13:45:10', NULL, NULL),
(41, 'NailBar Samran', 299.00, '0860000038', 'samran@nailbar.com', 1, 'Samran Subdistrict', 'samran.jpg', 1, '2025-12-10 13:45:10', NULL, NULL),
(42, 'NailBar Mueang Kao', 399.00, '0860000039', 'mueangkao@nailbar.com', 1, 'Mueang Kao National Museum Area', 'mueangkao.jpg', 1, '2025-12-10 13:45:10', NULL, NULL),
(43, 'NailBar Saphan Mit', 299.00, '0860000040', 'saphanmit@nailbar.com', 1, 'Saphan Mit Official Market', 'saphanmit.jpg', 1, '2025-12-10 13:45:10', NULL, NULL),
(44, 'NailBar Klang Mueang Road', 399.00, '0860000041', 'klangmuang@nailbar.com', 1, 'Klang Mueang Walking Street', 'klangmuang.jpg', 1, '2025-12-10 13:45:10', NULL, NULL),
(45, 'NailBar Lao Nadee', 299.00, '0860000042', 'laonadee@nailbar.com', 1, 'Lao Nadee Community', 'laonadee.jpg', 1, '2025-12-10 13:45:10', NULL, NULL),
(46, 'NailBar Ban Ped Lotus', 399.00, '0860000043', 'banped_lotus@nailbar.com', 1, 'Lotus Ban Ped Branch', 'banped_lotus.jpg', 1, '2025-12-10 13:45:10', NULL, NULL),
(47, 'แแแ', 0.00, '', '', 1, NULL, NULL, 1, '2026-01-19 01:00:18', NULL, NULL),
(48, 'Dutchass', 0.00, '', '', 1, NULL, NULL, 1, '2026-01-19 01:10:37', NULL, NULL),
(49, 'แก้วกานสวัสดีจุบุ', 200.00, '', '', 1, NULL, NULL, 1, '2026-01-19 01:15:36', NULL, NULL),
(50, 'kitty', 450.00, '', '', 1, NULL, NULL, 1, '2026-01-19 01:42:52', NULL, NULL),
(51, 'littiig', 500.00, '', 'kugho@kkumail.com', 1, NULL, NULL, 1, '2026-01-19 02:36:11', NULL, NULL),
(52, 'eee', 444.00, '', 'asdfg@gmail.com', 1, NULL, NULL, 1, '2026-01-19 02:38:41', NULL, NULL),
(53, 'ddf', 50.00, '', 'eaa@gmaol.com', 1, NULL, NULL, 1, '2026-01-19 17:23:37', NULL, NULL),
(54, 'พำกด', 297.00, '0646785822', 'sdf@gmail.com', 1, NULL, NULL, 1, '2026-01-19 17:28:45', NULL, NULL),
(55, '', 0.00, '', '', 1, NULL, NULL, 1, '2026-01-19 17:30:46', NULL, NULL),
(56, 'puttan', 535.00, '0646985834', 'fgdodf@gamil.com', 1, NULL, NULL, 1, '2026-01-19 17:32:49', NULL, NULL),
(57, 'puttan', 535.00, '0646985834', 'fgdodf@gamil.com', 1, NULL, NULL, 1, '2026-01-19 17:33:07', NULL, NULL),
(58, 'puttan', 535.00, '0646985834', 'fgdodf@gamil.com', 1, NULL, NULL, 1, '2026-01-19 17:33:14', NULL, NULL),
(59, 'puttan', 535.00, '0646985834', 'fgdodf@gamil.com', 1, NULL, NULL, 1, '2026-01-19 17:33:22', NULL, NULL),
(60, 'puttan', 300.00, '0646785822', 'abcd@gamil.com', 1, NULL, NULL, 1, '2026-01-19 17:36:34', NULL, NULL),
(61, 'puttan', 300.00, '0646785822', 'abcd@gamil.com', 1, NULL, NULL, 1, '2026-01-19 17:37:52', NULL, NULL),
(62, '', 0.00, '', '', 1, NULL, NULL, 1, '2026-01-19 17:38:25', NULL, NULL),
(63, 'puttan', 400.00, '0646785834', 'chttiiky@gmail.com', 1, NULL, NULL, 1, '2026-01-19 17:40:52', NULL, NULL),
(64, 'puttan', 400.00, '0646785834', 'chttiiky@gmail.com', 1, NULL, NULL, 1, '2026-01-19 17:42:15', NULL, NULL),
(65, 'puttan', 400.00, '0646785834', 'chttiiky@gmail.com', 1, NULL, NULL, 1, '2026-01-19 17:43:05', NULL, NULL),
(66, 'puttanyg', 400.00, '0646785834', 'chttiiky@gmail.com', 1, NULL, NULL, 1, '2026-01-19 17:43:40', NULL, NULL),
(67, 'a', 397.00, '0987654321', 'dfbfhg@gamil.com', 1, NULL, NULL, 1, '2026-01-19 17:56:28', NULL, NULL),
(68, 'kiyt', 99.00, '0986578977', 'hfrbe@gmail.com', 1, NULL, NULL, 1, '2026-01-20 01:15:14', NULL, NULL),
(69, 'kitty888', 398.00, '0646785822', 'dcfgb@gamil.com', 1, NULL, NULL, 1, '2026-02-08 23:17:37', NULL, NULL),
(70, 'kitty888', 398.00, '0646785822', 'dcfgb@gamil.com', 1, NULL, NULL, 1, '2026-02-08 23:17:51', NULL, NULL),
(71, 'ดดดด', 398.00, '0891234567', 'dsfghjk@gmail.com', 50, NULL, NULL, 1, '2026-02-08 23:34:04', NULL, NULL),
(72, 'ดดดด', 398.00, '0891234567', 'dsfghjk@gmail.com', 50, NULL, NULL, 1, '2026-02-08 23:35:02', NULL, NULL),
(73, 'ดดดด', 398.00, '0891234567', 'dsfghjk@gmail.com', 1, NULL, NULL, 1, '2026-02-08 23:37:39', NULL, NULL),
(74, 'ดดดด', 398.00, '0891234567', 'dsfghjk@gmail.com', 50, NULL, NULL, 1, '2026-02-08 23:45:10', NULL, NULL),
(75, 'sxa', 494.00, '0981234567', 'dfdfgh@gmail.com', 50, NULL, NULL, 1, '2026-02-08 23:46:06', NULL, NULL),
(76, 'sxa', 494.00, '0981234567', 'dfdfgh@gmail.com', 50, NULL, NULL, 1, '2026-02-08 23:48:00', NULL, NULL),
(77, 'sxa', 494.00, '0981234567', 'dfdfgh@gmail.com', 50, NULL, NULL, 1, '2026-02-08 23:49:36', NULL, NULL),
(78, 'sxa', 494.00, '0981234567', 'dfdfgh@gmail.com', 50, NULL, NULL, 1, '2026-02-08 23:49:44', NULL, NULL),
(79, 'sxa', 494.00, '0981234567', 'dfdfgh@gmail.com', 50, NULL, NULL, 1, '2026-02-08 23:55:37', NULL, NULL),
(80, 'sxa', 494.00, '0981234567', 'dfdfgh@gmail.com', 50, NULL, NULL, 1, '2026-02-08 23:57:10', NULL, NULL),
(81, 'sxa', 494.00, '0981234567', 'dfdfgh@gmail.com', 50, NULL, NULL, 1, '2026-02-08 23:58:30', NULL, NULL),
(82, 'sxa', 494.00, '0981234567', 'dfdfgh@gmail.com', 50, NULL, NULL, 1, '2026-02-08 23:59:37', NULL, NULL),
(83, 'BTS', 200.00, '0981234567', 'wdertyydsfgh@gmail.com', 50, NULL, NULL, 1, '2026-02-09 23:39:18', NULL, NULL),
(84, 'BTS', 200.00, '0981234567', 'wdertyydsfgh@gmail.com', 50, NULL, NULL, 1, '2026-02-09 23:45:47', NULL, NULL),
(85, 'asgfbvcv', 200.00, '0981234567', 'dsgthngff@gmail.com', 50, NULL, NULL, 1, '2026-02-10 00:06:59', NULL, NULL),
(86, 'BTSS', 400.00, '0981234567', 'frgthh@mail.com', 50, NULL, NULL, 1, '2026-02-10 00:36:08', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `store_address`
--

CREATE TABLE IF NOT EXISTS `store_address` (
  `store_address_id` int(11) NOT NULL,
  `province` varchar(200) DEFAULT NULL,
  `district` varchar(200) DEFAULT NULL,
  `subdistrict` varchar(200) DEFAULT NULL,
  `postal_code` varchar(20) DEFAULT NULL,
  `store_id` int(11) DEFAULT NULL,
  `is_verified` tinyint(1) DEFAULT 0,
  `has_parking` tinyint(1) DEFAULT 0,
  `open_time` time DEFAULT NULL,
  `close_time` time DEFAULT NULL,
  `recommend_text` text DEFAULT NULL,
  `street` varchar(255) DEFAULT NULL,
  `deleted_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `store_address`
--

INSERT INTO `store_address` (`store_address_id`, `province`, `district`, `subdistrict`, `postal_code`, `store_id`, `is_verified`, `has_parking`, `open_time`, `close_time`, `recommend_text`, `street`, `deleted_at`) VALUES
(1, 'กรุงเทพ', 'เลขที่: 123/4\r\nตำบล: ปทุมวัน', 'สยาม', '10330', 1, 1, 1, '10:00:00', '20:00:00', 'แนะนำ: เจลพื้นเรียบ + มินิมอล · ใช้ของแท้ · สีทน', 'ถนนมิตรภาพ', NULL),
(2, 'กรุงเทพฯ', 'เลขที่: 45/7\nตำบล: หัวหมาก', 'หัวหมาก', '10240', 2, 1, 0, '11:00:00', '21:00:00', 'เด่นงานเจลลุคหวาน เหมาะกับทุกวัย', 'ถนนรัชดาภิเษก', NULL),
(3, 'กรุงเทพฯ', 'เลขที่: 99/12\nตำบล: คลองเตยเหนือ', 'คลองเตยเหนือ', '10110', 3, 0, 0, '10:30:00', '20:30:00', 'เชี่ยวชาญงานเพ้นท์ลายละเอียด', 'ถนนพหลโยธิน', NULL),
(4, 'กรุงเทพฯ', 'เลขที่: 200/5\nตำบล: ดินแดง', 'ดินแดง', '10400', 4, 1, 1, '09:30:00', '19:30:00', 'ร้านประจำย่านลาดพร้าว งานเรียบร้อย', 'ถนนลาดพร้าว', NULL),
(5, 'กรุงเทพฯ', 'เลขที่: 78/3\nตำบล: บางซื่อ', 'บางซื่อ', '10800', 5, 1, 0, '12:00:00', '22:00:00', 'สายแฟชั่นต้องลอง สีเจลแน่น', 'ถนนสุขุมวิท', NULL),
(6, 'กรุงเทพฯ', 'เลขที่: 12/9\nตำบล: จตุจักร', 'จตุจักร', '10900', 6, 0, 1, '10:00:00', '19:00:00', 'บริการดี เป็นกันเอง ราคาเหมาะสม', 'ถนนวิภาวดีรังสิต', NULL),
(7, 'กรุงเทพฯ', 'เลขที่: 56/2\nตำบล: พระโขนง', 'พระโขนง', '10260', 7, 1, 0, '11:00:00', '20:00:00', 'ลายมินิมอล สายเกาหลี', 'ถนนเพชรบุรี', NULL),
(8, 'กรุงเทพฯ', 'เลขที่: 300/11\nตำบล: บางนา', 'บางนา', '10260', 8, 0, 1, '09:00:00', '18:00:00', 'เหมาะกับลูกค้าครอบครัว มีที่จอดรถ', 'ถนนบางนา-ตราด', NULL),
(9, 'กรุงเทพฯ', 'เลขที่: 144/8\nตำบล: สุขุมวิท', 'คลองตันเหนือ', '10110', 9, 1, 1, '10:00:00', '21:00:00', 'งานพรีเมียม ใช้วัสดุนำเข้า', 'ถนนพระราม 9', NULL),
(10, 'กรุงเทพฯ', 'เลขที่: 510/4\nตำบล: ปากคลองภาษีเจริญ', 'ภาษีเจริญ', '10160', 10, 0, 1, '10:00:00', '20:00:00', 'ร้านเล็บครบวงจร งานเนี๊ยบ', 'ถนนศรีนครินทร์', NULL),
(11, 'ขอนแก่น', 'เมืองขอนแก่น', 'ในเมือง', '40000', 11, 1, 1, '10:00:00', '20:00:00', 'ร้านเล็บสไตล์เกาหลี ดีไซน์ทันสมัย', 'ถนนมิตรภาพ', NULL),
(12, 'ขอนแก่น', 'เมืองขอนแก่น', 'ในเมือง', '40000', 12, 1, 1, '09:00:00', '21:00:00', 'เน้นงานปั้นนูนและอะคริลิค', 'ถนนรื่นรมย์', NULL),
(13, 'ขอนแก่น', 'เมืองขอนแก่น', 'ศิลา', '40000', 13, 1, 0, '10:00:00', '20:00:00', 'บริการเป็นกันเอง ราคานักศึกษา', 'ถนนกัลปพฤกษ์', NULL),
(14, 'ขอนแก่น', 'เมืองขอนแก่น', 'ในเมือง', '40000', 14, 1, 1, '11:00:00', '21:00:00', 'สปามือเท้าครบวงจร', 'ถนนหน้าเมือง', NULL),
(15, 'ขอนแก่น', 'เมืองขอนแก่น', 'บ้านเป็ด', '40000', 15, 1, 1, '10:30:00', '20:30:00', 'เด่นงานเพ้นท์ลายการ์ตูน', 'ถนนมะลิวัลย์', NULL),
(16, 'ขอนแก่น', 'เมืองขอนแก่น', 'ในเมือง', '40000', 16, 1, 1, '09:00:00', '19:00:00', 'บรรยากาศมินิมอล ถ่ายรูปสวย', 'ถนนกลางเมือง', NULL),
(17, 'ขอนแก่น', 'เมืองขอนแก่น', 'ในเมือง', '40000', 17, 1, 0, '10:00:00', '20:00:00', 'สีเจลนำเข้าจากญี่ปุ่น', 'ถนนดรุณสำราญ', NULL),
(18, 'ขอนแก่น', 'เมืองขอนแก่น', 'ศิลา', '40000', 18, 1, 1, '11:00:00', '21:00:00', 'ต่อเล็บ PVC ทนทาน งานละเอียด', 'ถนนเลี่ยงเมือง', NULL),
(19, 'ขอนแก่น', 'เมืองขอนแก่น', 'ในเมือง', '40000', 19, 1, 1, '10:00:00', '20:00:00', 'โปรโมชั่นเปิดร้านใหม่ ลด 20%', 'ถนนเหล่านาดี', NULL),
(20, 'ขอนแก่น', 'ชุมแพ', 'ชุมแพ', '40130', 20, 1, 1, '09:30:00', '19:30:00', 'ร้านดังในชุมแพ งานสวยเนี๊ยบ', 'ถนนมะลิวัลย์', NULL),
(21, 'ขอนแก่น', 'ชุมแพ', 'หนองไผ่', '40130', 21, 1, 1, '10:00:00', '20:00:00', 'บริการทำเล็บและต่อขนตา', 'ถนนราษฎร์บำรุง', NULL),
(22, 'ขอนแก่น', 'กระนวน', 'หนองโก', '40170', 22, 1, 1, '09:00:00', '19:00:00', 'งานไว ตรงปก ไม่รอนาน', 'ถนนสายไหม', NULL),
(23, 'ขอนแก่น', 'บ้านไผ่', 'ในเมือง', '40110', 23, 1, 1, '10:00:00', '20:00:00', 'ช่างมีประสบการณ์กว่า 10 ปี', 'ถนนเจนจบทิศ', NULL),
(24, 'ขอนแก่น', 'พล', 'เมืองพล', '40120', 24, 1, 0, '09:30:00', '19:30:00', 'ร้านเล็บราคาย่อมเยา', 'ถนนเสริมสวัสดิ์', NULL),
(25, 'ขอนแก่น', 'เมืองขอนแก่น', 'ในเมือง', '40000', 25, 1, 1, '11:00:00', '22:00:00', 'เปิดดึกเอาใจคนทำงาน', 'ถนนรื่นจิตร', NULL),
(26, 'ขอนแก่น', 'เมืองขอนแก่น', 'ในเมือง', '40000', 26, 1, 1, '10:00:00', '20:00:00', 'งานเจลขัดผงกระจกสุดหรู', 'ถนนพิมพสุต', NULL),
(27, 'ขอนแก่น', 'เมืองขอนแก่น', 'ในเมือง', '40000', 27, 1, 1, '10:00:00', '20:00:00', 'งานตัดหนังสะอาด ทาสีสวย', 'ถนนชวนชื่น', NULL),
(28, 'ขอนแก่น', 'เมืองขอนแก่น', 'ในเมือง', '40000', 28, 1, 0, '09:00:00', '19:00:00', 'รับออกแบบลายเล็บตามใจชอบ', 'ถนนหลังเมือง', NULL),
(29, 'ขอนแก่น', 'เมืองขอนแก่น', 'บ้านเป็ด', '40000', 29, 1, 1, '10:30:00', '20:30:00', 'สปาพาราฟินมือและเท้า', 'ถนนศรีจันทร์', NULL),
(30, 'ขอนแก่น', 'น้ำพอง', 'น้ำพอง', '40140', 30, 1, 1, '09:00:00', '18:00:00', 'บริการดี ยิ้มแย้มแจ่มใส', 'ถนนพิทักษ์พงษ์', NULL),
(31, 'ขอนแก่น', 'น้ำพอง', 'วังชัย', '40140', 31, 1, 1, '10:00:00', '20:00:00', 'งานติดอะไหล่แน่น ไม่หลุดง่าย', 'ถนนน้ำพอง-กระนวน', NULL),
(32, 'ขอนแก่น', 'เมืองขอนแก่น', 'ในเมือง', '40000', 32, 1, 1, '09:00:00', '19:00:00', 'สีเจลออร์แกนิค ปลอดภัย', 'ถนนกสิกรทุ่งสร้าง', NULL),
(33, 'ขอนแก่น', 'เมืองขอนแก่น', 'ในเมือง', '40000', 33, 1, 1, '10:00:00', '21:00:00', 'เน้นงานเรียบหรู ดูแพง', 'ถนนประชาสโมสร', NULL),
(34, 'ขอนแก่น', 'เมืองขอนแก่น', 'ศิลา', '40000', 34, 1, 1, '10:00:00', '20:00:00', 'รับสอนทำเล็บและบริการ', 'ถนนขอนแก่น-ยางตลาด', NULL),
(35, 'ขอนแก่น', 'เมืองขอนแก่น', 'ในเมือง', '40000', 35, 1, 1, '09:30:00', '20:00:00', 'ต่อเล็บโพลีเจล เบาสบาย', 'ถนนเทพารักษ์', NULL),
(36, 'ขอนแก่น', 'เมืองขอนแก่น', 'บ้านเป็ด', '40000', 36, 1, 0, '11:00:00', '21:00:00', 'ร้านเล็กๆ แต่อบอุ่น', 'ถนนหมู่บ้านคำไฮ', NULL),
(37, 'ขอนแก่น', 'เมืองขอนแก่น', 'ในเมือง', '40000', 37, 1, 1, '10:00:00', '20:00:00', 'ช่างเก่งงานลูกแก้ว Cat Eye', 'ถนนวรสิทธิ์', NULL),
(38, 'ขอนแก่น', 'เมืองขอนแก่น', 'ในเมือง', '40000', 38, 1, 1, '10:00:00', '20:00:00', 'โปรโมชั่นสะสมแต้มครบ 10 ฟรี 1', 'ถนนหน้าสถานีรถไฟ', NULL),
(39, 'ขอนแก่น', 'หนองเรือ', 'หนองเรือ', '40210', 39, 1, 1, '09:00:00', '18:00:00', 'บริการทั่วถึง ราคามิตรภาพ', 'ถนนทางหลวง 12', NULL),
(40, 'ขอนแก่น', 'บ้านฝาง', 'บ้านฝาง', '40270', 40, 1, 1, '09:00:00', '19:00:00', 'งานทาสีเจลพื้นฐานสุดเนี๊ยบ', 'ถนนมะลิวัลย์', NULL),
(41, 'ขอนแก่น', 'เมืองขอนแก่น', 'ในเมือง', '40000', 41, 1, 1, '10:00:00', '20:00:00', 'สีสวยติดทนนานเกินเดือน', 'ถนนรื่นรมย์ (ทางรถไฟ)', NULL),
(42, 'ขอนแก่น', 'เมืองขอนแก่น', 'ในเมือง', '40000', 42, 1, 1, '11:00:00', '21:00:00', 'ใช้ผลิตภัณฑ์ชั้นนำระดับโลก', 'ถนนนิกรสำราญ', NULL),
(43, 'ขอนแก่น', 'เมืองขอนแก่น', 'ในเมือง', '40000', 43, 1, 1, '09:00:00', '20:00:00', 'ร้านทำเล็บในตำนานของขอนแก่น', 'ถนนอำมาตย์', NULL),
(44, 'ขอนแก่น', 'เมืองขอนแก่น', 'ในเมือง', '40000', 44, 1, 1, '10:00:00', '19:00:00', 'งานเพ้นท์ปลายเล็บ French Nail', 'ถนนสนามบิน', NULL),
(45, 'ขอนแก่น', 'เมืองขอนแก่น', 'ในเมือง', '40000', 45, 1, 1, '08:30:00', '19:30:00', 'รับทำเล็บนอกสถานที่', 'ถนนหลังศูนย์ราชการ', NULL),
(46, 'ขอนแก่น', 'เมืองขอนแก่น', 'ในเมือง', '40000', 46, 1, 1, '10:00:00', '20:00:00', 'ร้านเล็บคุณภาพ ราคาประทับใจ', 'ถนนร่วมจิตร', NULL),
(47, 'อารีย์', NULL, NULL, '', 47, 0, 0, '10:00:00', '20:00:00', '10:00', '123 v.vv m.mm j.jj', NULL),
(48, 'ขอนแก่น', 'ไม่ระบุ', 'ไม่ระบุ', '', 48, 0, 0, '09:00:00', '20:00:00', 'ร้านพี่เปิดตามใจ', '555 ', NULL),
(51, 'อุตรดิตถ์', 'ลับแล', 'ไผ่ล้อม', '53210', 51, 0, 0, '10:00:00', '20:00:00', 'ghuhoo', '235', NULL),
(52, 'กระบี่', 'เขาพนม', 'เขาดิน', '81140', 52, 0, 0, '10:00:00', '20:00:00', 'สวยมากจ้า', '123', NULL),
(53, 'นครสวรรค์', 'โกรกพระ', 'บางประมุง', '60170', 53, 0, 0, '10:00:00', '20:00:00', 'l;po;j;', '12345', NULL),
(54, 'เชียงราย', 'ขุนตาล', 'ป่าตาล', '57340', 54, 0, 0, '10:00:00', '20:00:00', '', '123', NULL),
(55, '', '', '', '', 55, 0, 0, '10:00:00', '20:00:00', '', '', NULL),
(56, 'หนองบัวลำภู', 'นาวัง', 'นาแก', '39170', 56, 0, 0, '10:00:00', '20:00:00', '', '123', NULL),
(57, 'หนองบัวลำภู', 'นาวัง', 'นาแก', '39170', 57, 0, 0, '10:00:00', '20:00:00', '', '123', NULL),
(58, 'หนองบัวลำภู', 'นาวัง', 'นาแก', '39170', 58, 0, 0, '10:00:00', '20:00:00', '', '123', NULL),
(59, 'หนองบัวลำภู', 'นาวัง', 'นาแก', '39170', 59, 0, 0, '10:00:00', '20:00:00', '', '123', NULL),
(60, 'ชุมพร', 'ปะทิว', 'สะพลี', '86230', 60, 0, 0, '10:00:00', '20:00:00', '', '123', NULL),
(61, 'ชุมพร', 'ปะทิว', 'สะพลี', '86230', 61, 0, 0, '10:00:00', '20:00:00', '', '123', NULL),
(62, '', '', '', '', 62, 0, 0, '10:00:00', '20:00:00', '', '', NULL),
(63, 'สมุทรสาคร', 'บ้านแพ้ว', 'บ้านแพ้ว', '74120', 63, 0, 0, '10:00:00', '20:00:00', '', '123', NULL),
(64, 'สมุทรสาคร', 'บ้านแพ้ว', 'บ้านแพ้ว', '74120', 64, 0, 0, '10:00:00', '20:00:00', '', '123', NULL),
(65, 'สมุทรสาคร', 'บ้านแพ้ว', 'บ้านแพ้ว', '74120', 65, 0, 0, '10:00:00', '20:00:00', '', '123', NULL),
(66, 'สมุทรสาคร', 'บ้านแพ้ว', 'บ้านแพ้ว', '74120', 66, 0, 0, '10:00:00', '20:00:00', '', '123', NULL),
(67, 'อำนาจเจริญ', 'ลืออำนาจ', 'ไร่ขี', '37000', 67, 0, 0, '10:00:00', '20:00:00', '', '123', NULL),
(68, 'พะเยา', 'เชียงคำ', 'น้ำแวน', '56110', 68, 0, 0, '10:00:00', '20:00:00', '', '45/6', NULL),
(69, 'กระบี่', 'คลองท่อม', 'พรุดินนา', '81120', 69, 0, 0, '14:00:00', '23:00:00', '', '9eek', NULL),
(70, 'กระบี่', 'คลองท่อม', 'พรุดินนา', '81120', 70, 0, 0, '14:00:00', '23:00:00', '', '9eek', NULL),
(71, 'กำแพงเพชร', 'ทรายทองวัฒนา', 'ทุ่งทราย', '62190', 71, 0, 0, '10:00:00', '20:00:00', '', 'dfgh', NULL),
(72, 'กำแพงเพชร', 'ทรายทองวัฒนา', 'ทุ่งทราย', '62190', 72, 0, 0, '10:00:00', '20:00:00', '', 'dfgh', NULL),
(73, 'กำแพงเพชร', 'ทรายทองวัฒนา', 'ทุ่งทราย', '62190', 73, 0, 0, '10:00:00', '20:00:00', '', 'dfgh', NULL),
(74, 'กำแพงเพชร', 'ทรายทองวัฒนา', 'ทุ่งทราย', '62190', 74, 0, 0, '10:00:00', '20:00:00', '', 'dfgh', NULL),
(75, 'กรุงเทพมหานคร', 'คลองสามวา', 'สามวาตะวันออก', '10510', 75, 0, 0, '10:00:00', '20:00:00', '', 'dcfg', NULL),
(76, 'กรุงเทพมหานคร', 'คลองสามวา', 'สามวาตะวันออก', '10510', 76, 0, 0, '10:00:00', '20:00:00', '', 'dcfg', NULL),
(77, 'กรุงเทพมหานคร', 'คลองสามวา', 'สามวาตะวันออก', '10510', 77, 0, 0, '10:00:00', '20:00:00', '', 'dcfg', NULL),
(78, 'กรุงเทพมหานคร', 'คลองสามวา', 'สามวาตะวันออก', '10510', 78, 0, 0, '10:00:00', '20:00:00', '', 'dcfg', NULL),
(79, 'กรุงเทพมหานคร', 'คลองสามวา', 'สามวาตะวันออก', '10510', 82, 0, 0, '10:00:00', '20:00:00', '', 'dcfg', NULL),
(80, 'ชัยภูมิ', 'บ้านแท่น', 'บ้านเต่า', '36190', 83, 0, 0, '10:00:00', '20:00:00', '', 'dtryuh', NULL),
(81, 'ชัยภูมิ', 'บ้านแท่น', 'บ้านเต่า', '36190', 84, 0, 0, '10:00:00', '20:00:00', '', 'dtryuh', NULL),
(82, 'ขอนแก่น', 'เมืองขอนแก่น', 'ศิลา', '40000', 85, 0, 0, '10:00:00', '20:00:00', '', 'ergf', NULL),
(83, 'จันทบุรี', 'มะขาม', 'ท่าหลวง', '22150', 86, 0, 0, '10:00:00', '20:00:00', 'สวยเเละดีมาก', 'dfvf', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `store_tag`
--

CREATE TABLE IF NOT EXISTS `store_tag` (
  `store_tag_id` int(11) NOT NULL,
  `store_id` int(11) NOT NULL,
  `tag_id` int(11) NOT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `store_tag`
--

INSERT INTO `store_tag` (`store_tag_id`, `store_id`, `tag_id`, `created_at`) VALUES
(1, 1, 1, '2026-01-08 22:28:27'),
(2, 1, 2, '2026-01-08 22:28:27'),
(3, 3, 3, '2026-01-08 22:28:27');

-- --------------------------------------------------------

--
-- Table structure for table `tag`
--

CREATE TABLE IF NOT EXISTS `tag` (
  `tag_id` int(11) NOT NULL,
  `tag_name` varchar(100) NOT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tag`
--

INSERT INTO `tag` (`tag_id`, `tag_name`, `created_at`) VALUES
(1, 'เพ้นท์มินิมอล', '2026-01-08 22:27:06'),
(2, 'งานหรู', '2026-01-08 22:27:06'),
(3, 'ต่อเล็บ', '2026-01-08 22:27:06'),
(4, 'สปามือเท้า', '2026-01-08 22:27:06'),
(5, 'งานเจ้าสาว', '2026-01-08 22:27:06');

-- --------------------------------------------------------

--
-- Table structure for table `token`
--

CREATE TABLE IF NOT EXISTS `token` (
  `token_id` int(11) NOT NULL,
  `jwt_key` varchar(300) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `expired_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `token`
--

INSERT INTO `token` (`token_id`, `jwt_key`, `user_id`, `created_at`, `expired_at`) VALUES
(1, 'token_abc123', 1, '2025-12-10 13:41:34', '2025-12-17 13:41:34'),
(2, 'token_xyz789', 2, '2025-12-10 13:41:34', '2025-12-17 13:41:34');

-- --------------------------------------------------------

--
-- Table structure for table `type_booking`
--

CREATE TABLE IF NOT EXISTS `type_booking` (
  `type_booking_id` int(11) NOT NULL,
  `type_booking_name` varchar(200) DEFAULT NULL,
  `description` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `type_booking`
--

INSERT INTO `type_booking` (`type_booking_id`, `type_booking_name`, `description`) VALUES
(1, 'normal', 'Normal booking'),
(2, 'walk_in', 'Walk-in customer'),
(3, 'vip', 'VIP booking');

-- --------------------------------------------------------

--
-- Table structure for table `type_promo`
--

CREATE TABLE IF NOT EXISTS `type_promo` (
  `type_promo_id` int(11) NOT NULL,
  `name` varchar(200) DEFAULT NULL,
  `description` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `type_promo`
--

INSERT INTO `type_promo` (`type_promo_id`, `name`, `description`) VALUES
(1, 'discount', 'Percentage discount'),
(2, 'cash', 'Cash discount'),
(3, 'bundle', 'Buy 2 Get 1');

-- --------------------------------------------------------

--
-- Table structure for table `type_service`
--

CREATE TABLE IF NOT EXISTS `type_service` (
  `type_id` int(11) NOT NULL,
  `name` varchar(200) DEFAULT NULL,
  `description` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `type_service`
--

INSERT INTO `type_service` (`type_id`, `name`, `description`) VALUES
(1, 'manicure', 'Hand nail service'),
(2, 'pedicure', 'Foot nail service'),
(3, 'gel_art', 'Gel polish and art'),
(4, 'spa', 'Spa and treatment');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `user_id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `nickname` varchar(100) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `email` varchar(200) DEFAULT NULL,
  `password` varchar(200) DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `username`, `nickname`, `phone`, `email`, `password`, `role_id`, `created_at`, `updated_at`, `deleted_at`) VALUES
(1, 'thanakon01', 'คิตตี้', '081234567', 'golf01@example.com', '123456789', 3, '2025-12-03 13:31:57', '2026-01-18 05:33:44', NULL),
(2, 'supansa02', 'แป้งอ้วน', '0987654321', 'noona02@example.com', 'password123', 3, '2025-12-03 13:31:57', '2026-01-19 01:07:14', NULL),
(3, 'pawat03', 'โบ๊ท', '0812345673', 'pawat03@example.com', 'password123', 3, '2025-12-03 13:31:57', '2025-12-03 13:31:57', NULL),
(4, 'kanyarat04', 'แพน', '0812345674', 'nan04@example.com', 'password123', 3, '2025-12-03 13:31:57', '2025-12-03 13:31:57', NULL),
(5, 'woraphon05', 'โอม', '0812345675', 'oat05@example.com', 'password123', 3, '2025-12-03 13:31:57', '2025-12-03 13:31:57', NULL),
(6, 'sirikul06', 'อิม', '0812345676', 'aom06@example.com', 'password123', 3, '2025-12-03 13:31:57', '2025-12-03 13:31:57', NULL),
(7, 'jakrit07', 'แจ็ค', '0812345677', 'jack07@example.com', 'password123', 2, '2025-12-03 13:31:57', '2025-12-03 13:31:57', NULL),
(8, 'kanokwan08', 'กานต์', '0812345678', 'kan08@example.com', 'password123', 3, '2025-12-03 13:31:57', '2025-12-03 13:31:57', NULL),
(9, 'narong09', 'นาย', '0812345679', 'nai09@example.com', 'password123', 3, '2025-12-03 13:31:57', '2025-12-03 13:31:57', NULL),
(10, 'pitchaya10', 'พีช', '0812345680', 'pit10@example.com', 'password123', 3, '2025-12-03 13:31:57', '2025-12-03 13:31:57', NULL),
(11, 'phudit11', 'ภูดิศ', '0812345681', 'phu11@example.com', 'password123', 2, '2025-12-03 13:31:57', '2025-12-03 13:31:57', NULL),
(12, 'warai12', 'วรา', '0812345682', 'war12@example.com', 'password123', 3, '2025-12-03 13:31:57', '2025-12-03 13:31:57', NULL),
(13, 'kanokporn13', 'พร', '0812345683', 'pair13@example.com', 'password123', 3, '2025-12-03 13:31:57', '2025-12-03 13:31:57', NULL),
(14, 'natdanai14', 'บิ๊ก', '0812345684', 'big14@example.com', 'password123', 3, '2025-12-03 13:31:57', '2025-12-03 13:31:57', NULL),
(15, 'jalisai15', 'ลิสา', '0812345685', 'lisa15@example.com', 'password123', 3, '2025-12-03 13:31:57', '2025-12-03 13:31:57', NULL),
(16, 'pakin16', 'กิ้น', '0812345686', 'top16@example.com', 'password123', 3, '2025-12-03 13:31:57', '2025-12-03 13:31:57', NULL),
(17, 'amalie17', 'แอม', '0812345687', 'am17@example.com', 'password123', 3, '2025-12-03 13:31:57', '2025-12-03 13:31:57', NULL),
(18, 'namnueng18', 'น้ำหนึ่ง', '0812345688', 'nn18@example.com', 'password123', 3, '2025-12-03 13:31:57', '2025-12-03 13:31:57', NULL),
(19, 'tanawat19', 'ต้น', '0812345689', 'ton19@example.com', 'password123', 3, '2025-12-03 13:31:57', '2025-12-03 13:31:57', NULL),
(20, 'sirinya20', 'ซี', '0812345690', 'see20@example.com', 'password123', 3, '2025-12-03 13:31:57', '2025-12-03 13:31:57', NULL),
(21, 'mookw20', 'มุก', '0812345681', 'mook20@example.com', 'password123', 3, '2025-12-13 14:39:12', '2025-12-13 14:39:12', NULL),
(22, 'fernw21', 'เฟิร์น', '0812345682', 'fern21@example.com', 'password123', 3, '2025-12-13 14:39:12', '2025-12-13 14:39:12', NULL),
(23, 'meena22', 'มีนา', '0812345683', 'meena22@example.com', 'password123', 3, '2025-12-13 14:39:12', '2025-12-13 14:39:12', NULL),
(24, 'praew23', 'แพรว', '0812345684', 'praew23@example.com', 'password123', 3, '2025-12-13 14:39:12', '2025-12-13 14:39:12', NULL),
(25, 'ploy24', 'พลอย', '0812345685', 'ploy24@example.com', 'password123', 3, '2025-12-13 14:39:12', '2025-12-13 14:39:12', NULL),
(26, 'amp25', 'แอมป์', '0812345686', 'amp25@example.com', 'password123', 3, '2025-12-13 14:39:12', '2025-12-13 14:39:12', NULL),
(27, 'fon26', 'ฝน', '0812345687', 'fon26@example.com', 'password123', 3, '2025-12-13 14:39:12', '2025-12-13 14:39:12', NULL),
(28, 'nan27', 'แนน', '0812345688', 'nan27@example.com', 'password123', 3, '2025-12-13 14:39:12', '2025-12-13 14:39:12', NULL),
(29, 'nike28', 'ไนซ์', '0812345689', 'nike28@example.com', 'password123', 3, '2025-12-13 14:39:12', '2025-12-13 14:39:12', NULL),
(30, 'mild29', 'มิ้ว', '0812345690', 'mild29@example.com', 'password123', 3, '2025-12-13 14:39:12', '2025-12-13 14:39:12', NULL),
(38, ' ', '', '0646785823', 'chakrit.u@kkumail.com', '123456789', 2, '2026-01-17 01:17:29', '2026-01-17 01:17:29', NULL),
(39, ' ', 'testt', '0828815929', '47chakrit@gmail.com', '123456789', 2, '2026-01-17 01:18:00', '2026-03-26 21:25:14', NULL),
(40, ' ', '', '0828815929', 'kitty@example.com', '123456789', 2, '2026-01-17 01:23:17', '2026-01-17 01:23:17', NULL),
(41, ' ', '', '0646785824', 'suiperrugebark@mail.1com', '123456789', 2, '2026-01-17 01:29:08', '2026-01-17 01:29:08', NULL),
(42, ' ', '', '0646785824', 'suiperrugebark@mail.com', '123456789', 2, '2026-01-17 01:32:35', '2026-01-17 01:32:35', NULL),
(43, ' ', '', '0932162909', 'kk1@mail.com', '123456789', 2, '2026-01-17 01:33:56', '2026-01-17 01:33:56', NULL),
(44, ' ', '', '0932162909', 'kk2@mail.com', '123456789', 2, '2026-01-17 01:35:48', '2026-01-17 01:35:48', NULL),
(45, ' ', '', '0932162909', 'kk@mail.com', '123456789', 2, '2026-01-17 01:38:56', '2026-01-17 01:38:56', NULL),
(46, ' ', '', '0932162909', 'kg@mail.com', '123456789', 2, '2026-01-17 01:40:12', '2026-01-17 01:40:12', NULL),
(47, ' ', '', '0932162909', 'kc@mail.com', '123456789', 2, '2026-01-17 01:41:47', '2026-01-17 01:41:47', NULL),
(48, 'fatimabud makteesu', 'fatimabud', '0932162909', 'kyyyy@mail.com', '123456789', 2, '2026-01-17 01:54:30', '2026-01-17 01:54:30', NULL),
(49, 'fati makteesu', 'fati', '0932162909', 'y@mail.com', '123456789', 1, '2026-01-17 01:56:09', '2026-01-17 01:56:09', NULL),
(50, 'kitty44 sdf', 'kitty44', '0675834567', 'sdfghj@gmail.com', '111222333', 1, '2026-02-08 23:28:50', '2026-02-08 23:28:50', NULL),
(51, 'Doy Doyny', 'Doy', '0981234567', 'Doy123dd@gmail.com', '$2b$12$hqEc9C/E9Z5.Y0WYvkR85ukwaxOJLqJVGLiBXiHZYzpymArqdPtO2', 1, '2026-02-15 17:38:25', '2026-02-15 17:38:25', NULL),
(52, 'chakritkitty kittykt', 'chakritkitty', '0982134567', 'chakritkitty@gmail.com', '$2b$12$I/HhDIzOLI9M92a4FKyqhuWOTIbHAENDh2uOn.I3yrY1glZ6O2d5a', 1, '2026-03-22 23:34:16', '2026-03-22 23:34:16', NULL),
(53, 'Chakrit Uamum', 'Chakrit', '0981234567', 'chakrit.uu@kkumail.com', '$2b$12$He1S4Uy4T/Ng.6eY7MQ2keC/ns8VMvhe6lS99pt31eIO4lEd2RxQ2', 1, '2026-03-22 23:35:30', '2026-03-22 23:35:30', NULL),
(54, 'Chakrit Uamum', 'Chakrit', '098123456', 'chakrit.ukkkkk@kkumail.com', '$2b$12$2M6oElt5Zkzho9QATu5sMOxMIvzav0mlO9uFatUo1TQTICJ6k0V/u', 1, '2026-03-23 00:08:33', '2026-03-23 00:08:33', NULL),
(55, 'Chakritfff Uamumfff', 'Chakritfff', '0981234567', 'chakrit.uf@kkumail.com', '$2b$12$Lbarb1PYRbX2FyUcoyWdcef61Wkl3.NoHa3vd.SPZoJFKx2wQhIQW', 1, '2026-03-23 00:16:18', '2026-03-23 00:16:18', NULL),
(56, 'ggg ggg', 'ggg', '0981234567', 'g@mail.com', '$2b$12$ySzl2rA8bdlxjJf1k/zqt.fRPpD108Ycby.V5Tpb8OlyP6iTQIVrq', 1, '2026-03-23 00:20:56', '2026-03-23 00:20:56', NULL),
(57, 'Chakrit Uamum', 'Chakrit', '0981231234', 'gg@gmail.com', 'scrypt:32768:8:1$bKfOhgOxS5Qxg1pO$1420eb6764cb9d1ca1755c8c1cd5f9e88fa30e184b599438812a7d327b623b1bdc51452c73fc1b1381b729b4320e84d9d028d766c7a40e467a0b700f4a8ec0a9', 1, '2026-03-23 00:26:16', '2026-03-23 00:26:16', NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `address`
--
ALTER TABLE `address`
  ADD PRIMARY KEY (`address_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `bill`
--
ALTER TABLE `bill`
  ADD PRIMARY KEY (`bill_id`),
  ADD KEY `store_id` (`store_id`),
  ADD KEY `status_id` (`status_id`);

--
-- Indexes for table `booking`
--
ALTER TABLE `booking`
  ADD PRIMARY KEY (`booking_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `employee_id` (`employee_id`),
  ADD KEY `store_id` (`store_id`),
  ADD KEY `type_booking_id` (`type_booking_id`),
  ADD KEY `status_id` (`status_id`);

--
-- Indexes for table `bookings`
--
ALTER TABLE `bookings`
  ADD PRIMARY KEY (`booking_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `store_id` (`store_id`),
  ADD KEY `employee_id` (`employee_id`),
  ADD KEY `status_booking_id` (`status_booking_id`),
  ADD KEY `type_booking_id` (`type_booking_id`);

--
-- Indexes for table `booking_services`
--
ALTER TABLE `booking_services`
  ADD PRIMARY KEY (`booking_service_id`),
  ADD KEY `booking_id` (`booking_id`),
  ADD KEY `service_id` (`service_id`);

--
-- Indexes for table `click_log`
--
ALTER TABLE `click_log`
  ADD PRIMARY KEY (`click_log_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `store_id` (`store_id`);

--
-- Indexes for table `employee`
--
ALTER TABLE `employee`
  ADD PRIMARY KEY (`employee_id`),
  ADD KEY `store_id` (`store_id`);

--
-- Indexes for table `favorite`
--
ALTER TABLE `favorite`
  ADD PRIMARY KEY (`favorite_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `store_id` (`store_id`);

--
-- Indexes for table `payment`
--
ALTER TABLE `payment`
  ADD PRIMARY KEY (`payment_id`),
  ADD KEY `booking_id` (`booking_id`),
  ADD KEY `bill_id` (`bill_id`);

--
-- Indexes for table `permission`
--
ALTER TABLE `permission`
  ADD PRIMARY KEY (`permission_id`);

--
-- Indexes for table `promotion`
--
ALTER TABLE `promotion`
  ADD PRIMARY KEY (`promo_id`),
  ADD KEY `store_id` (`store_id`),
  ADD KEY `type_promo_id` (`type_promo_id`);

--
-- Indexes for table `review`
--
ALTER TABLE `review`
  ADD PRIMARY KEY (`review_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `store_id` (`store_id`);

--
-- Indexes for table `role`
--
ALTER TABLE `role`
  ADD PRIMARY KEY (`role_id`);

--
-- Indexes for table `role_permission`
--
ALTER TABLE `role_permission`
  ADD PRIMARY KEY (`role_permission_id`),
  ADD KEY `permission_id` (`permission_id`),
  ADD KEY `role_id` (`role_id`);

--
-- Indexes for table `service`
--
ALTER TABLE `service`
  ADD PRIMARY KEY (`service_id`),
  ADD KEY `store_id` (`store_id`),
  ADD KEY `fk_service_type` (`type_id`);

--
-- Indexes for table `status_booking`
--
ALTER TABLE `status_booking`
  ADD PRIMARY KEY (`status_booking_id`);

--
-- Indexes for table `status_service`
--
ALTER TABLE `status_service`
  ADD PRIMARY KEY (`status_service_id`);

--
-- Indexes for table `status_store`
--
ALTER TABLE `status_store`
  ADD PRIMARY KEY (`status_store_id`);

--
-- Indexes for table `store`
--
ALTER TABLE `store`
  ADD PRIMARY KEY (`store_id`),
  ADD KEY `status_store_id` (`status_store_id`),
  ADD KEY `fk_store_user` (`user_id`);

--
-- Indexes for table `store_address`
--
ALTER TABLE `store_address`
  ADD PRIMARY KEY (`store_address_id`),
  ADD KEY `store_id` (`store_id`);

--
-- Indexes for table `store_tag`
--
ALTER TABLE `store_tag`
  ADD PRIMARY KEY (`store_tag_id`),
  ADD KEY `store_id` (`store_id`),
  ADD KEY `tag_id` (`tag_id`);

--
-- Indexes for table `tag`
--
ALTER TABLE `tag`
  ADD PRIMARY KEY (`tag_id`);

--
-- Indexes for table `token`
--
ALTER TABLE `token`
  ADD PRIMARY KEY (`token_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `type_booking`
--
ALTER TABLE `type_booking`
  ADD PRIMARY KEY (`type_booking_id`);

--
-- Indexes for table `type_promo`
--
ALTER TABLE `type_promo`
  ADD PRIMARY KEY (`type_promo_id`);

--
-- Indexes for table `type_service`
--
ALTER TABLE `type_service`
  ADD PRIMARY KEY (`type_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `role_id` (`role_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `address`
--
ALTER TABLE `address`
  MODIFY `address_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT for table `bill`
--
ALTER TABLE `bill`
  MODIFY `bill_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `booking`
--
ALTER TABLE `booking`
  MODIFY `booking_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `bookings`
--
ALTER TABLE `bookings`
  MODIFY `booking_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=57;

--
-- AUTO_INCREMENT for table `booking_services`
--
ALTER TABLE `booking_services`
  MODIFY `booking_service_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=110;

--
-- AUTO_INCREMENT for table `click_log`
--
ALTER TABLE `click_log`
  MODIFY `click_log_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `employee`
--
ALTER TABLE `employee`
  MODIFY `employee_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=141;

--
-- AUTO_INCREMENT for table `favorite`
--
ALTER TABLE `favorite`
  MODIFY `favorite_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `payment`
--
ALTER TABLE `payment`
  MODIFY `payment_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `permission`
--
ALTER TABLE `permission`
  MODIFY `permission_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `promotion`
--
ALTER TABLE `promotion`
  MODIFY `promo_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `review`
--
ALTER TABLE `review`
  MODIFY `review_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=257;

--
-- AUTO_INCREMENT for table `role`
--
ALTER TABLE `role`
  MODIFY `role_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `role_permission`
--
ALTER TABLE `role_permission`
  MODIFY `role_permission_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `service`
--
ALTER TABLE `service`
  MODIFY `service_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=531;

--
-- AUTO_INCREMENT for table `status_booking`
--
ALTER TABLE `status_booking`
  MODIFY `status_booking_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `status_service`
--
ALTER TABLE `status_service`
  MODIFY `status_service_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `status_store`
--
ALTER TABLE `status_store`
  MODIFY `status_store_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `store`
--
ALTER TABLE `store`
  MODIFY `store_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=87;

--
-- AUTO_INCREMENT for table `store_address`
--
ALTER TABLE `store_address`
  MODIFY `store_address_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=84;

--
-- AUTO_INCREMENT for table `store_tag`
--
ALTER TABLE `store_tag`
  MODIFY `store_tag_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `tag`
--
ALTER TABLE `tag`
  MODIFY `tag_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `token`
--
ALTER TABLE `token`
  MODIFY `token_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `type_booking`
--
ALTER TABLE `type_booking`
  MODIFY `type_booking_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `type_promo`
--
ALTER TABLE `type_promo`
  MODIFY `type_promo_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `type_service`
--
ALTER TABLE `type_service`
  MODIFY `type_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=58;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `address`
--
ALTER TABLE `address`
  ADD CONSTRAINT `address_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

--
-- Constraints for table `bill`
--
ALTER TABLE `bill`
  ADD CONSTRAINT `bill_ibfk_1` FOREIGN KEY (`store_id`) REFERENCES `store` (`store_id`),
  ADD CONSTRAINT `bill_ibfk_2` FOREIGN KEY (`status_id`) REFERENCES `status_store` (`status_store_id`);

--
-- Constraints for table `booking`
--
ALTER TABLE `booking`
  ADD CONSTRAINT `booking_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  ADD CONSTRAINT `booking_ibfk_2` FOREIGN KEY (`employee_id`) REFERENCES `employee` (`employee_id`),
  ADD CONSTRAINT `booking_ibfk_3` FOREIGN KEY (`store_id`) REFERENCES `store` (`store_id`),
  ADD CONSTRAINT `booking_ibfk_4` FOREIGN KEY (`type_booking_id`) REFERENCES `type_booking` (`type_booking_id`),
  ADD CONSTRAINT `booking_ibfk_5` FOREIGN KEY (`status_id`) REFERENCES `status_booking` (`status_booking_id`);

--
-- Constraints for table `bookings`
--
ALTER TABLE `bookings`
  ADD CONSTRAINT `bookings_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  ADD CONSTRAINT `bookings_ibfk_2` FOREIGN KEY (`store_id`) REFERENCES `store` (`store_id`),
  ADD CONSTRAINT `bookings_ibfk_3` FOREIGN KEY (`employee_id`) REFERENCES `employee` (`employee_id`),
  ADD CONSTRAINT `bookings_ibfk_4` FOREIGN KEY (`status_booking_id`) REFERENCES `status_booking` (`status_booking_id`),
  ADD CONSTRAINT `bookings_ibfk_5` FOREIGN KEY (`type_booking_id`) REFERENCES `type_booking` (`type_booking_id`);

--
-- Constraints for table `booking_services`
--
ALTER TABLE `booking_services`
  ADD CONSTRAINT `booking_services_ibfk_1` FOREIGN KEY (`booking_id`) REFERENCES `bookings` (`booking_id`),
  ADD CONSTRAINT `booking_services_ibfk_2` FOREIGN KEY (`service_id`) REFERENCES `service` (`service_id`);

--
-- Constraints for table `click_log`
--
ALTER TABLE `click_log`
  ADD CONSTRAINT `click_log_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  ADD CONSTRAINT `click_log_ibfk_2` FOREIGN KEY (`store_id`) REFERENCES `store` (`store_id`);

--
-- Constraints for table `employee`
--
ALTER TABLE `employee`
  ADD CONSTRAINT `employee_ibfk_1` FOREIGN KEY (`store_id`) REFERENCES `store` (`store_id`);

--
-- Constraints for table `favorite`
--
ALTER TABLE `favorite`
  ADD CONSTRAINT `favorite_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  ADD CONSTRAINT `favorite_ibfk_2` FOREIGN KEY (`store_id`) REFERENCES `store` (`store_id`);

--
-- Constraints for table `payment`
--
ALTER TABLE `payment`
  ADD CONSTRAINT `payment_ibfk_1` FOREIGN KEY (`booking_id`) REFERENCES `booking` (`booking_id`),
  ADD CONSTRAINT `payment_ibfk_2` FOREIGN KEY (`bill_id`) REFERENCES `bill` (`bill_id`);

--
-- Constraints for table `promotion`
--
ALTER TABLE `promotion`
  ADD CONSTRAINT `promotion_ibfk_1` FOREIGN KEY (`store_id`) REFERENCES `store` (`store_id`),
  ADD CONSTRAINT `promotion_ibfk_2` FOREIGN KEY (`type_promo_id`) REFERENCES `type_promo` (`type_promo_id`);

--
-- Constraints for table `review`
--
ALTER TABLE `review`
  ADD CONSTRAINT `review_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  ADD CONSTRAINT `review_ibfk_2` FOREIGN KEY (`store_id`) REFERENCES `store` (`store_id`);

--
-- Constraints for table `role_permission`
--
ALTER TABLE `role_permission`
  ADD CONSTRAINT `role_permission_ibfk_1` FOREIGN KEY (`permission_id`) REFERENCES `permission` (`permission_id`),
  ADD CONSTRAINT `role_permission_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `role` (`role_id`);

--
-- Constraints for table `service`
--
ALTER TABLE `service`
  ADD CONSTRAINT `fk_service_type` FOREIGN KEY (`type_id`) REFERENCES `type_service` (`type_id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `service_ibfk_1` FOREIGN KEY (`type_id`) REFERENCES `type_service` (`type_id`),
  ADD CONSTRAINT `service_ibfk_2` FOREIGN KEY (`store_id`) REFERENCES `store` (`store_id`);

--
-- Constraints for table `store`
--
ALTER TABLE `store`
  ADD CONSTRAINT `fk_store_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `store_ibfk_1` FOREIGN KEY (`status_store_id`) REFERENCES `status_store` (`status_store_id`);

--
-- Constraints for table `store_address`
--
ALTER TABLE `store_address`
  ADD CONSTRAINT `store_address_ibfk_1` FOREIGN KEY (`store_id`) REFERENCES `store` (`store_id`);

--
-- Constraints for table `store_tag`
--
ALTER TABLE `store_tag`
  ADD CONSTRAINT `store_tag_ibfk_1` FOREIGN KEY (`store_id`) REFERENCES `store` (`store_id`),
  ADD CONSTRAINT `store_tag_ibfk_2` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`tag_id`);

--
-- Constraints for table `token`
--
ALTER TABLE `token`
  ADD CONSTRAINT `token_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

--
-- Constraints for table `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `role` (`role_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
