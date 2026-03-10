with source as (
    select * from {{ source('oltp', 'products') }}
),

renamed as (
    select
        product_id,
        product_type,
        name as product_name,
        price
    from source
)

select * from renamed