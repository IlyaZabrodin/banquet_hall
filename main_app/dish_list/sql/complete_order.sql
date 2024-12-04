UPDATE client_order
SET real_cost = prepaid_expense, order_status = '$order_status'
WHERE idorder = '$order_id';