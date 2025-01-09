import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

# Database connection details
DB_HOST = 'localhost'
DB_NAME = 'movie_database'
DB_USER = 'postgres'
DB_PASSWORD = 'letsdoit143*'
DB_PORT = 5433

# File paths for the datasets
PERSON_FILE = '/Users/micky/Documents/Web Projects/assignment/name.basics.tsv'
MOVIES_FILE = '/Users/micky/Documents/Web Projects/assignment/title.basics.tsv'

# Function to connect to the PostgreSQL database
def connect_to_db():
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        print("Connected to the database successfully!")
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        exit()

# Function to import data into PostgreSQL
def import_data(connection, table_name, data_frame):
    cursor = connection.cursor()
    cols = ', '.join(list(data_frame.columns))
    query = f"INSERT INTO {table_name} ({cols}) VALUES %s ON CONFLICT DO NOTHING"

    # Convert dataframe to a list of tuples
    values = [tuple(row) for row in data_frame.to_numpy()]

    try:
        execute_values(cursor, query, values)
        connection.commit()
        print(f"Data imported into {table_name} successfully!")
    except Exception as e:
        connection.rollback()
        print(f"Error importing data into {table_name}: {e}")
    finally:
        cursor.close()

# Main script execution
if __name__ == "__main__":
    # Connect to the database
    conn = connect_to_db()

    # Read the TSV files
    person_data = pd.read_csv(PERSON_FILE, low_memory=False, sep='\t', na_values='\\N')
    movies_data = pd.read_csv(MOVIES_FILE, low_memory=False, sep='\t', na_values='\\N')

    movies_data['isAdult'] = movies_data['isAdult'].apply(lambda x: bool(x) if pd.notnull(x) else None)

    # Replace NaN with None for PostgreSQL compatibility
    person_data = person_data.where(pd.notnull(person_data), None)
    movies_data = movies_data.where(pd.notnull(movies_data), None)

    # Import data into the database
    import_data(conn, 'Person', person_data)
    import_data(conn, 'Movies', movies_data)

    # Close the connection
    conn.close()
    print("Database connection closed.")
