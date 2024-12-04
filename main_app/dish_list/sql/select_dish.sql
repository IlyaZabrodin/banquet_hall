SELECT
    iddish,
    dish_name,
    dish_price,
    dish_weight
FROM menu
WHERE '$dish_id'=iddish;