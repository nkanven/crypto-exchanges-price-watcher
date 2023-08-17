

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


CREATE TABLE `price` (
  `birza` smallint(5) UNSIGNED NOT NULL,
  `symbol` varchar(20) NOT NULL,
  `price` decimal(24,14) NOT NULL,
  `prevDay` decimal(8,2) NOT NULL DEFAULT 0.00,
  `last_update` int(10) UNSIGNED NOT NULL DEFAULT unix_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `price_history_1d` (
  `birza` smallint(5) UNSIGNED NOT NULL,
  `symbol` varchar(20) NOT NULL,
  `date_day` date NOT NULL DEFAULT current_timestamp(),
  `price` decimal(24,14) UNSIGNED NOT NULL DEFAULT 0.00000000000000
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `price_history_1h` (
  `birza` smallint(5) UNSIGNED NOT NULL,
  `symbol` varchar(20) NOT NULL,
  `hour` tinyint(3) UNSIGNED NOT NULL DEFAULT date_format(current_timestamp(),'%H'),
  `price` decimal(24,14) UNSIGNED NOT NULL DEFAULT 0.00000000000000,
  `last_update` int(10) UNSIGNED NOT NULL DEFAULT unix_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `price_history_1m` (
  `birza` smallint(5) UNSIGNED NOT NULL,
  `symbol` varchar(20) NOT NULL,
  `minut` varchar(5) NOT NULL DEFAULT date_format(current_timestamp(),'%H:%i'),
  `price` decimal(24,14) UNSIGNED NOT NULL DEFAULT 0.00000000000000,
  `last_update` int(10) UNSIGNED NOT NULL DEFAULT unix_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `price_history_10m` (
  `birza` smallint(5) UNSIGNED NOT NULL,
  `symbol` varchar(20) NOT NULL,
  `minut` varchar(5) NOT NULL DEFAULT concat(substr(date_format(current_timestamp(),'%H:%i'),1,4),'0'),
  `price` decimal(24,14) UNSIGNED NOT NULL DEFAULT 0.00000000000000,
  `last_update` int(10) UNSIGNED NOT NULL DEFAULT unix_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


ALTER TABLE `price`
  ADD PRIMARY KEY (`birza`,`symbol`) USING BTREE;


ALTER TABLE `price_history_1d`
  ADD PRIMARY KEY (`birza`,`symbol`,`date_day`),
  ADD KEY `birza` (`birza`),
  ADD KEY `symbol` (`symbol`),
  ADD KEY `date_day` (`date_day`);


ALTER TABLE `price_history_1h`
  ADD PRIMARY KEY (`birza`,`hour`,`symbol`) USING BTREE,
  ADD KEY `symbol` (`symbol`),
  ADD KEY `last_update` (`last_update`),
  ADD KEY `birza` (`birza`);


ALTER TABLE `price_history_1m`
  ADD PRIMARY KEY (`birza`,`symbol`,`minut`) USING BTREE,
  ADD KEY `last_update` (`last_update`),
  ADD KEY `symbol` (`symbol`),
  ADD KEY `birza` (`birza`);


ALTER TABLE `price_history_10m`
  ADD PRIMARY KEY (`birza`,`minut`,`symbol`) USING BTREE,
  ADD KEY `last_update` (`last_update`),
  ADD KEY `symbol` (`symbol`),
  ADD KEY `birza` (`birza`);
COMMIT;
