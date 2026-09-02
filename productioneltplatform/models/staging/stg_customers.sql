select
    customer_id,
    first_name,
    last_name,
    email,
    city,
    signup_date,
    _batch_id,
    _ingested_at
from {{ source('raw', 'customers') }}

select
    product_id,
    product_name,
    category,
    price,
    is_active,
    _batch_id,
    _ingested_at
from {{ source('raw', 'products') }}