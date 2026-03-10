with source as (
    select * from {{ source('oltp', 'orders') }}
),

renamed as (
    select
        order_id,
        customer_id,
        order_date
    from source
)

select * from renamed