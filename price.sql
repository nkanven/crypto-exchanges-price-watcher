

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

CREATE TABLE IF NOT EXISTS `price`  (
  `exchange_id` smallint(5) UNSIGNED NOT NULL,
  `symbol` varchar(20) NOT NULL,
  `symbol` varchar(20) NOT NULL,
  `harmonized_symbol` varchar(20) NOT NULL,
  `price` decimal(24,14) NOT NULL,
  `prevDay` decimal(8,2) NOT NULL DEFAULT 0.00,
  `last_update` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



CREATE TABLE IF NOT EXISTS `price_history_1m`  (
  `exchange_id` smallint(5) UNSIGNED NOT NULL,
  `symbol` varchar(20) NOT NULL,
  `harmonized_symbol` varchar(20) NOT NULL,
  `minut` varchar(5) NOT NULL,
  `price` decimal(24,14) UNSIGNED NOT NULL DEFAULT 0.00000000000000,
  `last_update` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE IF NOT EXISTS `price_history_1d` (
  `exchange_id` smallint(5) UNSIGNED NOT NULL,
  `symbol` varchar(20) NOT NULL,
  `date_day` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `price` decimal(24,14) UNSIGNED NOT NULL DEFAULT 0.00000000000000
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE IF NOT EXISTS `price_history_1h`  (
  `exchange_id` smallint(5) UNSIGNED NOT NULL,
  `symbol` varchar(20) NOT NULL,
  `hour` tinyint(2) UNSIGNED NOT NULL,
  `price` decimal(24,14) UNSIGNED NOT NULL DEFAULT 0.00000000000000,
  `last_update` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE IF NOT EXISTS `price_history_10m`  (
  `exchange_id` smallint(5) UNSIGNED NOT NULL,
  `symbol` varchar(20) NOT NULL,
  `minut` varchar(5) NOT NULL,
  `price` decimal(24,14) UNSIGNED NOT NULL DEFAULT 0.00000000000000,
  `last_update` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `log`  (
  `exchange_id` smallint(5) UNSIGNED NOT NULL,
  `message` text NOT NULL,
  `time_create` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


ALTER TABLE `price`
  ADD PRIMARY KEY (`exchange_id`,`symbol`) USING BTREE;


ALTER TABLE `log`
  ADD PRIMARY KEY (`exchange_id`,`message`,`time_create`),
  ADD KEY `exchange_id` (`exchange_id`),
  ADD KEY `message` (`message`),
  ADD KEY `time_create` (`time_create`);


ALTER TABLE `price_history_1d`
  ADD PRIMARY KEY (`exchange_id`,`symbol`,`date_day`),
  ADD KEY `exchange_id` (`exchange_id`),
  ADD KEY `symbol` (`symbol`),
  ADD KEY `date_day` (`date_day`);


ALTER TABLE `price_history_1h`
  ADD PRIMARY KEY (`exchange_id`,`hour`,`symbol`) USING BTREE,
  ADD KEY `symbol` (`symbol`),
  ADD KEY `last_update` (`last_update`),
  ADD KEY `exchange_id` (`exchange_id`);


ALTER TABLE `price_history_1m`
  ADD PRIMARY KEY (`exchange_id`,`symbol`,`minut`) USING BTREE,
  ADD KEY `last_update` (`last_update`),
  ADD KEY `symbol` (`symbol`),
  ADD KEY `exchange_id` (`exchange_id`);


ALTER TABLE `price_history_10m`
  ADD PRIMARY KEY (`exchange_id`,`minut`,`symbol`) USING BTREE,
  ADD KEY `last_update` (`last_update`),
  ADD KEY `symbol` (`symbol`),
  ADD KEY `exchange_id` (`exchange_id`);
COMMIT;
