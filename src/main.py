import logging
import os

import duckdb
from dotenv import load_dotenv

from pipeline.extract import extract
from pipeline.load_delta import load_delta
from pipeline.load_iceberg import load_iceberg
from pipeline.transform import transform
from utils.logging import setup_logging

load_dotenv()
setup_logging()

logger = logging.getLogger(__name__)


def main():
    logger.info("🚀 Starting ETL Pipeline")
    os.makedirs("data/duckdb", exist_ok=True)

    logger.info("🔌 Connecting to DuckDB...")
    db_con: duckdb.DuckDBPyConnection = duckdb.connect(
        database="data/duckdb/siak.duckdb"
    )

    logger.info("📦 Installing PostgreSQL extension...")
    db_con.execute("INSTALL postgres;")
    db_con.execute("LOAD postgres;")

    logger.info("🔗 Attaching to PostgreSQL database...")
    db_con.execute("ATTACH DATABASE '' AS p_siak (TYPE POSTGRES, READ_ONLY);")

    logger.info("📥 Extracting data...")
    extract(db_con)

    logger.info("🔄 Transforming data...")
    transform(db_con)

    logger.info("📤 Loading data with Delta table...")
    load_delta(db_con)

    logger.info("📤 Loading data with Iceberg table...")
    load_iceberg(db_con)

    db_con.close()
    logger.info("✅ ETL Pipeline completed successfully!")


if __name__ == "__main__":
    main()
