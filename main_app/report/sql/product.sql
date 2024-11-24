SELECT
    rep_id, prod_id, prod_col, rep_month, rep_year, income
FROM
    product_report
WHERE
    rep_month = '$rep_month' AND rep_year = '$rep_year';
