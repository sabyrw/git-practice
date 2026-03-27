import psycopg2
from config import params

def connect():
    """ Connecting to a PostgreSQL database """
    conn = None
    try:
        conn = psycopg2.connect(**params)
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Connection error: {error}")
        return None

if __name__ == "__main__":
    connection = connect()
    if connection:
        print("Database connection completed successfully!")
        connection.close()