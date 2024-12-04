UPDATE client_order
SET real_cost = prepaid_expense + '$add_pay', dish_amount = dish_amount +'$add_amount', order_status = '$order_status'
WHERE idorder = '$order_id';