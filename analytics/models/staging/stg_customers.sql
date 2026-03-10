with source as (
    select * from {{ source('oltp', 'customers') }}
),

renamed as (
    select
        customer_id,
        email,
        first_name,
        last_name,
        created_at as customer_created_at
    from source
)

select * from renamed