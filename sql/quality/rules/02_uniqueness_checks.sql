-- Customer Duplicate Check

SELECT
customer_id,
COUNT(*)
FROM raw.customers
GROUP BY customer_id
HAVING COUNT(*) > 1;

-- Order Duplicate Check

SELECT
order_id,
COUNT(*)
FROM raw.orders
GROUP BY order_id
HAVING COUNT(*) > 1;