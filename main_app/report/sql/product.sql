SELECT
    idrep, idmanag, r_year, r_month, ord_amount, ord_sum
FROM
    orderreport
WHERE
    r_month = '$rep_month' AND r_year = '$rep_year';
