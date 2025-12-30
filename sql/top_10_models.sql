SELECT
    make,
    model,
    COUNT(DISTINCT VIN) AS registered
FROM
    dataframe
GROUP BY
    make,
    model
ORDER BY
    registered DESC
LIMIT 10