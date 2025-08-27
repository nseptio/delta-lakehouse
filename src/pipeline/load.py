import logging

from deltalake import DeltaTable, write_deltalake
from duckdb import DuckDBPyConnection

import delta_schema
from utils.config import Config
from utils.minio import ensure_bucket, get_minio_client

logger = logging.getLogger(__name__)

# MinIO bucket and Delta table paths
MINIO_BUCKET = "lakehouse"
DELTA_TABLES = [
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


def create_delta_tables(cfg: dict):
    """Create Delta Lake tables in MinIO with predefined schemas"""
    logger.info("Creating Delta Lake tables in MinIO")

    for table_name in DELTA_TABLES:
        try:
            schema = delta_schema.get_schema(table_name)
            table_uri = f"s3://{MINIO_BUCKET}/{table_name}"

            # Create Delta table in MinIO
            DeltaTable.create(
                table_uri=table_uri,
                schema=schema,
                mode="overwrite",
                storage_options=cfg,
            )

            logger.info(f"✅ Created Delta table: {table_name}")
            logger.info(f"   URI: {table_uri}")
            logger.info(f"   Schema: {len(schema)} fields")

        except Exception as e:
            logger.error(f"❌ Failed to create {table_name}: {e}")

    logger.info("✅ All Delta tables created successfully")


def load_to_delta_tables(cfg: Config, duck: DuckDBPyConnection):
    for table_name in DELTA_TABLES:
        try:
            table_uri = f"s3://{MINIO_BUCKET}/{table_name}"
            data_arrow = duck.execute(f"SELECT * FROM {table_name}").arrow()

            write_deltalake(
                table_or_uri=table_uri,
                data=data_arrow,
                mode="append",
                storage_options=cfg,
            )
            logger.info(f"Loaded data into Delta table: {table_name}")
        except Exception as e:
            logger.error(f"❌ Failed to create {table_name}: {e}")

    logger.info("✅ All data loaded into Delta tables successfully")


def load_pipeline(duck: DuckDBPyConnection):
    logger.info("🚀 Starting Load Pipeline")

    # ensure S3 or MinIO bucket
    logger.info("🪣 Setting up MinIO bucket...")
    minio_client = get_minio_client()
    ensure_bucket(MINIO_BUCKET, minio_client)
    logger.info(f"✅ MinIO bucket '{MINIO_BUCKET}' ready")

    # create Delta table, just the table definition without any data
    logger.info("📊 Configuring Delta Lake storage...")
    cfg = Config()
    storage_options = {
        "AWS_ACCESS_KEY_ID": cfg.minio_access_key,
        "AWS_SECRET_ACCESS_KEY": cfg.minio_secret_key,
        "AWS_ENDPOINT_URL": cfg.minio_endpoint_url,
        "AWS_ALLOW_HTTP": "true",
    }

    logger.info("🏗️  Creating Delta table schemas...")
    create_delta_tables(storage_options)

    # load data to delta table
    logger.info("📥 Loading data into Delta tables...")
    load_to_delta_tables(storage_options, duck)

    logger.info("🎉 Load Pipeline completed successfully!")
