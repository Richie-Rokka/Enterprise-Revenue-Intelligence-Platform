-- Negative Revenue

SELECT *
FROM raw.order_items
WHERE price < 0;

-- Negative Freight

SELECT *
FROM raw.order_items
WHERE freight_value < 0;