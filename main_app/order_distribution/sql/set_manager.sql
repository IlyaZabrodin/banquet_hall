UPDATE client_order
SET idmanager = '$manager_id',
    order_status = '$order_status'
WHERE idorder = '$order_id';