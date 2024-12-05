SELECT
    idhall,
    real_cost,
    banquet_time
FROM client_order
WHERE 1=1
    AND order_status='$order_status'
    AND idhall='$hall_id'
    AND DATE(banquet_time) >= '$date_month_ago';