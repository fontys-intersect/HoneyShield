-- phpMyAdmin SQL Dump
-- version 4.9.5deb2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: May 10, 2023 at 10:43 AM
-- Server version: 8.0.33-0ubuntu0.20.04.1
-- PHP Version: 7.4.3-4ubuntu2.18

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `Honeypot`
--

-- --------------------------------------------------------

--
-- Table structure for table `Attackers`
--

CREATE TABLE `Attackers` (
  `id` int NOT NULL,
  `ip` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Attacks`
--

CREATE TABLE `Attacks` (
  `id` int NOT NULL,
  `attackerId` int NOT NULL,
  `src_ip` varchar(50) DEFAULT NULL,
  `src_port` int DEFAULT NULL,
  `dest_ip` varchar(50) DEFAULT NULL,
  `dest_port` int DEFAULT NULL,
  `pub_ip` varchar(50) DEFAULT NULL,
  `data_type` varchar(50) DEFAULT NULL,
  `request` text,
  `response` text,
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Duration`
--

CREATE TABLE `Duration` (
  `id` int NOT NULL,
  `attackerId` int NOT NULL,
  `duration` time NOT NULL,
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Ip_reputation`
--

CREATE TABLE `Ip_reputation` (
  `id` int NOT NULL,
  `attackerId` int NOT NULL,
  `reputation` int DEFAULT NULL,
  `countryCode` varchar(4) DEFAULT NULL,
  `city` varchar(20) DEFAULT NULL,
  `latitude` decimal(10,3) DEFAULT NULL,
  `longitude` decimal(11,3) DEFAULT NULL,
  `is_crawler` tinyint(1) NOT NULL,
  `proxy` tinyint(1) NOT NULL,
  `vpn` tinyint(1) NOT NULL,
  `tor` tinyint(1) NOT NULL,
  `recent_abuse` tinyint(1) NOT NULL,
  `bot_status` tinyint(1) NOT NULL,
  `timestamp` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Protocols`
--

CREATE TABLE `Protocols` (
  `id` int NOT NULL,
  `attackerId` int NOT NULL,
  `protocols` json NOT NULL,
  `amount` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Seriousness_score`
--

CREATE TABLE `Seriousness_score` (
  `id` int NOT NULL,
  `attackerId` int NOT NULL,
  `score` int DEFAULT NULL,
  `timestamp` timestamp NULL,
  `iprep_score` int NOT NULL,
  `duration_score` int NOT NULL,
  `protocols_score` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Settings`
--

CREATE TABLE `Settings` (
  `global` json NOT NULL,
  `category_weights` json NOT NULL,
  `protocol_weights` json NOT NULL,
  `iprep_percentage_to_level` json NOT NULL,
  `protocols_percentage_to_level` json NOT NULL,
  `duration_seconds_to_level` json NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `Settings`
--

INSERT INTO `Settings` (`global`, `category_weights`, `protocol_weights`, `iprep_percentage_to_level`, `protocols_percentage_to_level`, `duration_seconds_to_level`) VALUES
('{\"rep_exp\": 1, \"attacktime_threshold\": 5, \"calc_score_threshold\": 1}', '{\"duration\": 0.33333, \"protocols\": 0.33333, \"reputation\": 0.33333}', '{\"ftp\": 1, \"enip\": 3, \"http\": 1, \"snmp\": 4, \"tftp\": 2, \"bacnet\": 5, \"modbus\": 5, \"s7comm\": 5}', '{\"level1\": 20, \"level2\": 40, \"level3\": 60, \"level4\": 80}', '{\"level1\": 20, \"level2\": 40, \"level3\": 60, \"level4\": 80}', '{\"level1\": 600, \"level2\": 1200, \"level3\": 1800, \"level4\": 2400}');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Attackers`
--
ALTER TABLE `Attackers`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `IP` (`ip`);

--
-- Indexes for table `Attacks`
--
ALTER TABLE `Attacks`
  ADD PRIMARY KEY (`id`),
  ADD KEY `attackerId` (`attackerId`);

--
-- Indexes for table `Duration`
--
ALTER TABLE `Duration`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `attackerId` (`attackerId`);

--
-- Indexes for table `Ip_reputation`
--
ALTER TABLE `Ip_reputation`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `attackerId` (`attackerId`);

--
-- Indexes for table `Protocols`
--
ALTER TABLE `Protocols`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `attackerId_2` (`attackerId`),
  ADD KEY `attackerId` (`attackerId`);

--
-- Indexes for table `Seriousness_score`
--
ALTER TABLE `Seriousness_score`
  ADD PRIMARY KEY (`id`),
  ADD KEY `attackerId` (`attackerId`) USING BTREE;

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Attackers`
--
ALTER TABLE `Attackers`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `Attacks`
--
ALTER TABLE `Attacks`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `Duration`
--
ALTER TABLE `Duration`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `Ip_reputation`
--
ALTER TABLE `Ip_reputation`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `Protocols`
--
ALTER TABLE `Protocols`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `Seriousness_score`
--
ALTER TABLE `Seriousness_score`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Attacks`
--
ALTER TABLE `Attacks`
  ADD CONSTRAINT `Attacks_ibfk_1` FOREIGN KEY (`attackerId`) REFERENCES `Attackers` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `Duration`
--
ALTER TABLE `Duration`
  ADD CONSTRAINT `Duration_ibfk_1` FOREIGN KEY (`attackerId`) REFERENCES `Attackers` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `Ip_reputation`
--
ALTER TABLE `Ip_reputation`
  ADD CONSTRAINT `Ip_reputation_ibfk_1` FOREIGN KEY (`attackerId`) REFERENCES `Attackers` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `Protocols`
--
ALTER TABLE `Protocols`
  ADD CONSTRAINT `Protocols_ibfk_1` FOREIGN KEY (`attackerId`) REFERENCES `Attackers` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `Seriousness_score`
--
ALTER TABLE `Seriousness_score`
  ADD CONSTRAINT `Seriousness_score_ibfk_1` FOREIGN KEY (`attackerId`) REFERENCES `Attackers` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
