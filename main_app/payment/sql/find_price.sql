SELECT
    order_status,
    CASE
        WHEN real_cost IS NULL THEN prepaid_expense
        ELSE (real_cost - prepaid_expense)
    END AS result
FROM client_order
WHERE idorder = '$order_id';