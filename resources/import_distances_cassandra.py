#!/usr/bin/env python
"""
Reads data/origin_dest_distances.jsonl and loads it into Cassandra.
Creates the keyspace and table if they don't exist.

Usage:
    python resources/import_distances_cassandra.py
"""

import json
import os
from cassandra.cluster import Cluster
from cassandra.policies import RoundRobinPolicy

CASSANDRA_HOST = os.environ.get("CASSANDRA_HOST", "localhost")
CASSANDRA_PORT = int(os.environ.get("CASSANDRA_PORT", 9042))
DISTANCES_FILE = os.path.join(os.path.dirname(__file__), "../data/origin_dest_distances.jsonl")

def get_session():
    cluster = Cluster(
        [CASSANDRA_HOST],
        port=CASSANDRA_PORT,
        load_balancing_policy=RoundRobinPolicy()
    )
    return cluster.connect()

def create_schema(session):
    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS agile_data_science
        WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}
    """)
    session.set_keyspace("agile_data_science")
    session.execute("""
        CREATE TABLE IF NOT EXISTS origin_dest_distances (
            origin   TEXT,
            dest     TEXT,
            distance DOUBLE,
            PRIMARY KEY (origin, dest)
        )
    """)
    print("Keyspace and table ready.")

def load_distances(session):
    insert_stmt = session.prepare("""
        INSERT INTO origin_dest_distances (origin, dest, distance)
        VALUES (?, ?, ?)
    """)

    count = 0
    with open(DISTANCES_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            session.execute(insert_stmt, (
                record["Origin"],
                record["Dest"],
                float(record["Distance"])
            ))
            count += 1

    print(f"Inserted {count} distance records into Cassandra.")

if __name__ == "__main__":
    session = get_session()
    create_schema(session)
    load_distances(session)
    session.shutdown()
