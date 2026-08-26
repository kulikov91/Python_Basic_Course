-- Выполнить внутри базы farm_market.
CREATE TABLE IF NOT EXISTS markets (
    fmid VARCHAR(30) PRIMARY KEY,
    data JSONB NOT NULL
);

CREATE TABLE IF NOT EXISTS reviews (
    id SERIAL PRIMARY KEY,
    fmid VARCHAR(30) NOT NULL REFERENCES markets(fmid) ON DELETE CASCADE,
    name TEXT NOT NULL,
    review TEXT NOT NULL DEFAULT '',
    rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5)
);

CREATE TABLE IF NOT EXISTS zip_coordinates (
    zip_code VARCHAR(10) PRIMARY KEY,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL
);
