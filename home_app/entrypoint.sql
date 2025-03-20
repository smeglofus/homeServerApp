-- Vytvoření tabulky pro ukládání dat senzorů
CREATE TABLE IF NOT EXISTS fermentator_sensordata (
    id SERIAL PRIMARY KEY,
    temperature FLOAT NOT NULL,
    humidity FLOAT NOT NULL,
    desired_temp FLOAT NOT NULL,
    timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
