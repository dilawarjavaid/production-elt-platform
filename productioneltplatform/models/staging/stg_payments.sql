select
    payment_id,
    order_id,
    payment_method,
    payment_status,
    amount,
    payment_date,
    _batch_id,
    _ingested_at
from {{ source('raw', 'payments') }}