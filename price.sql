SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

CREATE TABLE IF NOT EXISTS `price`  (
  `exchange_id` smallint(5) UNSIGNED NOT NULL,
  `symbol` varchar(20) NOT NULL,
  `harmonized_symbol` varchar(20) NOT NULL,
  `price` varchar(50) NOT NULL,
  `bid` varchar(50) NOT NULL,
  `ask` varchar(50) NOT NULL,
  `bidqty` varchar(50) NOT NULL,
  `askqty` varchar(50) NOT NULL,
  `volume` varchar(50) NOT NULL,
  `prevDay` varchar(50) NOT NULL DEFAULT 0.00,
  `last_update` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `price_history_1m`  (
  `exchange_id` smallint(5) UNSIGNED NOT NULL,
  `symbol` varchar(20) NOT NULL,
  `harmonized_symbol` varchar(20) NOT NULL,
  `minut` varchar(5) NOT NULL,
  `price` varchar(50) NOT NULL DEFAULT '0.00000000000000',
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
  ADD PRIMARY KEY (`exchange_id`,`time_create`),
  ADD KEY `exchange_id` (`exchange_id`),
  ADD KEY `time_create` (`time_create`);


ALTER TABLE `price_history_1m`
  ADD PRIMARY KEY (`exchange_id`,`symbol`,`minut`) USING BTREE,
  ADD KEY `last_update` (`last_update`),
  ADD KEY `symbol` (`symbol`),
  ADD KEY `exchange_id` (`exchange_id`);

COMMIT;
