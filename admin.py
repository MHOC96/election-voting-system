from connection import database_connection
from nominee_see import nominee_see


def admin_login():

    try:
        print("Welcome to the admin dash board")
        admin_login_connection = database_connection()
        admin_find_cursor = admin_login_connection.cursor()

        admin_email = input("Enter admin email:")
        query = "select password from admin where email=%s"
        admin_find_cursor.execute(query, (admin_email,))
        password_details = admin_find_cursor.fetchone()
        attempts = 3
        while attempts:
            if password_details:
                admin_stored_password = password_details[0]
                admin_password = input("Enter admin password:")
                if admin_password == admin_stored_password:
                    print("Welcome admin")
                    return True
                elif attempts == 0:
                    print("Your attempts are finished. Access locked")
                    break
                else:
                    print(
                        f"Incorrect password You have {attempts-1} attempts remaining "
                    )
                    attempts -= 1

            else:
                print("Not a admin")
                break
        if attempts == 0:
            print("Your attempts are finished. Access locked")
    
    except Exception as e:
        print(f"error found:{e}")
    
    finally:
        admin_find_cursor.close()
        admin_login_connection.close()


def find_nominee_if_already_exit(name):
    try:
        find_nominee = database_connection()
        find_nominee_cursor = find_nominee.cursor()
        query = f"select name from nominee where name=%s"
        find_nominee_cursor.execute(query, (name,))
        nominee_detail = find_nominee_cursor.fetchone()
        
        if nominee_detail:
            find_nominee_cursor.close()
            find_nominee.close()
            return False
        find_nominee_cursor.close()
        find_nominee.close()
        return True
    
    except Exception as e:
        print(f"Error found:{e}")
    
    finally:
        find_nominee.close()
        find_nominee_cursor.close()


def add_nominees():
    try:
        adding_nominee = database_connection()
        adding_nominee_cursor = adding_nominee.cursor()
        while True:
            nominee_name = input("Enter nominee_name:")

            if find_nominee_if_already_exit(nominee_name) == True:
                nominee_party = input("Enter nominee_party:")
                query = "insert into nominee(name,nominee_party) values(%s,%s)"
                adding_nominee_cursor.execute(query, (nominee_name, nominee_party))
                adding_nominee.commit()
                print(
                    f"sucuessfully add\nnominee name:{nominee_name}\nnominee party:{nominee_party}"
                )

                ask = input("Do you need to add another nominee(yes/no):").lower()
                if ask == "no":
                    break
            else:
                print(
                    f"{nominee_name} already registered please enter another nominee name"
                )
                continue
    except Exception as e:
        print(f"Error found:{e}")

    finally:
        adding_nominee_cursor.close()
        adding_nominee.close()


def calculate():
    try:
        nominee_see()
        admin_featuers = database_connection()
        count_find_cursor = admin_featuers.cursor()
        nominee_id = int(input("Enter nominee_id admin want to see:"))

        query = """
        SELECT n.nominee_id, n.name, n.nominee_party, COUNT(v.nic_no) AS total_votes
        FROM nominee n
        JOIN voter v ON n.nominee_id = v.nominee_id
        WHERE n.nominee_id = %s
        GROUP BY n.nominee_id, n.name, n.nominee_party;
        """
        count_find_cursor.execute(query, (nominee_id,))
        result = count_find_cursor.fetchone()

        if result:
            print("Nominee ID:", result[0])
            print("Name:", result[1])
            print("Party:", result[2])
            print("Total Votes:", result[3])
        else:
            print("No votes found for nominee_id =", nominee_id)

    except Exception as e:
        print(f"Error found:{e}")

    finally:
        count_find_cursor.close()
        admin_featuers.close()


def admin_main():
    if admin_login() == True:

        print("Press 1 to add nominee details\npress 2 to show results")
        while True:
            try:
                admin_function = int(input("What functions admin need to performe:"))
                if admin_function == 1:
                    add_nominees()
                elif admin_function == 2:
                    calculate()

                need_addition = input("Do admin need another service(yes/no):").lower()

                if need_addition != "yes":
                    print("Thanks")
                    break

            except ValueError as e:
                print("Please enter 1 or 2 only")


