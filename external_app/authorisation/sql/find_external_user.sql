SELECT
    user_id,
    user_group
FROM external_user
WHERE 1=1
    AND login ='$login'
    AND password = '$password'