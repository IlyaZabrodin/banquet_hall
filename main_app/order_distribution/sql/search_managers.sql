SELECT
    idmanager,
    passport_data
FROM manager
WHERE 1=1
    AND (layoff_date>DATE('$order_date') OR layoff_date is NULL)
    AND employment_date<DATE('$order_date')
    AND (idmanager NOT IN (
        SELECT idmanager
        FROM client_order
        WHERE DATE(banquet_time) = DATE('$order_date')
    ) OR (
        SELECT idmanager
        FROM client_order
        WHERE DATE(banquet_time) = DATE('$order_date')
    ) is NULL);