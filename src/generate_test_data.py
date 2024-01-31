import pandas as pd
from datetime import datetime, timedelta
import random

# Function to create synthetic data
def create_synthetic_data(num_rows):
    data = {
        'PULocationID': [random.randint(1, 263) for _ in range(num_rows)],
        'DOLocationID': [random.randint(1, 263) for _ in range(num_rows)],
        'trip_distance': [random.uniform(0.1, 30) for _ in range(num_rows)],
        'tpep_pickup_datetime': [(datetime(2021, 3, 1) + timedelta(minutes=random.randint(0, 30*24*60))) for _ in range(num_rows)],
        'tpep_dropoff_datetime': [(datetime(2021, 3, 1) + timedelta(minutes=random.randint(30*24*60, 31*24*60))) for _ in range(num_rows)],
    }
    df = pd.DataFrame(data)
    return df

# Create synthetic data
num_rows = 100  # Change this to the number of rows you want
synthetic_data = create_synthetic_data(num_rows)

# Save synthetic data to a parquet file
synthetic_data.to_parquet('/Users/jrdegbe/Desktop/jlp-data-engineer-test/data/test_data.parquet', index=False)