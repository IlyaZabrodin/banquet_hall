SELECT
    idhall,
    banquet_time,
    expected_place_amount
FROM client_order
WHERE 1=1
    AND idhall='$hall_id'
    AND DATE(banquet_time) >= '$tomorrow_date';