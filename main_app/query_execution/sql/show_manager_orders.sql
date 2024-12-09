SELECT idorder, banquet_time, idhall, order_status, client_phone
FROM client_order
WHERE idmanager = '$manager_id'
  AND DATE(banquet_time) >= '$current_date';
