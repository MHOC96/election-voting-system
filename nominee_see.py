from connection import database_connection
from tabulate import tabulate


def display_nominee_list():
    try:
        nominee_connection = database_connection()
        
        if not nominee_connection:
            print("Failed to connect to the database.")
            return False

        nominee_cursor = nominee_connection.cursor()

        nominee_query = "SELECT * FROM nominee"
        nominee_cursor.execute(nominee_query)
        nominee_data = []
        headers = ["Nominee ID", "Nominee Name", "Nominee Party"]
        all_nominee_details = nominee_cursor.fetchall()
        
        for nominee_details in all_nominee_details:
            nominee_id, nominee_name, nominee_party = nominee_details
            nominee_data.append([nominee_id, nominee_name, nominee_party])
            
        if nominee_data:
            print(tabulate(nominee_data, headers=headers, tablefmt="grid"))

        else:
            print("No nominee records found.")
        
    except Exception as e:
        print(f"Error found: {e}")

    finally:
        nominee_cursor.close()
        nominee_connection.close()
