from pathlib import Path
from datetime import datetime, timezone
import uuid
from validation import validate_dataset
import pandas as pd
from state import (calculate_file_hash, already_processed, mark_processed,)
from s3_uploader import upload_file_to_s3


SOURCE_DIR = Path("data/generated")
RAW_DIR = Path("data/raw")

DATASETS = [
    "customers",
    "products",
    "orders",
    "order_items",
    "payments",
]


def read_dataset(dataset_name):
    file_path = SOURCE_DIR / f"{dataset_name}.csv"

    if not file_path.exists():
        raise FileNotFoundError(
            f"Source file not found: {file_path}"
        )

    dataframe = pd.read_csv(file_path)

    if dataframe.empty:
        raise ValueError(
            f"{dataset_name} contains no data."
        )

    print(
        f"Read {len(dataframe):,} rows from {file_path}"
    )

    return dataframe


def add_ingestion_metadata(dataframe, batch_id):
    dataframe = dataframe.copy()

    dataframe["_batch_id"] = batch_id
    dataframe["_ingested_at"] = datetime.now(timezone.utc)

    return dataframe


def save_to_raw_zone(dataframe, dataset_name, batch_id):
    ingestion_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    output_directory = (
        RAW_DIR
        / dataset_name
        / f"ingestion_date={ingestion_date}"
    )

    output_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    output_path = (
        output_directory
        / f"{dataset_name}_{batch_id}.csv"
    )

    dataframe.to_csv(
        output_path,
        index=False
    )

    print(f"Saved raw batch -> {output_path}")

    return output_path, ingestion_date


def ingest_dataset(dataset_name, batch_id):
    print(f"\nIngesting: {dataset_name}")

    file_path = SOURCE_DIR / f"{dataset_name}.csv"

    file_hash = calculate_file_hash(
        file_path
    )

    if already_processed(
        dataset_name,
        file_hash
    ):
        print(
            f"Skipping {dataset_name}: "
            "source file already processed."
        )

        return

    dataframe = read_dataset(
        dataset_name
    )

    validate_dataset(
        dataframe,
        dataset_name
    )

    dataframe = add_ingestion_metadata(
        dataframe,
        batch_id
    )
    
    output_path, ingestion_date = save_to_raw_zone(
        dataframe,
        dataset_name,
        batch_id
    )

    upload_file_to_s3(
        local_path=output_path,
        dataset_name=dataset_name,
        ingestion_date=ingestion_date,
        filename=output_path.name
    )

    mark_processed(
        dataset_name,
        file_hash
    )

def main():
    batch_id = str(uuid.uuid4())

    print("=" * 60)
    print("Starting ecommerce ingestion")
    print(f"Batch ID: {batch_id}")
    print("=" * 60)

    for dataset_name in DATASETS:
        try:
            ingest_dataset(
                dataset_name,
                batch_id
            )

        except Exception as error:
            print(
                f"FAILED: {dataset_name}: {error}"
            )
            raise

    print("\n" + "=" * 60)
    print("Ingestion completed successfully")
    print("=" * 60)


if __name__ == "__main__":
    main()