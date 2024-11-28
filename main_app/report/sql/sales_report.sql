SELECT
    idrep, idhall, r_year, r_month, reserves_number, real_cost
FROM
    salereport
WHERE
    r_month = '$rep_month' AND r_year = '$rep_year';