SELECT
    idorder,
    banquet_time,
    expected_place_amount,
    idhall,
    prepaid_expense,
    dish_amount,
    real_cost,
    order_status,
    client_phone,
    user_id
FROM client_order
WHERE 1=1
    AND idmanager='$user_id'
    AND order_status<>'$avoid_status'