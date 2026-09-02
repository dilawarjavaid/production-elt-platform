select
    order_item_id,
    order_id,
    product_id,
    quantity,
    unit_price,
    line_total,
    _batch_id,
    _ingested_at
from {{ source('raw', 'order_items') }}
