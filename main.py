from voter import voter_vote
from admin import admin_main


def start_system():
    try:
        print("Welcome to the E-Voting System! This is a demo.")
        
        while True:
            user_input = input("Type 'vote' to enter the voting process: ").lower()
            
            if user_input == "vote":
                voter_vote()
                break
            elif user_input == "admin-voting":
                admin_main()
                break
            else:
                print("Invalid input. Please type 'vote' to enter the voting process.")
    
    except Exception as e:
        print(f"Error encountered: {e}")


if __name__ == "__main__":
    start_system()
