{% snapshot customers_snapshot %}

{{
    config(
      target_schema='SNAPSHOTS',
      unique_key='customer_id',
      strategy='check',
      check_cols=['first_name', 'last_name', 'email', 'city']
    )
}}

select
    customer_id,
    first_name,
    last_name,
    email,
    city,
    signup_date
from {{ source('raw', 'customers') }}

{% endsnapshot %}