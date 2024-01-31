import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

def load_query(filepath):
    try:
        with open(filepath, 'r') as file:
            return file.read()
    except Exception as e:
        print(f"Failed to read query file: {e}")
        return None

def main():
    # Display library versions
    print(f"Pandas version: {pd.__version__}")
    print(f"Seaborn version: {sns.__version__}")
    print(f"Matplotlib version: {plt.matplotlib.__version__}")

    # Create a connection to the database
    connection_string = "postgresql://postgres:derek@db:5432/my_database"
    try:
        engine = create_engine(connection_string)
    except Exception as e:
        print(f"Failed to create engine: {e}")
        return

    # Load the query from top_5.sql
    query_filepath = '/usr/src/app/top_5.sql'
    query = load_query(query_filepath)
    if query is None:
        return

    # Load the data into a pandas DataFrame
    try:
        df = pd.read_sql_query(query, engine)
    except Exception as e:
        print(f"Failed to load data: {e}")
        engine.dispose()
        return

    # Close the database connection
    engine.dispose()

    # Set the style and color palette of the plots
    sns.set(style="whitegrid")
    sns.set_palette("pastel")

    # Create a line plot
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x='week', y='avg_speed', hue='PULocationID', marker="o")

    # Add titles and labels
    plt.title('Weekly Average Speed per Pickup Location')
    plt.xlabel('Week')
    plt.ylabel('Average Speed (mph)')
    plt.legend(title='Pickup Location ID', bbox_to_anchor=(1.05, 1), loc='upper left')

    # Save the plot to a file
    plt.savefig('/usr/src/app/plot.png')

    # Show the plot
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
