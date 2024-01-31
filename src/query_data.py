import pandas as pd
from sqlalchemy import create_engine, text  # Import text
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)

def load_query(filepath):
    with open(filepath, 'r') as file:
        return file.read()

def get_db_engine():
    connection_string = "postgresql://postgres:derek@db:5432/my_database"
    engine = create_engine(connection_string, echo=True)
    return engine

def execute_debug_queries_updated(engine):
    db_name = ""
    schema_name = ""
    try:
        with engine.connect() as connection:
            print(f"Connection details: {connection}")

            # Use text to create a text clause from your SQL string
            result = connection.execute(text('SELECT current_database();'))
            for row in result:
                db_name = row[0]
                print(f"Current database: {db_name}")

            # Same here
            result = connection.execute(text('SELECT current_schema();'))
            for row in result:
                schema_name = row[0]
                print(f"Current schema: {schema_name}")

    except Exception as e:
        logging.error(f"An error occurred in execute_debug_queries: {str(e)}")

    return db_name, schema_name
        
def query_top_pickup_locations_updated(engine):
    df = None
    try:
        execute_debug_queries_updated(engine)
        
        query_filepath = Path(__file__).parent / 'top_5.sql'  # Adjust the path if necessary
        query = load_query(query_filepath)

        df = pd.read_sql_query(query, engine)
        print(df)  # Add this line to print the DataFrame to the console

    except Exception as e:
        logging.error(f"An error occurred in query_top_pickup_locations: {str(e)}")
    
    return df

def main():
    engine = get_db_engine()
    query_top_pickup_locations_updated(engine)

if __name__ == "__main__":
    main()
