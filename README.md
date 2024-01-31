# A Challenge for Prospective Data Engineers
Thank you for taking the time to participate in this challenge! 

This is the technical exercise we use at John Lewis Partnership to evaluate potential new candidate Data Engineers. It will allow 
you to demonstrate that you know how to: 

* Acquire and explore a dataset
* Ingest data
* Transform data
* Query data

Please read all the instructions below carefully and don’t hesitate to contact us if you have any queries.

As a Data Engineer, you shouldn't find this exercise to be particularly difficult. We're expecting a simple solution
that addresses only what is asked.

## Instructions

### Context
In this challenge, pretend that you are an Engineer working in a Data Engineering Team. You have been given the following user story to implement:

> As a data analyst
> 
> I want to query the [New York City Taxi cab Data Set](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
> 
> So that I can conveniently answer important business questions such as 
>
>    _"In each week for the month of March 2021, what are the top 5 Pick up locations (`PULocationID`) 
>    that result in trips which are slower than the average speed for a trip in the month 
>    (regardless of drop off and pick up locations)?"_

At John Lewis Partnership, we mainly use Snowflake as our Data Warehouse, using functionality provided by the Google Cloud Platform for 
orchestration and ingestion, but for this exercise we'll use a containerised version of PostgreSQL to allow you to perform the challenge on your local machine.

In this repository, we provide some things to get you started:

* A working `docker-compose` file that has working sample Python code that connects to the postgres db and runs a piece of test SQL.
* A Python script to retrieve source data. We've used Python 3.10
* A `Pipenv` environment describing some dependencies 

### Things you'll need to have installed

* Python 3.10 (possibly via [pyenv](https://github.com/pyenv/pyenv))
* [Pipenv](https://pipenv.pypa.io/en/latest/)
* A container runtime such as [Docker Desktop](https://www.docker.com/products/docker-desktop/)
* You may not need to install [docker-compose](https://github.com/docker/compose/releases) if you use Docker Desktop

### What we want you to do
Change the docker-compose file and provide (new and modified existing) Python scripts so that,
on running the container (via a `docker-compose run <yourservicenamehere>` command):

* PostgreSQL should start up in the container
* **ACQUIRE** You should automatically download the NYC Yellow taxi data set for March 2021
  (from [https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-03.parquet](https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-03.parquet) ). *Note that we only want the "Yellow" set, and for March 2021.*
* **INGEST AND TRANSFORM** Ingest the data set into a database in the PostgreSQL instance running in the container, with the following considerations:
  * You should only ingest the columns needed to answer the question below (i.e. for the SQL query you will need to write)
  * You need to correct a known data quality issue where Location ID 161 and Location 237 have been accidentally swapped in the source system. *You need to renumber them correctly during the ingestion*.
* **QUERY** When the container is up and running and all the steps above have been executed, it should be possible to run a  
  SQL query from the command line against the ingested data set. Write a SQL query to answer the question above. i.e.

     > In each week for the month of March 2021, what are the top 5 Pick up locations (PULocationID) 
     that result in trips which are slower than the average trip speed in the whole month 
     (regardless of drop off and pick up locations)?
  
     Print the result of the query to `stdout`.

     Note that, in answering this question, you will need to calculate the average speed of a trip from the existing columns. *You should
     discard any invalid rows which would make the calculation invalid.*

## What we're looking for
Things we value in your solution are:
* _Self-explanatory code_ – the solution must speak for itself. Multiple paragraphs explaining the solution are a sign that it isn’t straightforward enough to understand purely by reading the code. Also, you should ensure your code is correctly formatted and lints cleanly.
* _Tests_ – the solution must be well tested (possibly using a test-first approach).
* _Simplicity_ – We value simplicity as an architectural virtue and a development practice. Solutions should reflect the difficulty of the assigned task, and should NOT be overly complex. Layers of abstraction, patterns, or architectural features that aren’t called for should NOT be included.
* _Version Control_ - we are interested in how you have approached this work so please commit changes to your local repository and *do not* squash your commits 

Your solution needs to include:

1. Instructions about your strategy and important decisions you made. Provide these as a markdown file.
2. The document in (1) should also answer the following questions:
* How did you meet the needs of the data analyst described in the user story?
* How did you ensure data quality?
* What would need to change for the solution scale to work with a 10TiB dataset with new data arriving each day?
3. Your submission should be a zip file containing your solution and the requested documentation.
4. Your submission needs to contain everything we need to run the code (scripts etc.)
5. Your submission is your own work, you will not share your submission with others (including sharing your repository on a public  
   site such as Github), and you will not otherwise engage in activities that dishonestly improve your result.

## What happens after this?
We hope you'll succeed in this phase! If you do, you proceed to the next phase, in which we'll arrange an interview
where we are expecting you to run us through your solution, demonstrating it from your device. You'll show it running, and walk us 
through your solution while we discuss any choices that you made and provide feedback.

Apart from the exercise, we'll have a conversation about your experience, and you'll 
let us know in detail your past challenges and your future expectations.

*Good Luck!*

## Setup

Basic setup with bootstrapping PostgreSQL with a sample table and querying it.

```
❯ docker-compose run --rm hellodb
Creating jlp-data-engineer-test_db_1 ... done
Creating jlp-data-engineer-test_hellodb_run ... done
WARNING:retry.api:connection failed: Connection refused
	Is the server running on that host and accepting TCP/IP connections?, retrying in 1 seconds...
Sample table has 0 rows

```

## Tips

- You can create new tables by adding a `.sql` file inside `.initdb.d` folder and rebuilding the database
- You can rebuild the database by stoping and removing the container `docker-compose stop -t0 db; docker-compose rm -f db`

