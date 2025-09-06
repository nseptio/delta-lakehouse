import logging
import os

import duckdb
import psycopg
from dotenv import load_dotenv

from src.utils.logging import setup_logging

load_dotenv()
setup_logging()

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Make sure PostgreSQL built-in environment variables are set
    # see doc: https://www.postgresql.org/docs/current/libpq-envars.html
    conn_pg = psycopg.connect("")
    cur = conn_pg.cursor()

    # Fix schema file path
    schema_path = os.path.join(
        os.path.dirname(__file__), "../../schemas/siak_schema.sql"
    )
    with open(schema_path) as f:
        schema_sql = f.read()

    cur.execute(schema_sql)
    conn_pg.commit()
    logger.info("Database schema created successfully.")

    cur.close()
    conn_pg.close()
    logger.info("Database connection closed.")

    # Load parquet files into PostgreSQL with DuckDB
    con = duckdb.connect(database=":memory:")
    con.execute("INSTALL postgres;")
    con.execute("LOAD postgres;")

    # DuckDB will also use PostgreSQL env vars
    con.execute("ATTACH DATABASE '' AS duck_siak (TYPE POSTGRES);")

    # Since we'll seed data into PostgreSQL, a relational database, that has foreign key constraints,
    # we need to insert data in the correct order.
    tables = [
        "faculties",
        "programs",
        "lecturers",
        "students",
        "rooms",
        "courses",
        "semesters",
        "class_schedules",
        "registrations",
        "grades",
        "semester_fees",
        "academic_records",
    ]

    # Get the data directory path relative to this script
    data_dir = os.path.join(os.path.dirname(__file__), "../../data/generated")

    for table in tables:
        parquet_file = os.path.join(data_dir, f"{table}.parquet")
        con.execute(
            f"INSERT INTO duck_siak.{table} SELECT * FROM parquet_scan('{parquet_file}')"
        )
        logger.info(f"Loaded {table} from {parquet_file}")
