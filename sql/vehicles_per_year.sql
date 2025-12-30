SELECT
    model_year,
    COUNT(DISTINCT VIN) AS registered
FROM
    dataframe
GROUP BY
    model_year
ORDER BY
    model_year ASC