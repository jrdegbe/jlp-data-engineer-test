import pandas as pd
import pytest
from src.ingest_transform import load_dataset, correct_location_ids, calculate_trip_duration, select_necessary_columns, transform_data
from src.query_data import load_query, get_db_engine, execute_debug_queries_updated, query_top_pickup_locations_updated
from src.visualisation import load_query as viz_load_query

# Dummy data for testing
dummy_data_path = "/Users/jrdegbe/Desktop/jlp-data-engineer-test/data/test_data.parquet"
dummy_data = pd.read_parquet(dummy_data_path)

# Tests for ingest_transform.py
def test_load_dataset():
    assert isinstance(load_dataset(dummy_data_path), pd.DataFrame)

def test_correct_location_ids():
    corrected_data = correct_location_ids(dummy_data)
    assert corrected_data['PULocationID'].equals(dummy_data['PULocationID'].replace({161: 237, 237: 161}))

def test_calculate_trip_duration():
    data_with_duration = calculate_trip_duration(dummy_data)
    assert 'trip_duration' in data_with_duration.columns

def test_select_necessary_columns():
    data_with_duration = calculate_trip_duration(dummy_data)
    selected_data = select_necessary_columns(data_with_duration)
    assert list(selected_data.columns) == ['PULocationID', 'DOLocationID', 'trip_distance', 'trip_duration', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']

def test_transform_data():
    transformed_data = transform_data(dummy_data)
    # Add your assertions here

# Tests for query_data.py
def test_load_query():
    query = load_query('/Users/jrdegbe/Desktop/jlp-data-engineer-test/src/top_5.sql')
    assert isinstance(query, str)

# Tests for visualisation.py
def test_viz_load_query():
    query = viz_load_query('/Users/jrdegbe/Desktop/jlp-data-engineer-test/src/top_5.sql')
    assert isinstance(query, str)

