SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

CREATE TABLE IF NOT EXISTS `price`  (
  `exchange_id` smallint(5) UNSIGNED NOT NULL,
  `symbol` varchar(20) NOT NULL,
  `harmonized_symbol` varchar(20) NOT NULL,
  `price` decimal(24,14) NOT NULL,
  `bid` decimal(24,14) NOT NULL,
  `ask` decimal(24,14) NOT NULL,
  `bidqty` decimal(24,14) NOT NULL,
  `askqty` decimal(24,14) NOT NULL,
  `volume` decimal(24,14) NOT NULL,
  `prevDay` decimal(8,2) NOT NULL DEFAULT 0.00,
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

COMMIT;
