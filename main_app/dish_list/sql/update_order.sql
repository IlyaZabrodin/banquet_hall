UPDATE client_order
SET prepaid_expense = '$prepaid_expense', dish_amount = '$dish_amount', order_status = '$order_status'
WHERE idorder = '$order_id';