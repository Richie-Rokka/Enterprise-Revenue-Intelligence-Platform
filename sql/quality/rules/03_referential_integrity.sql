-- Orders → Customers

SELECT
COUNT(*) AS orphan_orders
FROM raw.orders o
LEFT JOIN raw.customers c
ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;

-- Payments → Orders

SELECT
COUNT(*) AS orphan_payments
FROM raw.order_payments p
LEFT JOIN raw.orders o
ON p.order_id = o.order_id
WHERE o.order_id IS NULL;