import pandas as pd
from sqlalchemy import create_engine, text, exc
import sqlalchemy.types
from sqlalchemy.orm import sessionmaker
from pathlib import Path

def load_dataset(filepath):
    data = pd.read_parquet(filepath)
    return data

def correct_location_ids(data):
    corrected_data = data.copy()
    corrected_data.loc[corrected_data['PULocationID'] == 161, 'PULocationID'] = 237
    corrected_data.loc[corrected_data['PULocationID'] == 237, 'PULocationID'] = 161
    return corrected_data

def calculate_trip_duration(data):
    data_with_duration = data.copy()
    data_with_duration['trip_duration'] = (data['tpep_dropoff_datetime'] - data['tpep_pickup_datetime']).dt.total_seconds()
    return data_with_duration

def select_necessary_columns(data):
    selected_columns_data = data[['PULocationID', 'DOLocationID', 'trip_distance', 'trip_duration', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']]
    return selected_columns_data

def transform_data(data):
    corrected_data = correct_location_ids(data)
    data_with_duration = calculate_trip_duration(corrected_data)
    transformed_data = select_necessary_columns(data_with_duration)
    return transformed_data

def get_db_engine(connection_string):
    engine = create_engine(connection_string, echo=True)
    return engine

def ingest_data(data, engine):
    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        data.to_sql(
            'taxi_trips', 
            engine, 
            if_exists='replace', 
            index=False, 
            method='multi', 
            chunksize=1000,
            dtype={
                'PULocationID': sqlalchemy.types.Integer(),
                'DOLocationID': sqlalchemy.types.Integer(),
                'trip_distance': sqlalchemy.types.Float(),
                'trip_duration': sqlalchemy.types.Float(),
                'tpep_pickup_datetime': sqlalchemy.types.DateTime(),
                'tpep_dropoff_datetime': sqlalchemy.types.DateTime()
            }
        )
        # Commit the transaction
        session.commit()  # Adding the commit statement here
        print("Data ingested successfully.")
    except exc.SQLAlchemyError as e:
        session.rollback()  # Rollback in case of an error
        print(f"An error occurred during data ingestion: {e}")
    finally:
        session.close()  # Ensure the session is closed

def create_indexes(engine):
    with engine.connect() as connection:
        trans = connection.begin()
        try:
            connection.execute(text('CREATE INDEX IF NOT EXISTS idx_pu_location ON taxi_trips ("PULocationID");'))
            connection.execute(text('CREATE INDEX IF NOT EXISTS idx_do_location ON taxi_trips ("DOLocationID");'))
            trans.commit()
            print("Indexes created successfully.")
        except exc.SQLAlchemyError as e:
            print(f"An error occurred during index creation: {e}")
            trans.rollback()

def main():
    filepath = Path(__file__).parent / "data-yellow-202103.parquet"
    dataset = load_dataset(str(filepath))
    transformed_data = transform_data(dataset)
    
    # Define the connection_string outside the function
    connection_string = "postgresql://postgres:derek@db:5432/my_database"
    engine = get_db_engine(connection_string)
    
    ingest_data(transformed_data, engine)
    create_indexes(engine)

if __name__ == "__main__":
    main()
    
    
