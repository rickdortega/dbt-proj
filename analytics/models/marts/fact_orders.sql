with orders as (
    select * from {{ ref('stg_orders') }}
),

order_items as (
    select * from {{ ref('stg_order_items') }}
),

products as (
    select * from {{ ref('stg_products') }}
),

-- First, calculate the total price and item count per order
order_summary as (
    select
        oi.order_id,
        sum(oi.quantity) as total_items,
        sum(oi.quantity * p.price) as total_order_amount
    from order_items oi
    join products p on oi.product_id = p.product_id
    group by 1
),

-- Finally, join that summary back to the main orders table
final as (
    select
        o.order_id,
        o.customer_id,
        o.order_date,
        coalesce(os.total_items, 0) as total_items,
        coalesce(os.total_order_amount, 0) as total_order_amount
    from orders o
    left join order_summary os on o.order_id = os.order_id
)

select * from final