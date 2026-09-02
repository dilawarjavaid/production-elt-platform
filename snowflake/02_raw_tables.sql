USE DATABASE PRODUCTION_ELT;
USE SCHEMA RAW;
USE WAREHOUSE ELT_WH;

CREATE OR REPLACE TABLE CUSTOMERS (
    customer_id INTEGER,
    first_name STRING,
    last_name STRING,
    email STRING,
    city STRING,
    signup_date DATE,
    _batch_id STRING,
    _ingested_at TIMESTAMP_TZ
);

CREATE OR REPLACE TABLE PRODUCTS (
    product_id INTEGER,
    product_name STRING,
    category STRING,
    price NUMBER(10,2),
    is_active BOOLEAN,
    _batch_id STRING,
    _ingested_at TIMESTAMP_TZ
);

CREATE OR REPLACE TABLE ORDERS (
    order_id INTEGER,
    customer_id INTEGER,
    order_date TIMESTAMP_NTZ,
    order_status STRING,
    _batch_id STRING,
    _ingested_at TIMESTAMP_TZ
);

CREATE OR REPLACE TABLE ORDER_ITEMS (
    order_item_id INTEGER,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    unit_price NUMBER(10,2),
    line_total NUMBER(12,2),
    _batch_id STRING,
    _ingested_at TIMESTAMP_TZ
);

CREATE OR REPLACE TABLE PAYMENTS (
    payment_id STRING,
    order_id INTEGER,
    payment_method STRING,
    payment_status STRING,
    amount NUMBER(12,2),
    payment_date TIMESTAMP_NTZ,
    _batch_id STRING,
    _ingested_at TIMESTAMP_TZ
);