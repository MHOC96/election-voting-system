from connection import database_connection
from tabulate import tabulate
from electorates import display_electoral_districts
from nominee_see import display_nominee_list
from mysql.connector import IntegrityError


def get_voter_details(nic):
    try:
        voter_connection = database_connection()
        if not voter_connection:
            print("Database connection failed")
            return None
            
        voter_details_get_cursor = voter_connection.cursor()

        query = "SELECT nic_number, name, electoral_district, electorates FROM voter_details WHERE nic_number=%s"
        voter_details_get_cursor.execute(query, (nic,))
        voter_details = voter_details_get_cursor.fetchone()

        if voter_details:
            return voter_details
        else:
            print("\nUser not available in the system, please contact Gramasewaka.")
            return None

    except Exception as e:
        print(f"Error found: {e}")
        return None

    finally:
        voter_details_get_cursor.close()
        voter_connection.close()


def voter_vote():
    print("\nWelcome to the voting process")
    voter_vote_connection = database_connection()
    if not voter_vote_connection:
        print("Database connection failed")
        return None
    voter_vote_cursor = voter_vote_connection.cursor()

    try:
        nic_number = int(input("\nEnter NIC number:"))
        voter_details = get_voter_details(nic_number)

        if voter_details:
            stored_nic, stored_name, stored_electoral_district, stored_electorate = voter_details

            while True:
                voter_name = input(
                    "\nEnter voter name (Need to enter name as in NIC/Type 'exit' to exit from voting process):"
                )

                if voter_name.lower() == "exit":
                    break

                elif voter_name != stored_name:
                    print("\nName does not match with NIC number you entered.")
                    continue

                electoral_district, electorate = display_electoral_districts()

                if electoral_district != stored_electoral_district:
                    print(f"\n{voter_name} does not belong to Electoral District: {electoral_district}.")

                elif electorate != stored_electorate:
                    print(f"\n{voter_name} belongs to Electoral District: {electoral_district} but not to Electorate: {electorate}.")
                    continue

                print(f"Vote: {voter_name} is eligible for voting.")
                display_nominee_list()

                vote_nominee = int(input("Enter nominee ID you wish to vote for:"))
                query_vote = "INSERT INTO voter(nic_no, voter_name, electoral_district, electorates, nominee_id) VALUES(%s, %s, %s, %s, %s)"
                voter_vote_cursor.execute(
                    query_vote,
                    (
                        nic_number,
                        voter_name,
                        electoral_district,
                        electorate,
                        vote_nominee,
                    ),
                )
                voter_vote_connection.commit()
                print(f"\nVoter: {voter_name} successfully voted.")
                break

    except ValueError:
        print("\nPlease enter numeric values only.")

    except IntegrityError:
        print(f"\nVoter: {voter_name} has already voted.")

    except Exception as e:
        print(f"\nError encountered: {e}")
        return None

    finally:
        voter_vote_cursor.close()
        voter_vote_connection.close()
