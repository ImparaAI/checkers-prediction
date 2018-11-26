BEGIN;
CREATE TABLE IF NOT EXISTS training_sessions (
  id INTEGER PRIMARY KEY,
  name varchar(100) NOT NULL,
  episodeCount int unsigned NOT NULL DEFAULT 0,
  episodeLimit int unsigned NULL DEFAULT NULL,
  secondsLimit int unsigned NULL DEFAULT NULL,
  deactivated tinyint NOT NULL DEFAULT 0,
  startTime datetime NULL DEFAULT NULL,
  endTime datetime NULL DEFAULT NULL,
  createdAt timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS training_sessions_time ON training_sessions (startTime, endTime, deactivated);

CREATE TABLE IF NOT EXISTS tournaments (
  id INTEGER PRIMARY KEY,
  player1 varchar(100) NOT NULL,
  player2 varchar(100) NOT NULL,
  episodeCount int unsigned NOT NULL DEFAULT 0,
  player1_win_count int unsigned NOT NULL DEFAULT 0,
  player2_win_count int unsigned NOT NULL DEFAULT 0,
  draw_count int unsigned NOT NULL DEFAULT 0,
  startTime datetime NULL DEFAULT NULL,
  endTime datetime NULL DEFAULT NULL,
  createdAt timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);
COMMIT;