import logging

from duckdb import DuckDBPyConnection

logger = logging.getLogger(__name__)

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


def extract(duck: DuckDBPyConnection):
    logger.info("🚀 Starting ETL Extract Process")

    # Extract PostgreSQL to DuckDB before transform process
    logger.info("Extracting data from PostgreSQL")
    for table in tables:
        query = f"CREATE TABLE IF NOT EXISTS {table} AS SELECT * FROM p_siak.{table}"
        duck.execute(query)

    # Verify data extraction (just for logging)
    logger.info("📊 Data extraction summary:")
    for table in tables:
        count = duck.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        logger.info(f"   - {table}: {count:,} rows")
