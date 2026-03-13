with source as (
    select * from {{ source('oltp', 'orders') }}
),

renamed as (
    select
        order_id,
        customer_id,
        order_status,
        -- Casting string timestamps into proper database timestamps
        cast(order_purchase_timestamp as timestamp) as order_purchase_at,
        cast(order_delivered_customer_date as timestamp) as order_delivered_at
    from source
)

select * from renamed