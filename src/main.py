import logging
import os

import pandas as pd
from deltalake import DeltaTable
from deltalake.writer import write_deltalake

from utils.logging import setup_logging

# from utils.minio import get_minio_client


def main():
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting Delta Lakehouse example")
    df = pd.DataFrame(range(5), columns=["id"])
    os.makedirs("./data/deltars_table", exist_ok=True)
    # Create Pandas DataFrame
    write_deltalake("./data/deltars_table", df, mode="overwrite")
    # Write Delta Lake table
    df = pd.DataFrame(range(6, 11), columns=["id"])  # Generate new data
    write_deltalake("./data/deltars_table", df, mode="append")
    # Append new data
    dt = DeltaTable("./data/deltars_table")
    # Read Delta Lake table
    print(dt.to_pandas())


if __name__ == "__main__":
    main()
