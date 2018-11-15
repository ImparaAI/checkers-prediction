CREATE DATABASE IF NOT EXISTS prediction;

CREATE TABLE IF NOT EXISTS prediction.training_sessions (
  id int(11) unsigned NOT NULL AUTO_INCREMENT,
  name varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  episodeCount int(11) unsigned NOT NULL DEFAULT 0,
  episodeLimit int(11) unsigned NULL DEFAULT NULL,
  secondsLimit int(11) unsigned NULL DEFAULT NULL,
  deactivated tinyint(1) NOT NULL DEFAULT 0,
  startTime datetime NULL DEFAULT NULL,
  endTime datetime NULL DEFAULT NULL,
  createdAt timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `time` (`startTime`, `endTime`, `deactivated`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;