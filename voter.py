from connection import database_connection
from tabulate import tabulate
from electorates import electoral_district_electorates
from nominee_see import nominee_see
from mysql.connector import IntegrityError


def get_voter_details(nic):
    try:
        voter_connection = database_connection()
        if voter_connection is None:
            print("Database connection failed")
        voter_details_get_cursor = voter_connection.cursor()

        query = "select nic_number,name,electoral_district,electorates from voter_details where nic_number=%s"
        voter_details_get_cursor.execute(query, (nic,))
        voter_details = voter_details_get_cursor.fetchone()

        if voter_details:
            return voter_details
        else:
            print("User not available in the system please contact Gramasewaka")
            return False

    except Exception as e:
        print(f"Error found:{e}")

    finally:
        voter_details_get_cursor.close()
        voter_connection.close()


def voter_vote():
    print("Welcome to the voting process")
    voter_vote_connection = database_connection()
    if voter_vote_connection is None:
        print("Database connection failed")
    voter_vote_cursor = voter_vote_connection.cursor()

    try:
        nic_number = int(input("Enter NIC number:"))
        voter_detals = get_voter_details(nic_number)

        if voter_detals:
            st_nic, st_name, st_electoral_district, st_electorate = voter_detals

            while True:
                voter_name = input("Enter voter name(Need to enter name in NIC/Type exit to exit from voting process):").lower()

                if voter_name=="exit":
                    break
                
                elif voter_name != st_name:
                    print("Name does not match with NIC number you entered:")
                    continue

                eletoral_disctrict, electorate = electoral_district_electorates()

                if eletoral_disctrict != st_electoral_district:
                    print(
                        f"{voter_name} is  not belong to Electoral District :{eletoral_disctrict} "
                    )

                elif electorate != st_electorate:
                    print(
                        f"{voter_name} is belong to Electoral District :{eletoral_disctrict} but not belong to Electorate:{electorate}"
                    )
                    continue

                print(f"voter:{voter_name} is eligible for voting")
                nominee_see()

                vote_nominee = int(input("Enter nominee id you wish to vote:"))
                query_vote = "insert into voter(nic_no,voter_name,electoral_district,electorates,nominee_id) values(%s,%s,%s,%s,%s)"
                voter_vote_cursor.execute(
                    query_vote,
                    (
                        nic_number,
                        voter_name,
                        eletoral_disctrict,
                        electorate,
                        vote_nominee,
                    ),
                )
                voter_vote_connection.commit()
                print(f"voter:{voter_name} Sucuessfully voted")
                break
    
    except IntegrityError:
        print(f" voter:{voter_name} already voted")

    except Exception as e:
        print(f"Error is:{e}")

    finally:
        voter_vote_cursor.close()
        voter_vote_connection.close()



