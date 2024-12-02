SELECT
    idmanager,
    passport_data
FROM manager AS m
LEFT JOIN client_order AS o ON (o.idmanager=m.idmanager AND DATE(o.banquet_time) = DATE('$order_date'))
WHERE (m.layoff_date>DATE('$order_date') OR m.layoff_date is NULL)
    AND m.employment_date<DATE('$order_date')
    AND o.idmanager IS NULL;
