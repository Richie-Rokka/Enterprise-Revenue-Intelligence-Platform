-- Orders Table

SELECT
COUNT(*) AS total_rows,

COUNT(*) - COUNT(order_id)
AS missing_order_id,

COUNT(*) - COUNT(customer_id)
AS missing_customer_id,

COUNT(*) - COUNT(order_status)
AS missing_order_status

FROM raw.orders;

-- Products Table

SELECT
COUNT(*) - COUNT(product_category_name)
AS missing_category,

COUNT(*) - COUNT(product_name_lenght)
AS missing_name_length,

COUNT(*) - COUNT(product_description_lenght)
AS missing_description_length

FROM raw.products;