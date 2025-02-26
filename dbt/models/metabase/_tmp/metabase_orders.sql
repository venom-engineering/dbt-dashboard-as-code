select
    orders.*,
    locations.location_name,
    customers.customer_type

from
    {{ ref("orders") }}

left join
    {{ ref("locations") }}
on
    orders.location_id = locations.location_id

left join
    {{ ref("customers") }}
on
    orders.customer_id = customers.customer_id
