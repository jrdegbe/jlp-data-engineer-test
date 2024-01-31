- A Challenge for Prospective Data Engineers: Documentation My Approach and Decisions

Preparation Steps:
Environment Setup:
Ensured Docker and Docker Compose were installed on my macOS.
Installed Python 3.10 using a virtual environment as I encountered environmental issues with pyenv.

- Development Steps:

1. Acquiring the Dataset:
The script retrieve_source_data.py is utilized to fetch the dataset from the specified URL using the requests library.
The dataset is saved locally as data-yellow-202103.parquet.


2. Data Ingestion and Transformation:
The ingest_transform.py script loads the dataset using the pandas library.
Data transformation includes:
Correcting the Location IDs 161 and 237.
Calculating trip duration in seconds.
Selecting necessary columns for ingestion.


3. Database Setup and Data Ingestion:
Used Docker to set up a PostgreSQL database.
The transformed data is ingested into the database using SQLAlchemy in the ingest_transform.py script.
Indexes are created on the PULocationID and DOLocationID columns to optimise query performance.


4. Querying the Data:
The query_data.py script contains the logic to query the top 5 pickup locations with slower than average speeds for each week of March 2021.
top_5.sql and visualisation.py scripts are also prepared to facilitate data querying and visualisation.


5. Data Visualisation:
The visualisation.py script utilizes matplotlib and seaborn libraries to create a line plot showcasing the weekly average speed per pickup location.


6. Testing:
Created test_functions.py to ensure the correctness of data transformation, database connection, and visualization functions.


7. Docker Compose:
Updated docker-compose.yml to orchestrate the containers for database, data ingestion, data querying, and visualisation.

Version Control:
Make frequent commits to your local Git repository to track your progress.

- Running the Code:
Build and Start the Docker Containers:

docker-compose up --build -d

- Execute the Data Ingestion and Transformation Script:
docker-compose run data-ingestion

- Execute the Query Script:
docker-compose run query-data

- Execute the test scripts:
- docker-compose up --build test

- (Optional) Execute the Visualization Script:

docker-compose run visualisation

Accessing and Running the .SQL Script on PostgreSQL:
- Access PostgreSQL Container:
docker exec -it jlp-data-engineer-test-query-data psql -U postgres -d my_database


- Create the Database (if not already created):
CREATE DATABASE my_database;


- Run the .SQL Script:
docker cp /path/to/your/script.sql jlp-data-engineer-test-query-data:/script.sql

\i /script.sql

- psql -U postgres -d my_database


- Viewing the Results:
SELECT * FROM taxi_trips;


- Exiting the PostgreSQL Interactive Terminal:
\q


- Stopping the Containers:
docker-compose down

Additional Notes:
Ensure to navigate to the correct directory if the script paths are relative.
If there are any issues or if further configurations are required, they would be documented in the provided README file.

8. Requirements:
Specified the necessary Python libraries in requirements.txt.


Answers to Task Questions

1. Meeting the Needs of the Data Analyst:
Provided scripts and SQL queries to answer the business question regarding the top 5 pickup locations with slower than average speeds for each week of March 2021.


2. Ensuring Data Quality:
Data transformation steps were taken to correct known data quality issues (e.g., swapping Location IDs 161 and 237).
Ensured only valid rows are considered in the average speed calculations.


3. Scaling the Solution:
For a larger dataset (e.g., 10TiB), considerations would include:
Optimising the database schema and indexing.

Additional Sections
Code Structure:
Directory Structure:
src: Contains all scripts necessary for data ingestion, transformation, querying, and visualisation and Where the downloaded dataset is stored.
Root level: SQL scripts are stored.

Modular Code:
Functions and scripts are separated based on their responsibilities, making the codebase easy to navigate and maintain.


Error Handling:
Implemented error handling during data ingestion and index creation to ensure data quality and integrity.


Version Control:
Utilised Git for version control to track changes and ensure a reliable development workflow.
Ensured to commit changes locally as per the task instructions, maintaining a well-kept history of the development process.


Future Improvements:
Performance Optimisation:
Explore optimisation techniques for handling larger datasets, such as database sharding or utilising a Big Data framework like Apache Spark.


Automated Data Pipeline:
Consider setting up an automated data pipeline for continuous data ingestion and transformation, especially as new data arrives daily.


Deployment:
Look into deployment options for making the solution available in a production environment, e.g., deploying on a cloud platform like AWS or GCP.


Monitoring and Alerting:
Implement monitoring and alerting to track the system’s health and receive notifications for any unexpected behaviour.


- For the Analysis I did investigate others.
Here are the following: 

1. The question is to find the top 5 pick-up locations that result in trips which are slower than the average trip speed for each week of March 2021. 

Here is the query formatted for direct execution in psql:

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
        taxi_trips
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
        taxi_trips
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


Here's a breakdown of the results:

In the week starting 1st March 2021:
1. Pickup Location (PULocationID): 207 had an average speed of approximately 8.45 mph.
2. Pickup Location (PULocationID): 193 had an average speed of approximately 9.35 mph.
3. Pickup Location (PULocationID): 58 had an average speed of approximately 10.02 mph.
4. Pickup Location (PULocationID): 236 had an average speed of approximately 10.74 mph.
5. Pickup Location (PULocationID): 161 had an average speed of approximately 10.90 mph.

Observations:
- It seems that all top 5 pickup locations with speeds slower than the monthly average fall within the same week of 1st March 2021.


The results seem to provide a clear answer to the question: identifying the top 5 pickup locations that result in trips slower than the average speed for the entire month of March 2021.

- A few observations and suggestions:

1. Data Consistency: The initial data transformation corrected the PULocationID values by swapping 161 and 237. 
This change seems to be reflected in the final results, as PULocationID 161 appears in the list. 
It's essential to remember why this transformation was performed and ensure it was appropriate.

2. Interpretation: All top 5 slowest trips occurred in the week starting 1st March 2021. 
It might be worth investigating whether there were any external factors affecting the speed during this week (e.g., events, roadworks, weather conditions).

3. Further Analysis: While the query provides the top 5 slowest pickup locations for a single week, 
you might want to expand the analysis to see the top 5 slowest pickup locations for each week of March 2021. This could provide more comprehensive insights into the entire month.

4. Performance: The query you've written seems to be efficient. However, as the data grows, it's always good to monitor the performance. 
The creation of indexes, as seen in the ingestion code, is a good step in ensuring that the query runs efficiently.

5. Data Quality: The results show average speeds that are quite low (e.g., 8.45 mph). 
It might be worth checking if these low speeds are due to traffic congestion at those pickup locations, shorter trips, or perhaps data quality issues.

- In conclusion, the query seems well-constructed to answer the given question. 
The results provide a starting point for deeper analysis and potentially actionable insights for taxi operators or city planners.


- FOR DATA QUALITY:

When addressing potential data quality issues related to average speeds, a few analyses can be performed:

1. Short Trips: If many of the trips from these pickup locations are short, the average speed might be lower due to the frequent starting and stopping associated with short trips.

2. Time of Day: Trips during rush hours might have lower average speeds compared to those during off-peak hours. Analyzing the distribution of pickup times might give insights into this.

3. Duration Outliers: Extremely long or short trip durations relative to the distance traveled might skew the average speed. Check for outliers in the trip duration and distance data.

4. Traffic Congestion: If certain pickup locations are in heavily congested areas (e.g., busy commercial districts, tourist spots), then low speeds are expected.

5. Data Errors: There could be erroneous data entries, such as trips with zero distances but non-zero durations or vice versa.


- Here's a SQL query to check the distribution of trip distances and durations for the top pickup location (PULocationID = 207):

SELECT
    "PULocationID",
    AVG("trip_distance") AS average_distance,
    AVG("trip_duration") AS average_duration,
    MIN("trip_distance") AS min_distance,
    MAX("trip_distance") AS max_distance,
    MIN("trip_duration") AS min_duration,
    MAX("trip_duration") AS max_duration
FROM
    taxi_trips
WHERE
    "tpep_pickup_datetime" >= '2021-03-01' AND
    "tpep_pickup_datetime" < '2021-04-01' AND
    "PULocationID" = 207
GROUP BY
    "PULocationID";


The results: 
--------------+--------------------+------------------+--------------+--------------+--------------+--------------
          207 | 2.8396694214876037 | 1359.01652892562 |            0 |        13.45 |            6 |        33054

The results for PULocationID = 207 provide some interesting insights:

Average Distance & Duration: The average trip distance from this location is approximately 2.84 miles with an average duration of approximately 1,359 seconds (or 22.65 minutes). 
This gives an average speed of about 7.55 mph, which is close to the previously observed value of 8.45 mph.

Min & Max Distance: The minimum distance of 0 miles suggests there are trips that started and ended at the same location. 
This might be due to trips that were cancelled shortly after starting or other data anomalies. 
The maximum distance of 13.45 miles gives us a sense of the range of trip distances from this location.

Min & Max Duration: The minimum duration is 6 seconds, which is very short and might indicate trips that were started and ended almost immediately. 
The maximum duration of 33,054 seconds (or 550.9 minutes) is quite long, especially when compared to the average duration. 
This might be an outlier or a long trip that was left running.

Observations: 

The data suggests a few potential data quality issues:

1. Short Trips: Trips with extremely short distances and durations might be influencing the average speed.
Possible Outliers: The maximum duration seems quite long, especially if the associated distance isn't proportionally high.


Next steps:

1. Investigate trips with very short distances and durations to determine if they are genuine trips or data anomalies.
2. Examine trips with unusually long durations to see if they're outliers or genuine long trips.
3. Analyze the distribution of pickup times to see if rush hours might be influencing average speeds.

1. Investigate trips with very short distances and durations
We'll start by looking at trips from PULocationID = 207 during March 2021 that have both a distance of less than 0.1 miles and a duration of less than 60 seconds.
This will help us understand the nature and frequency of these very short trips.

SELECT
    COUNT(*) AS num_short_trips,
    AVG("trip_distance") AS avg_distance_short_trips,
    AVG("trip_duration") AS avg_duration_short_trips
FROM
    taxi_trips
WHERE
    "tpep_pickup_datetime" >= '2021-03-01' AND
    "tpep_pickup_datetime" < '2021-04-01' AND
    "PULocationID" = 207 AND
    "trip_distance" < 0.1 AND
    "trip_duration" < 60;

 num_short_trips | avg_distance_short_trips | avg_duration_short_trips 
-----------------+--------------------------+--------------------------
              20 |                        0 |                    42.35
(1 row)


- The results from the query focused on short trips indicate:

There were 20 trips from PULocationID = 207 in March 2021 with a distance of less than 0.1 miles and a duration of less than 60 seconds.
The average distance for these trips is 0, which implies that the distance covered in these trips was negligible or perhaps not even recorded accurately.
The average duration for these trips was 42.35 seconds, indicating that these trips were indeed very short.

These short trips might be due to various reasons:

1. Data Entry Errors: It's possible that some of these trips are data entry errors or anomalies in the recording system. 
A trip with a negligible distance but a recorded duration might be a system glitch or an error during data entry.

2. Cancelled Trips: They could represent trips where passengers changed their minds shortly after entering the vehicle or realized they boarded the wrong taxi.
3. Meter Activation Errors: Sometimes, taxi drivers might activate the meter before the passenger boards or in anticipation of a passenger who ultimately doesn't take the trip.

2. Examine trips with unusually long durations
Next, we'll investigate the trips that have durations longer than, say, 3 hours (10,800 seconds). 
This will give us a sense of whether these are outliers or genuine long trips.

SELECT
    COUNT(*) AS num_long_trips,
    AVG("trip_distance") AS avg_distance_long_trips,
    AVG("trip_duration") AS avg_duration_long_trips
FROM
    taxi_trips
WHERE
    "tpep_pickup_datetime" >= '2021-03-01' AND
    "tpep_pickup_datetime" < '2021-04-01' AND
    "PULocationID" = 207 AND
    "trip_duration" > 10800;

 num_long_trips | avg_distance_long_trips | avg_duration_long_trips 
----------------+-------------------------+-------------------------
              1 |                       0 |                   33054
(1 row)

The results from the query focused on long trips indicate:

There was 1 trip from PULocationID = 207 in March 2021 with a duration greater than 10,800 seconds (or 3 hours).
Surprisingly, the average distance for this trip is 0, which means that the vehicle traveled virtually no distance but the duration was recorded as 33,054 seconds (or roughly 9.18 hours).


This data point seems highly anomalous for a few reasons:

1. Stagnant Trip: A 9-hour trip with virtually no distance covered is implausible in a normal taxi service scenario. 
It could have been a case where the meter was left running accidentally without any trip taking place.
2. Data Entry Errors: This could be an error in data recording or entry. It's unusual for a taxi to be stationary for such a long duration with the meter running.
3. Special Scenarios: While unlikely, there might be special cases where a taxi is hired for long durations without much movement, 
like using the taxi for some other purpose or waiting for an extended period. However, a 9-hour wait is still highly unusual.

3. Analyze the distribution of pickup times
Lastly, we'll examine the distribution of pickup times to determine if there are specific hours during the day when trips are more frequent, 
which could indicate rush hours or other patterns.

SELECT
    EXTRACT(HOUR FROM "tpep_pickup_datetime") AS pickup_hour,
    COUNT(*) AS num_trips
FROM
    taxi_trips
WHERE
    "tpep_pickup_datetime" >= '2021-03-01' AND
    "tpep_pickup_datetime" < '2021-04-01' AND
    "PULocationID" = 207
GROUP BY
    pickup_hour
ORDER BY
    pickup_hour;
 pickup_hour | num_trips 
-------------+-----------
           5 |         1
           7 |         3
           8 |         2
           9 |         4
          10 |        20
          11 |        13
          12 |        20
          13 |        17
          14 |        18
          15 |         7
          16 |         1
          17 |         7
          18 |         2
          22 |         5
          23 |         1
(15 rows)


- The results from the query provide insights into the distribution of taxi pickups at location PULocationID = 207 over different hours of the day in March 2021:

1. Morning Rush: The morning starts slow with only 1 trip at 5 AM. The pickups then increase slightly around 7-9 AM, indicating the start of the morning rush.

2. Mid-day Peak: The most significant activity is during mid-day from 10 AM to 2 PM, with 20 trips at 10 AM and 12 PM, and 17-18 trips around 1-2 PM. 
This indicates that this location might be popular for lunchtime activities or mid-day commutes.

3. Afternoon Decline: The activity declines in the afternoon, with the lowest at 16 trips at 4 PM.

4. Evening: There's a slight increase in the early evening around 5-6 PM, perhaps indicating the start of the evening rush or end-of-day activities.

5. Night: The pickups decrease drastically post 6 PM, with minimal activity during the night.

- This hourly distribution can provide insights into the nature of the pickup location:

If it's a business district, the mid-day peak might correspond to lunch breaks or meetings.
If it's a recreational area, the mid-day peak might indicate popular visiting hours.

The decline in evening and nighttime indicates it might not be a primary nightlife spot or residential area where late-night pickups would be more frequent.

Understanding these patterns can help taxi drivers decide where and when to position themselves for maximum pickups. 
It can also assist city planners in understanding traffic and commuter patterns.