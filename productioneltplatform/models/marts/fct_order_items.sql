select
    oi.order_item_id,
    oi.order_id,
    oi.product_id,
    oi.quantity,
    oi.unit_price,
    oi.line_total,
    o.customer_id,
    o.order_date,
    o.order_status
from {{ ref('stg_order_items') }} oi

left join {{ ref('stg_orders') }} o
    on oi.order_id = o.order_id