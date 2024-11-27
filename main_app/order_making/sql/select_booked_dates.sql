SELECT
    DATE(banquet_time)
FROM client_order
WHERE 1=1
    AND DATE(banquet_time) >= '$tomorrow_date'
    AND DATE(banquet_time) <= '$next_month_date';