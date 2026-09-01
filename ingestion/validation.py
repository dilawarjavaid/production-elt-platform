EXPECTED_COLUMNS = {
    "customers": {
        "customer_id",
        "first_name",
        "last_name",
        "email",
        "city",
        "signup_date",
    },

    "products": {
        "product_id",
        "product_name",
        "category",
        "price",
        "is_active",
    },

    "orders": {
        "order_id",
        "customer_id",
        "order_date",
        "order_status",
    },

    "order_items": {
        "order_item_id",
        "order_id",
        "product_id",
        "quantity",
        "unit_price",
        "line_total",
    },

    "payments": {
        "payment_id",
        "order_id",
        "payment_method",
        "payment_status",
        "amount",
        "payment_date",
    },
}


def validate_schema(dataframe, dataset_name):
    expected_columns = EXPECTED_COLUMNS[dataset_name]
    actual_columns = set(dataframe.columns)

    missing_columns = expected_columns - actual_columns
    unexpected_columns = actual_columns - expected_columns

    if missing_columns:
        raise ValueError(
            f"{dataset_name} missing columns: "
            f"{sorted(missing_columns)}"
        )

    if unexpected_columns:
        raise ValueError(
            f"{dataset_name} has unexpected columns: "
            f"{sorted(unexpected_columns)}"
        )


def validate_null_keys(dataframe, dataset_name):
    primary_keys = {
        "customers": "customer_id",
        "products": "product_id",
        "orders": "order_id",
        "order_items": "order_item_id",
        "payments": "payment_id",
    }

    primary_key = primary_keys[dataset_name]

    if dataframe[primary_key].isnull().any():
        raise ValueError(
            f"{dataset_name} contains null values "
            f"in primary key {primary_key}"
        )


def validate_duplicates(dataframe, dataset_name):
    primary_keys = {
        "customers": "customer_id",
        "products": "product_id",
        "orders": "order_id",
        "order_items": "order_item_id",
        "payments": "payment_id",
    }

    primary_key = primary_keys[dataset_name]

    if dataframe[primary_key].duplicated().any():
        raise ValueError(
            f"{dataset_name} contains duplicate "
            f"{primary_key} values"
        )


def validate_dataset(dataframe, dataset_name):
    validate_schema(dataframe, dataset_name)
    validate_null_keys(dataframe, dataset_name)
    validate_duplicates(dataframe, dataset_name)

    print(f"Validation passed: {dataset_name}")