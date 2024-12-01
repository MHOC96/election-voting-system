from tabulate import tabulate


def display_electoral_districts():
    district_data = [
        [1, "Colombo", "Maharagama", "Dehiwala"],
        [2, "Gampaha", "Negombo", "Gampaha"],
        [3, "Kalutara", "Panadura", "Kalutara"],
        [4, "Kandy", "Yatinuwara", "Harispattuwa"],
        [5, "Matale", "Laggala", "Dambulla"],
        [6, "Nuwara Eliya", "Kotmale", "Hanguranketha"],
        [7, "Galle", "Balapitiya", "Habaraduwa"],
        [8, "Matara", "Deniyaya", "Hakmana"],
        [9, "Hambantota", "Beliatta", "Tissamaharamaya"],
        [10, "Jaffna", "Kayts", "Kilinochchi"],
        [11, "Vanni", "Mannar", "Vavuniya"],
        [12, "Batticaloa", "Kalkudah", "Padiruppu"],
        [13, "Digamadulla", "Ampara", "Samanturai"],
        [14, "Trincomalee", "Seruwila", "Mutur"],
        [15, "Kurunegala", "Wariyapola", "Yapahuwa"],
        [16, "Puttalam", "Chillaw", "Anamaduwa"],
        [17, "Anuradhapura", "Horowpothana", "Kalawewa"],
        [18, "Polonnaruwa", "Minneriya", "Medirigiriya"],
        [19, "Badulla", "Welimada", "Bandarawela"],
        [20, "Monaragala", "Bibila", "Wellawaya"],
        [21, "Ratnapura", "Rakwana", "Kolonna"],
        [22, "Kegalle", "Aranayake", "Yatiyantota"],
    ]
    
    headers = [
        "District Number",
        "Electoral District",
        "Electorate 1",
        "Electorate 2",
    ]

    print(tabulate(district_data, headers=headers, tablefmt="grid"))
    
    while True:
        try:
            district_number = int(input("\nEnter a District number between 1 and 22:"))
            if district_number in range(1, 23):
                electoral_district = district_data[district_number - 1][1]
                electorate_choice = int(input("Enter 1 for Electorate 1, or 2 for Electorate 2:"))
                
                if electorate_choice in [1, 2]:
                    electorate = district_data[district_number - 1][electorate_choice + 1]
                    print(f"\nSelected Electoral District: {electoral_district}")
                    print(f"Selected Electorate: {electorate}")
                    return electoral_district, electorate
                else:
                    print("\nInvalid choice. Please enter 1 or 2.")
                    continue
            else:
                print("\nInvalid district number. Please enter a number between 1 and 22.")
                continue
        except ValueError:
            print("\nInvalid input. Please enter numeric values only.")
            continue
