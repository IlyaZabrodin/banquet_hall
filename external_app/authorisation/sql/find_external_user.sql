SELECT
    user_id,
    NULL AS user_group
FROM external_user
WHERE 1=1
    AND login ='$login'
    AND password = '$password'