SELECT
customer_id,
COUNT(*)
FROM raw.customers
GROUP BY customer_id
HAVING COUNT(*) > 1;