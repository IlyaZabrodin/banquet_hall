SELECT passport_data, idmanager
FROM manager
WHERE layoff_date>DATE('$current_date') OR layoff_date is NULL;