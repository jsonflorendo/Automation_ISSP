from Login.login import login
from Login.SI_000 import SI_000
from selenium import webdriver


def run_test_case(case_name):
    # Initialize shared driver
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("http://10.10.99.23/login")
    # login(driver)

    print(f"\n------------------------------Test Case {case_name}------------------------------\n")

    if case_name == "SI-000":
        SI_000(driver)
    else:
        print(f"❌ Incorrect test case name, '{case_name}'. \n")

    driver.quit()

# Ask user whether to run all test cases or a specific one
choice = input("\nDo you want to run all the test cases? (yes/no): ").strip().lower()

if choice == "yes":
    run_test_case("SI-000")
elif choice == "no":
    selected_case = input("Enter test case title (e.g., SI-000.....): ").strip().upper()
    run_test_case(selected_case)
else:
    print("❌ Invalid input. Please enter 'yes' or 'no'. \n")