from enum import Enum

import requests
from tqdm import tqdm
#import psycopg2-binary

class TaxiType(Enum):
    Yellow = "yellow"
    Green = "green"
    ForHire = "fhv"
    HighVolume = "fhvhv"

    def __str__(self):
        return str(self.value)


def _filename_for_date(year: int, month: int, taxi_type: TaxiType) -> str:
    assert 2000 < year < 2050
    assert 1 <= month <= 12
    return f"{taxi_type.value}_tripdata_{year:04}-{month:02}.parquet"


def fetch_data(year: int, month: int, taxi_type: TaxiType, output_filename: str):
    url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{_filename_for_date(year, month, taxi_type)}"
    print(f"Fetching dataset at {url}")
    with requests.get(url, stream=True) as response:
        MiB = 1024 * 1024
        total_size_in_bytes = int(response.headers.get("Content-Length", 0))
        chunk_size = MiB // 16
        response.raise_for_status()
        with open(output_filename, "wb") as f:
            with tqdm(
                desc=url,
                total=total_size_in_bytes,
                unit="iB",
                unit_scale=True,
                unit_divisor=1024,
            ) as progress_bar:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    bytes_written = f.write(chunk)
                    progress_bar.update(bytes_written)
    print("Done")


if __name__ == "__main__":
    fetch_data(2021, 3, TaxiType.Yellow, "data-yellow-202103.parquet")
