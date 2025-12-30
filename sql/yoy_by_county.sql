WITH SalesByYear AS(
    SELECT
        county,
        model_year,
        COUNT(DISTINCT vin) AS registered
    FROM
        dataframe
    GROUP BY
        county, model_year
)
SELECT
    county,
    model_year,
    registered,
    LAG(registered, 1, 0) OVER (ORDER BY county, model_year) AS registered_ly,
    ((registered - LAG(registered, 1, 0) OVER (ORDER BY county, model_year)) / LAG(registered, 1, registered) OVER (ORDER BY county, model_year)) AS yoy_growth_percent
FROM
    SalesByYear
ORDER BY
    county, model_year