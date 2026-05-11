CREATE KEYSPACE IF NOT EXISTS agile_data_science
  WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

CREATE TABLE IF NOT EXISTS agile_data_science.origin_dest_distances (
    origin   TEXT,
    dest     TEXT,
    distance DOUBLE,
    PRIMARY KEY (origin, dest)
);

CREATE TABLE IF NOT EXISTS agile_data_science.flight_delay_ml_response (
    uuid       TEXT PRIMARY KEY,
    origin     TEXT,
    dest       TEXT,
    carrier    TEXT,
    depdelay   DOUBLE,
    prediction DOUBLE,
    timestamp  TIMESTAMP
);
