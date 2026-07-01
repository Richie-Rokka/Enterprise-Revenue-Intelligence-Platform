SELECT
COUNT(*) AS total_rows,

COUNT(*) - COUNT(customer_id)
AS missing_customer_id,

COUNT(*) - COUNT(customer_unique_id)
AS missing_customer_unique_id,

COUNT(*) - COUNT(customer_city)
AS missing_customer_city,

COUNT(*) - COUNT(customer_state)
AS missing_customer_state

FROM raw.customers;