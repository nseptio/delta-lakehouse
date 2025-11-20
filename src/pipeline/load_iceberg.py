import logging
import os

from duckdb import DuckDBPyConnection
from pyiceberg.catalog import load_catalog

import schemas.delta_schema as delta_schema
import schemas.iceberg_schema as iceberg_schema

logger = logging.getLogger(__name__)

# TODO: duplicate with delta_schema.py file
ICEBERG_TABLES = [
    "dim_student",
    "dim_course",
    "dim_lecturer",
    "dim_semester",
    "dim_class",
    "dim_room",
    "fact_registration",
    "fact_grade",
    "fact_fee",
    "fact_academic",
    # "fact_attendence",
    "fact_teaching",
    "fact_room_usage",
]


def create_iceberg_tables(catalog):
    logger.info("Creating Iceberg tables in object storage via Postgres catalog")
    for table_name in ICEBERG_TABLES:
        try:
            catalog.create_table_if_not_exists(
                #  better to make schema as parameter instead of hard coded like this
                identifier=f"siak.{table_name}",
                schema=iceberg_schema.get_schema(table_name),
            )
            logger.info(f"✅ Created Iceberg table: {table_name}")
        except Exception as e:
            logger.error(f"❌ Failed to create Iceberg table: {e}")


def load_to_iceberg_tables(catalog, duck: DuckDBPyConnection):
    for table_name in ICEBERG_TABLES:
        try:
            data_arrow = duck.sql(f"SELECT * FROM {table_name}").arrow()
            data_arrow = data_arrow.cast(delta_schema.get_schema(table_name))
            table = catalog.load_table(f"siak.{table_name}")
            table.append(data_arrow)
            logger.info(f"✅ Data appended to Iceberg table: {table}")
        except Exception as e:
            logger.error(f"❌ Failed to load data table {table_name}: {e}")


def load_iceberg(duck: DuckDBPyConnection):
    logger.info("🏔️ Starting Load Pipeline with Iceberg")
    logger.info("🔌 Setup catalog configuration")
    os.environ["PYICEBERG_HOME"] = os.getcwd()  # cwd: current working directory
    print(os.getenv("PYICEBERG_HOME"))

    catalog = load_catalog(name="postgres")
    print(catalog.properties)

    namespace = "siak"
    logger.info("Creaing Iceberg namespace: " + namespace)
    catalog.create_namespace_if_not_exists(namespace)

    logger.info("🏗️  Creating Iceberg table schemas...")
    create_iceberg_tables(catalog)

    # load data to Iceberg table
    logger.info("📥 Loading data into Iceberg tables...")
    load_to_iceberg_tables(catalog, duck)

    logger.info("🎉 Load Pipeline completed successfully!")
