from connection import database_connection
from admin_count_functions import *


def admin_login():
    try:
        print("Welcome to the admin dashboard")
        admin_connection = database_connection()

        if not admin_connection:
            print("Database connection failed")
            return None

        admin_cursor = admin_connection.cursor()
        
        max_email_attempts = 3
        max_password_attempts = 3
        
        for email_attempt in range(max_email_attempts):
            admin_email = input("Enter admin email:").strip()
            query = "SELECT password FROM admin WHERE email=%s"
            admin_cursor.execute(query, (admin_email,))
            password_details = admin_cursor.fetchone()
            
            if not password_details:
                remaining_email_attempts = max_email_attempts - email_attempt - 1
                print(f"Incorrect email address. You have {remaining_email_attempts} attempts remaining.")
                continue

            for password_attempt in range(max_password_attempts):
                stored_password = password_details[0]
                admin_password = input("Enter admin password:").strip()
                if admin_password == stored_password:
                    print("Welcome admin")
                    return True
                else:
                    remaining_password_attempts = max_password_attempts - password_attempt - 1
                    print(f"Incorrect password. You have {remaining_password_attempts} attempts remaining.")
            
            print("Your password attempts are finished. Access locked.")
            return False
        
        print("Your email attempts are finished. Access locked.")
        return False

    except Exception as e:
        print(f"Error found: {e}")
        return False

    finally:
        admin_cursor.close()
        admin_connection.close()


def nominee_exists(name):
    try:
        connection = database_connection()

        if not connection:
            print("Database connection failed")
            return None

        cursor = connection.cursor()
        query = "SELECT name FROM nominee WHERE name=%s"
        cursor.execute(query, (name,))
        nominee_details = cursor.fetchone()

        if nominee_details:
            cursor.close()
            connection.close()
            return False
        
        return True

    except Exception as e:
        print(f"Error found: {e}")
        return None

    finally:
        connection.close()
        cursor.close()


def add_nominee_details():
    try:
        connection = database_connection()
        if not connection:
            print("Database connection failed")
            return False

        cursor = connection.cursor()
        while True:
            nominee_name = input("Enter nominee name:")

            if nominee_exists(nominee_name):
                nominee_party = input("Enter nominee party:")
                query = "INSERT INTO nominee(name, nominee_party) VALUES(%s, %s)"
                cursor.execute(query, (nominee_name, nominee_party))
                connection.commit()
                print(f"Successfully added nominee\nNominee name: {nominee_name}\nNominee party: {nominee_party}")

                ask = input("Do you need to add another nominee? (yes/no):").lower().strip()
                if ask == "no":
                    break
            else:
                print(f"{nominee_name} is already registered. Please enter another nominee name.")
                continue

    except Exception as e:
        print(f"Error found: {e}")
        return False

    finally:
        cursor.close()
        connection.close()


def admin_vote_options():
    try:
        while True:
            print("Select an option:")
            print("1 - Individual count")
            print("2 - Get top 3 nominees")
            print("exit - Exit the program")

            option_choice = input("Enter your choice:").strip().lower()
            
            if option_choice in ("1", "2", "exit"):
                if option_choice == "1":
                    individual_nominee_vote()
                elif option_choice == "2":
                    get_top3_nominees()
                elif option_choice == "exit":
                    print("Exiting the program. Goodbye!")
                    break
            else:
                print("Invalid input. Please enter '1', '2', or 'exit'.")
    except Exception as e:
        print(f"Error found: {e}")


def admin_main():
    if admin_login():
        print("Press 1 to add nominee details\nPress 2 to show results")
        while True:
            try:
                admin_function = input("What function would the admin like to perform? (Type 'exit' to exit):").lower().strip()

                if admin_function == "1":
                    add_nominee_details()
                elif admin_function == "2":
                    admin_vote_options()
                elif admin_function == "exit":
                    print("Exiting the program. Goodbye!")
                    break
                else:
                    print("Invalid option. Please enter '1', '2', or 'exit'.")
                    continue
            
                need_addition = input("Would the admin like to perform another action? (yes/no): ").lower().strip()

                if need_addition != "yes":
                    print("Thanks for using the admin dashboard. Goodbye!")
                    break

            except Exception as e:
                print(f"An error occurred: {e}")
