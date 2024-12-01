from connection import database_connection
from tabulate import tabulate
from nominee_see import display_nominee_list

def get_top3_nominees():
    try:
        top_3=database_connection()
        
        if not top_3:
            print("Cannot connected to database:")
            return False

        top_3_find_cursor=top_3.cursor()
        query = """
        SELECT 
            n.nominee_id,
            n.name AS nominee_name,
            n.nominee_party,
            COUNT(v.nominee_id) AS vote_count
        FROM 
            voter v
        JOIN 
            nominee n
        ON 
            v.nominee_id = n.nominee_id
        GROUP BY 
            n.nominee_id, n.name, n.nominee_party
        ORDER BY 
            vote_count DESC
        LIMIT 3;
        """
        
        top_3_find_cursor.execute(query)
        table_data=[]

        for rank,nominee_details in enumerate(top_3_find_cursor.fetchall(), start=1):
                print(nominee_details,rank)
                nominee_id,nominee_name,nominee_party,votes=nominee_details
                table_data.append([rank,nominee_name,nominee_party,votes])

        table_headers=["Place","Nominee Name","Nominee Party","Total Votes"]
        print(tabulate(table_data,headers=table_headers,tablefmt="grid"))
        
    except Exception as e:
        print(f"Error found:{e}")
        
    finally:
        top_3_find_cursor.close()
        top_3.close()

def individual_nominee_vote():
    try:
        di()
        vote_count = database_connection()
        if not vote_count :
            print("Database connection failed")
            return

        count_find_cursor = vote_count.cursor()
        nominee_id = int(input("Enter nominee_id admin wants to see:"))

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
        print(f"Error found: {e}")

    finally:
        count_find_cursor.close()
        vote_count.close()

