with orders as (
    select * from {{ ref('stg_orders') }}
),

order_items as (
    select * from {{ ref('stg_order_items') }}
),

-- Aggregate item-level data up to the order level
order_summary as (
    select
        order_id,
        count(order_item_sequence) as total_items,
        sum(item_price) as total_product_revenue,
        sum(item_freight) as total_freight_revenue,
        sum(item_price + item_freight) as total_order_value
    from order_items
    group by 1
),

-- Join the aggregations back to the main order record
final as (
    select
        o.order_id,
        o.customer_id,
        o.order_status,
        o.order_purchase_at,
        coalesce(os.total_items, 0) as total_items,
        coalesce(os.total_product_revenue, 0) as total_product_revenue,
        coalesce(os.total_order_value, 0) as total_order_value
    from orders o
    left join order_summary os on o.order_id = os.order_id
)

select * from final