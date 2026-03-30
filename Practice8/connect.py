import psycopg2
from config import load_config

def connect():
    """ Connect to the PostgreSQL database server """
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            print('Successfully connected to the PostgreSQL database.')
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(f"Connection error: {error}")

if __name__ == '__main__':
    connect()