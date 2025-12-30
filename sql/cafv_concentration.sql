SELECT
    state,
    city,
    county,
    COUNT(DISTINCT VIN) AS registered
FROM
    dataframe
WHERE
    "cafv_eligibility" = 'Clean Alternative Fuel Vehicle Eligible'
GROUP BY
    state,
    city,
    county
ORDER BY
    registered DESC