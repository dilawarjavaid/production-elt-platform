select
    product_id,
    product_name,
    category,
    price,
    is_active,
    _batch_id,
    _ingested_at
from {{ source('raw', 'products') }}