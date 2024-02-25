-- -----------------
-- NOT USED 
--
-- SQL statement to create sqlite database table
-- 
-- -----------------

CREATE TABLE IF NOT EXISTS smart_home_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time_of_day INTEGER,
    total_light_intensity INTEGER,
    total_energy_consumption INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
