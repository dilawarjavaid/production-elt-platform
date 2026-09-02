select
    c.customer_id,
    c.first_name,
    c.last_name,
    c.city,
    count(distinct o.order_id) as total_orders,
    sum(o.payment_amount) as total_revenue,
    avg(o.payment_amount) as avg_order_value
from {{ ref('dim_customers') }} c

left join {{ ref('fct_orders') }} o
    on c.customer_id = o.customer_id

group by
    c.customer_id,
    c.first_name,
    c.last_name,
    c.city