import psycopg2
from config import load_config

def upsert_contact(name, phone):
    """ Calls the upsert_contact procedure """
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
                conn.commit()
                print(f"Contact processed: {name}")
    except Exception as e:
        print(f"Error during upsert: {e}")

def search_contacts(pattern):
    """ Calls the get_contacts_by_pattern function """
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM get_contacts_by_pattern(%s)", (pattern,))
                rows = cur.fetchall()
                print(f"Search results for '{pattern}':")
                for row in rows:
                    print(row)
    except Exception as e:
        print(f"Search error: {e}")

def delete_contact(identifier):
    """ Calls the delete_contact procedure """
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("CALL delete_contact(%s)", (identifier,))
                conn.commit()
                print(f"Contact deleted successfully: {identifier}")
    except Exception as e:
        print(f"Delete error: {e}")

if __name__ == "__main__":
    # Test cases
    print("--- Upserting Contact ---")
    upsert_contact("John Doe", "123456789")
    
    print("\n--- Searching Contacts ---")
    search_contacts("John")
    
    print("\n--- Deleting Contact ---")
    delete_contact("123456789")