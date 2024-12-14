SELECT idorder
FROM client_order
WHERE order_status = '$ord_stat'
AND prepaid_expense IS NOT NULL;