{{
    config(
        materialized='incremental',
        unique_key='order_id'
    )
}}

select
    o.order_id,
    o.customer_id,
    o.order_date,
    o.order_status,
    p.payment_id,
    p.payment_method,
    p.payment_status,
    p.amount as payment_amount,
    o._ingested_at

from {{ ref('stg_orders') }} o

left join {{ ref('stg_payments') }} p
    on o.order_id = p.order_id

{% if is_incremental() %}

where o._ingested_at > (
    select coalesce(max(_ingested_at), '1900-01-01'::timestamp_tz)
    from {{ this }}
)

{% endif %}