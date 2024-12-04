SELECT
    m.dish_name,
    dl.dish_amount,
    m.dish_price,
    (dl.dish_amount * m.dish_price) AS total_price
FROM
    dish_list dl
JOIN
    menu m ON dl.iddish = m.iddish
JOIN
    client_order co ON dl.idorder = co.idorder
WHERE
    co.idorder = '$order_id';
