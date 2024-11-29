SELECT
    idorder,
    banquet_time,
    expected_place_amount,
    idhall,
    client_phone,
    user_id
FROM client_order
WHERE 1=1
    AND order_status='$order_status'