# 1) Setup & Login
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import sys
import time 
import os

sys.path.append('../Automation_ISSP')
from Login.login import agency_focal_login, driver

agency_focal_login()
wait = WebDriverWait(driver, 15)

# Navigate to Library
if len(driver.window_handles) > 1:
    driver.switch_to.window(driver.window_handles[-1])
driver.get("http://10.10.99.23/library")
print("Reached the Library panel.")
driver.execute_script("window.scrollBy(0, 1000);")
time.sleep(5)


# Click 'Add New' button
wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Add New']"))).click()
print("Add New button clicked.")
time.sleep(5)


def check_element(element, description, index): 
    try:
        assert element, f"❌ Test Case {index} Failed: {description} not found"
        print(f"✅ Test Case {index}: {description} found successfully")
    except AssertionError as ae:
        print(str(ae))
    time.sleep(1)



def main():
    time.sleep(5) 
    test_agency_modal_elements() # TEST CASE 1-17
    time.sleep(5)
    test_empty_fields()
    time.sleep(5)
    test_duplicate_entry()
    time.sleep(10)
    test_valid_entry_addition()
    time.sleep(5)
    test_update_entry()
    time.sleep(5)
    test_delete_entry()
    time.sleep(5)
    driver.quit()


# TEST CASE 1-17: Labels, inputs, buttons, and modal checking
def test_agency_modal_elements():
    print("\nTest Cases 1-17: Checking Agency Modal Elements")

    try:
        elements = [
            (driver.find_element(By.CLASS_NAME, "rounded-pnl"), "Office Modal container"),
            (driver.find_element(By.XPATH, "//span[contains(text(), 'Parent Office')]"), "Parent Office label"),
            (driver.find_element(By.ID, "ofc_parent"), "Parent Office input"),
            (driver.find_element(By.XPATH, "//span[contains(text(), 'Name of Office')]"), "Name of Office label"),
            (driver.find_element(By.ID, "ofc_name"), "Name of Office input"),
            (driver.find_element(By.XPATH, "//span[contains(., 'Alias') and contains(., '(short name)')]"), "Alias (short name) label"),
            (driver.find_element(By.ID, "ofc_code"), "Alias input"),
            (driver.find_element(By.XPATH, "//span[contains(text(), 'Function')]"), "Function label"),
            (driver.find_element(By.ID, "chartDesc"), "Function input"),
            (driver.find_element(By.XPATH, "//span[contains(text(), 'Name of Office Head')]"), "Office Head label"),
            (driver.find_element(By.ID, "ofc_head_fname"), "Office Head First Name input"),
            (driver.find_element(By.ID, "ofc_head_mi"), "Office Head Middle Initial input"),
            (driver.find_element(By.ID, "ofc_head_lname"), "Office Head Last Name input"),
            (driver.find_element(By.ID, "ofc_head_sfx"), "Office Head Suffix input"),
            (driver.find_element(By.CSS_SELECTOR, "svg.fa-xmark"), "Close (X) button"),
            (driver.find_element(By.XPATH, "//button[normalize-space()='Cancel']"), "Cancel button"),
            (driver.find_element(By.XPATH, "//button[normalize-space()='Save']"), "Save button"),
        ]

        for idx, (element, description) in enumerate(elements, start=1):
            check_element(element, description, idx)

    except Exception as e:
        print(f"❌ Test Cases 1-17 FAILED: Unexpected error during modal element checks: {e}")

# TEST CASE 18: All inputs left with empty fields
def test_empty_fields():
    print("\n********* ERROR TEST CASES *********/")
    print("\n/********* TEST CASE 18: Empty Entry Fields *********/")
    time.sleep(5)
    save_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Save']"))
    )
    save_button.click()
    print("Save button clicked.")

    # Wait for any error to appear
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "p.text-error"))
    )

    required_fields = {
        "ofc_name": "Name of Office",
        "ofc_code": "Alias",
        "ofc_head_fname": "Head First Name",
        "ofc_head_lname": "Head Last Name"
    }

    all_passed = True

    for field_id, label in required_fields.items():
        try:
            field = driver.find_element(By.ID, field_id)
            container = field.find_element(By.XPATH, "./ancestor::div[2]")
            error = container.find_element(By.CSS_SELECTOR, "p.text-error")

            if "This field is required." in error.text.strip():
                print(f"✅ {label}: Required field error shown as expected.")
            else:
                print(f"❌ {label}: Incorrect error message.")
                all_passed = False
        except Exception:
            print(f"❌ {label}: Error message not found.")
            all_passed = False

    try:
        assert all_passed, "❌ Test Case 15 Failed: Missing or incorrect error messages."
        print("✅ Test Case 15 Passed: All required field errors displayed correctly.")
    except AssertionError as ae:
        print(str(ae))

def select_parent_office(value):  
    dropdown_toggle = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#ofc_parent .vs__dropdown-toggle"))
    )
    dropdown_toggle.click()
    time.sleep(1)

    input_box = driver.find_element(By.CSS_SELECTOR, "#ofc_parent input.vs__search")
    input_box.send_keys(value)
    time.sleep(1)
    input_box.send_keys(Keys.ENTER)

def is_duplicate_error_displayed(field_id, expected_message):
    try:
        input_elem = driver.find_element(By.ID, field_id)
        parent_div = input_elem.find_element(By.XPATH, "./parent::*")
        error_elem = parent_div.find_element(By.XPATH, ".//p[contains(@class, 'text-error')]")
        return expected_message.lower() in error_elem.text.lower() and error_elem.is_displayed()
    except Exception as e:
        print(f"⚠️ Could not locate error for '{field_id}': {str(e)}")
        return False

# TEST CASE 19: Duplicate Entry
def test_duplicate_entry():
    print("\n/********* TEST CASE 16: Duplicate Entry *********/")

    duplicate_data = {
        "ofc_parent": "Planning and Evaluation Service20",
        "ofc_name": "Department of Science and Technology",
        "ofc_code": "DOST",
        "chartDesc": "djdhsdh",
        "ofc_head_fname": "Ma. Donna",
        "ofc_head_mi": "d.",
        "ofc_head_lname": "Fidelino",
        "ofc_head_sfx": "jr"
    }

    # First, select the custom dropdown
    select_parent_office(duplicate_data["ofc_parent"])

    # Then, fill the rest of the fields
    for field_id, value in duplicate_data.items():
        if field_id == "ofc_parent":
            continue  # already handled
        input_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, field_id))
        )
        input_field.clear()
        input_field.send_keys(value)
        time.sleep(1)

    # Submit
    save_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Save']"))
    )
    save_button.click()
    print("Save button clicked.")
    time.sleep(3)

    # Check for duplicate error messages
    office_name_error = is_duplicate_error_displayed("ofc_name", "Name of Office already exists")

    try:
        assert office_name_error, "❌ Test Case 19 Failed: Duplicate error for 'Name of Office' not found."
        print("✅ Test Case 19 Passed: Duplicate error for 'Name of Office' is shown.")
    except AssertionError as ae:
        print(str(ae))

# TEST CASE 20: Adding Valid Entry
def test_valid_entry_addition():
    print("\n/********* SUCCESSFUL TEST CASE *********/")
    print("\n/********* TEST CASE 20: Valid Entry Inputs *********/")

    # Clear and locate all inputs
    name_of_office_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ofc_name")))
    alias_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ofc_code")))
    function_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "chartDesc")))
    firstName_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ofc_head_fname")))
    mi_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ofc_head_mi")))
    surname_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ofc_head_lname")))
    suffix_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ofc_head_sfx")))

    # Select from dropdown
    select_parent_office("Planning and Evaluation Service20")  # Provide your actual office name here

    # Clear regular inputs
    for input_elem in [name_of_office_input, alias_input, function_input, firstName_input, mi_input, surname_input, suffix_input]:
        input_elem.clear()
        input_elem.send_keys(Keys.CONTROL + "a")
        input_elem.send_keys(Keys.DELETE)
        time.sleep(0.5)

    # Input values
    input_data = {
        "ofc_name": "Test",
        "ofc_code": "TEST",
        "chartDesc": "Test",
        "ofc_head_fname": "Test",
        "ofc_head_mi": "T",
        "ofc_head_lname": "User",
        "ofc_head_sfx": "Jr"
    }

    for field_id, value in input_data.items():
        input_elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, field_id)))
        input_elem.send_keys(value)
        time.sleep(1)

    print("✅ Inputted valid agency details.")

    # Submit form
    save_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Save']"))
    )
    save_button.click()
    print("Save button clicked.")

    # Confirmation
    try:
        WebDriverWait(driver, 25).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//h2[contains(@class,'swal2-title') and contains(text(), 'added successfully')]")
            )
        )
        print("✅ Confirmation popup appeared.")

        ok_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.swal2-confirm"))
        )
        ok_button.click()
        print("✅ Entry added successfully. OK button clicked.")
    except:
        print("❌ Confirmation alert not found or failed to click OK.")
        return

    # Navigate to Library page
    driver.get("http://10.10.99.23/library")
    time.sleep(5)
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//table//tbody/tr"))
    )
    
    # Validate the data in table
    expected_values = {
        "off_code": input_data["ofc_code"],
        "off_name": input_data["ofc_name"],
        "off_head": f"{input_data['ofc_head_fname']} {input_data['ofc_head_mi']}. {input_data['ofc_head_lname']} {input_data['ofc_head_sfx']}".strip()
    }

    rows = driver.find_elements(By.XPATH, "//table//tbody/tr")
    target_row = next((row for row in rows if row.find_elements(By.TAG_NAME, "td")[0].text.strip() == expected_values["off_code"]), None)

    if target_row:
        cells = target_row.find_elements(By.TAG_NAME, "td")
        actual_values = {
            "off_code": cells[0].text.strip(),
            "off_name": cells[1].text.strip(),
            "off_head": cells[2].text.strip()
        }
        try:
            assert actual_values == expected_values, (
                f"❌ Test Case 20 Failed: Mismatch\nExpected: {expected_values}\nGot: {actual_values}"
            )
            print("✅ Test Case 20 Passed: All values matched in the identified row.")
        except AssertionError as ae:
            print(str(ae))
    else:
        print(f"❌ Test Case 20 Failed: Could not find row with code '{expected_values['off_code']}'")

# TEST CASE 21: Updating Recent Entry
def test_update_entry():
    print("\n\n/********* TEST CASE 21: UPDATE Recent Entry *********/")
    
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//table//tbody/tr")))
    time.sleep(5)
    rows = driver.find_elements(By.XPATH, "//table//tbody/tr")
    target_row = None
    
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if cells and cells[0].text.strip() == "TEST":
            target_row = row
            break

    if target_row:
        target_row.click()
        print("✅ Target row clicked. Modal should appear.")
        
    time.sleep(5)  

    name_of_office_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ofc_name")))
    alias_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ofc_code")))
    function_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "chartDesc")))
    firstName_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ofc_head_fname")))
    mi_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ofc_head_mi")))
    surname_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ofc_head_lname")))
    suffix_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ofc_head_sfx")))

    # Select from dropdown
    select_parent_office("Planning and Evaluation Service20")  # Provide your actual office name here

    # Clear regular inputs
    for input_elem in [name_of_office_input, alias_input, function_input, firstName_input, mi_input, surname_input, suffix_input]:
        input_elem.clear()
        input_elem.send_keys(Keys.CONTROL + "a")
        input_elem.send_keys(Keys.DELETE)
        time.sleep(0.5)

    # Input values
    input_data = {
        "ofc_name": "Test-New",
        "ofc_code": "TEST-NEW",
        "chartDesc": "Test-New",
        "ofc_head_fname": "New-Test",
        "ofc_head_mi": "T",
        "ofc_head_lname": "User",
        "ofc_head_sfx": "Jr"
    }

    for field_id, value in input_data.items():
        input_elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, field_id)))
        input_elem.send_keys(value)
        time.sleep(1)

    print("✅ Inputted valid agency details.")

    # Submit form
    save_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Save']"))
    )
    save_button.click()
    print("Save button clicked.")

    try:
        WebDriverWait(driver, 25).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//h2[contains(@class,'swal2-title') and contains(text(), 'Office updated successfully.')]")
            )
        )
        print("✅ Confirmation popup appeared.")

        ok_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.swal2-confirm"))
        )
        ok_button.click()
        print("✅ Entry updated successfully. OK button clicked.")
    except:
        print("❌ Confirmation alert not found or failed to click OK.")
        return
    
    driver.get("http://10.10.99.23/library")
    time.sleep(5)
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//table//tbody/tr"))
    )
    
    # Validate the data in table
    expected_values = {
        "off_code": input_data["ofc_code"],
        "off_name": input_data["ofc_name"],
        "off_head": f"{input_data['ofc_head_fname']} {input_data['ofc_head_mi']}. {input_data['ofc_head_lname']} {input_data['ofc_head_sfx']}".strip()
    }

    rows = driver.find_elements(By.XPATH, "//table//tbody/tr")
    target_row = next((row for row in rows if row.find_elements(By.TAG_NAME, "td")[0].text.strip() == expected_values["off_code"]), None)

    if target_row:
        cells = target_row.find_elements(By.TAG_NAME, "td")
        actual_values = {
            "off_code": cells[0].text.strip(),
            "off_name": cells[1].text.strip(),
            "off_head": cells[2].text.strip()
        }
        try:
            assert actual_values == expected_values, (
                f"❌ Test Case 21 Failed: Mismatch\nExpected: {expected_values}\nGot: {actual_values}"
            )
            print("✅ Test Case 21 Passed: All values matched in the identified row.")
        except AssertionError as ae:
            print(str(ae))
    else:
        print(f"❌ Test Case 21 Failed: Could not find row with code '{expected_values['off_code']}'")

# TEST CASE 21: Deleting Recent Entry
def test_delete_entry():
    target_alias="TEST-NEW"
    print("\n\n/********* TEST CASE 22: DELETE Recent Entry *********/")
    time.sleep(10)

    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//table//tbody/tr")))

    def find_row_by_alias(alias):
        rows = driver.find_elements(By.XPATH, "//table//tbody/tr")
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if cells and cells[0].text.strip() == alias:
                return row
        return None

    target_row = find_row_by_alias(target_alias)
    alias_to_delete = ""

    if target_row:
        columns = target_row.find_elements(By.TAG_NAME, "td")
        if len(columns) >= 3:
            alias_to_delete = columns[0].text.strip()
            print(f" Alias to delete: {alias_to_delete}")
        else:
            print("❌ Not enough columns found in the row")
    else:
        print(f"❌ Could not find row with alias '{target_alias}'")

    if target_row:
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(target_row)).click()
            print("✅ Row clicked successfully. Modal should appear.")
        except Exception as e:
            print(f"❌ Failed to click the row: {e}")
            return

    try:
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "ofc_name")))
        print("✅ Modal appeared.")
    except:
        print("❌ Modal did not appear")
        return
    

    try:
        delete_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Delete']"))
        )
        delete_button.click()
        print("✅ Delete button clicked.")
    except:
        print("❌ Could not find or click delete button.")
        return

    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h2[text()='Are you sure you want to delete this item?']"))
        )
        print("✅ Delete confirmation dialog appeared.")
    except:
        print("❌ Delete confirmation dialog did not appear.")
        return

    try:
        confirm_delete_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'swal2-confirm') and text()='Delete']"))
        )
        confirm_delete_btn.click()
        print("✅ Confirm delete clicked.")
    except:
        print("❌ Failed to confirm delete.")
        return

    try:
        ok_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.swal2-confirm"))
        )
        ok_button.click()
        print("✅ Success alert closed.")
    except:
        print("❌ OK button not found after deletion.")

    time.sleep(5)
    driver.get("http://10.10.99.23/library")

    try:
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//table//tbody")))
        print("✅ Page reloaded successfully.")
    except:
        print("❌ Error reloading page.")
        return

    rows = driver.find_elements(By.XPATH, "//table//tbody/tr")
    
    remaining_aliases = [
        row.find_elements(By.TAG_NAME, "td")[0].text.strip()
        for row in rows if row.find_elements(By.TAG_NAME, "td")
    ]
    try:
        assert alias_to_delete, "❌ Test Case 22 Failed: Could not capture alias_to_delete for verification."
        assert alias_to_delete not in remaining_aliases, f"❌ Test Case 22 Failed: '{alias_to_delete}' still found in the table."
        print(f"✅ Test Case 22 Passed: '{alias_to_delete}' entry successfully deleted from the table.")
    except AssertionError as ae:
        print(str(ae))

    print("/********* END OF THE TEST *********/")
if __name__ == "__main__":
    main()