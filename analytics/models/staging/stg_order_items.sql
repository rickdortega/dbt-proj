with source as (
    select * from {{ source('oltp', 'order_items') }}
),

renamed as (
    select
        order_id,
        order_item_id as order_item_sequence,
        product_id,
        price as item_price,
        freight_value as item_freight
    from source
)

select * from renamed