-- create_table.sql

CREATE TABLE IF NOT EXISTS iot_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp INTEGER,
    topic TEXT,
    payload TEXT
);
