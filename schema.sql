DROP TABLE IF EXISTS jobs, filaments;

CREATE TABLE jobs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  job TEXT NOT NULL,
  color TEXT NOT NULL,
  submitted_by TEXT NOT NULL,
  completed BOOLEAN,
  deleted BOOLEAN,
  completed_on TIMESTAMP,
  deleted_on TIMESTAMP,
  comments TEXT
)
