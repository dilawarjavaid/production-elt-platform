select
    order_id,
    customer_id,
    order_date,
    order_status,
    _batch_id,
    _ingested_at
from {{ source('raw', 'orders') }}
