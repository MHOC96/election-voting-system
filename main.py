from voter import voter_vote
from admin import admin_main


def main():
    try:
        print("Welcome to the E-Voting System This is demo")
        while True:
            order = input("Type vote to enter to voting process:").lower()
            if order == "vote":
                voter_vote()
                break
            elif order == "admin-voting":
                admin_main()
                break
            else:
                print("Please type 'vote' to enter voting process")
    except Exception as e:
        print(f"Error found:{e}")


if __name__ == "__main__":
    main()
