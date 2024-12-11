SELECT
    idorder,
    order_status,
    banquet_time
FROM client_order
WHERE 1=1
    AND user_id='$user_id'