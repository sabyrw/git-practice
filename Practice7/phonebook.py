# phonebook.py
import csv
from connect import connect

def insert_contact(name, phone):
    """ Insert a single contact from the console """
    conn = connect()
    if conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", (name, phone))
        conn.commit()
        cur.close()
        conn.close()
        print(f"Contact '{name}' added successfully!")

def insert_from_csv(file_path):
    """ Batch insert contacts from a CSV file """
    conn = connect()
    if conn:
        cur = conn.cursor()
        try:
            with open(file_path, mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    cur.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", (row[0], row[1]))
            conn.commit()
            print("Contacts from CSV uploaded successfully!")
        except Exception as e:
            print(f"CSV Error: {e}")
        finally:
            cur.close()
            conn.close()

def update_contact(contact_id, new_name=None, new_phone=None):
    """ Update contact's name or phone number """
    conn = connect()
    if conn:
        cur = conn.cursor()
        if new_name:
            cur.execute("UPDATE phonebook SET name = %s WHERE id = %s", (new_name, contact_id))
        if new_phone:
            cur.execute("UPDATE phonebook SET phone = %s WHERE id = %s", (new_phone, contact_id))
        conn.commit()
        cur.close()
        conn.close()
        print(f"Contact ID {contact_id} updated.")

def query_contacts(filter_term):
    """ Search contacts by name or phone prefix """
    conn = connect()
    if conn:
        cur = conn.cursor()
        # ILIKE for case-insensitive name search, LIKE for phone prefix
        query = "SELECT * FROM phonebook WHERE name ILIKE %s OR phone LIKE %s"
        cur.execute(query, (f'%{filter_term}%', f'{filter_term}%'))
        rows = cur.fetchall()
        
        print(f"\n--- Search results for '{filter_term}' ---")
        for row in rows:
            print(f"ID: {row[0]} | Name: {row[1]} | Phone: {row[2]}")
        cur.close()
        conn.close()

def delete_contact(identifier):
    """ Delete a contact by name or phone number """
    conn = connect()
    if conn:
        cur = conn.cursor()
        query = "DELETE FROM phonebook WHERE name = %s OR phone = %s"
        cur.execute(query, (identifier, identifier))
        conn.commit()
        cur.close()
        conn.close()
        print(f"Contact matching '{identifier}' deleted.")

# --- Testing the implementation ---
if __name__ == "__main__":
    insert_from_csv("contacts.csv")
    query_contacts("")