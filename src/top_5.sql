WITH MonthlyAverage AS (
    SELECT
        AVG(
            CASE WHEN "trip_duration" <= 0 THEN
                0
            ELSE
                ABS("trip_distance") / (ABS("trip_duration") / 3600)
            END
        ) as avg_speed
    FROM
        public.taxi_trips
    WHERE
        "tpep_pickup_datetime" >= '2021-03-01' AND
        "tpep_pickup_datetime" < '2021-04-01'
        AND "trip_distance" >= 0
        AND "trip_duration" > 0
),
WeeklyAverages AS (
    SELECT
        date_trunc('week', "tpep_pickup_datetime") as week,
        "PULocationID",
        AVG(
            CASE WHEN "trip_duration" <= 0 THEN
                0
            ELSE
                ABS("trip_distance") / (ABS("trip_duration") / 3600)
            END
        ) as avg_speed
    FROM
        public.taxi_trips
    WHERE
        "tpep_pickup_datetime" >= '2021-03-01' AND
        "tpep_pickup_datetime" < '2021-04-01'
        AND "trip_distance" >= 0
        AND "trip_duration" > 0
    GROUP BY
        date_trunc('week', "tpep_pickup_datetime"), "PULocationID"
)
SELECT
    wa.week,
    wa."PULocationID",
    wa.avg_speed
FROM
    WeeklyAverages wa, MonthlyAverage ma
WHERE
    wa.avg_speed < ma.avg_speed
ORDER BY
    wa.week, wa.avg_speed ASC
LIMIT 5;
