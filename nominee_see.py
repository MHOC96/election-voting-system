from connection import database_connection
from tabulate import tabulate


def nominee_see():
    try:
        nominee_view_connection = database_connection()
        if nominee_view_connection is None:
            print("Database connection failed")
        see_nominee_cursor = nominee_view_connection.cursor()
        nominee_see_query = "select * from nominee"
        see_nominee_cursor.execute(nominee_see_query)
        table_data = []
        headers = ["Nominee ID", "Nominee Name", "Nominee Party"]
        while True:
            nominee_details = see_nominee_cursor.fetchone()
            if nominee_details:
                nominee_id, nominee_name, nominee_party = nominee_details
                table_data.append([nominee_id, nominee_name, nominee_party])
            break

        print(tabulate(table_data, headers=headers, tablefmt="grid"))
    except Exception as e:
        print(f"error found:{e}")

    finally:
        see_nominee_cursor.close()
        nominee_view_connection.close()
