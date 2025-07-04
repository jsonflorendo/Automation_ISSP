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
from Login.login import login, driver

login()
wait = WebDriverWait(driver, 15)

# Navigate to Library
if len(driver.window_handles) > 1:
    driver.switch_to.window(driver.window_handles[-1])
driver.get("http://10.10.99.23/library")
print("Reached the Library panel.")
driver.execute_script("window.scrollBy(0, 1000);")
time.sleep(5)

# Auxillary functions
def check_element(element, description, index): # TEST CASE 1-13
    try:
        assert element, f"❌ Test Case {index} Failed: {description} not found"
        print(f"✅ Test Case {index}: {description} found successfully")
    except AssertionError as ae:
        print(str(ae))
    time.sleep(1)

def is_duplicate_error_displayed(field_id):     # TEST CASE 16
    try:
        container = driver.find_element(By.XPATH, f"//input[@id='{field_id}']/parent::*")
        error = container.find_element(By.CSS_SELECTOR, "p.text-error")
        return "already exists" in error.text and error.is_displayed()
    except:
        return False

# Click 'Add New' button
wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Add New']"))).click()
print("Add New button clicked.")

# Main function
def main():
    time.sleep(5)
    test_agency_modal_elements()    
    time.sleep(5)
    test_agency_logo_image_upload()
    time.sleep(5)
    test_empty_fields()
    time.sleep(5)
    test_duplicate_entry()
    time.sleep(5)
    test_invalid_website_link()
    time.sleep(5)
    test_invalid_field_formats()
    time.sleep(5)
    test_valid_entry_addition()
    time.sleep(5)
    test_cancel_button_redirect()
    time.sleep(5)
    update_recent_agency_entry()
    time.sleep(5)
    delete_recent_agency_entry()
    time.sleep(5)
    
    driver.quit()

# TEST CASE 1-13: Labels, inputs, buttons, and modal checking
def test_agency_modal_elements():
    time.sleep(5)

    # Elements for Agency Logo and Upload Modal
    agencyLogo_label = driver.find_element(By.XPATH, "//span[contains(@class, 'label-text') and contains(text(), 'Agency Logo')]")
    agencyLogo_upload_modal = driver.find_element(By.XPATH, "//div[contains(@class, 'image-upload') and contains(@class, 'small-upload')]")

    # Form section
    agency_modal = driver.find_element(By.XPATH, "//div[contains(@class, 'rounded-pnl')]//p[contains(text(), 'Agency / Institution')]/ancestor::div[contains(@class, 'rounded-pnl')]//form")

    # Labels and Inputs
    agencyName_label = driver.find_element(By.XPATH, "//span[contains(@class, 'label-text') and contains(text(), 'Agency Name')]")
    agencyName_input = driver.find_element(By.XPATH, "//input[@id='agn_name']")

    alias_label = driver.find_element(By.XPATH, "//span[contains(text(), 'Alias') and .//i[contains(text(), '(short name)')]]")
    alias_input = driver.find_element(By.XPATH, "//input[@id='agn_code']")

    agencyGroup_label = driver.find_element(By.XPATH, "//span[contains(text(), 'Agency Group')]")
    agencyGroup_dropdown = driver.find_element(By.XPATH, "//select[@id='agn_group']")

    agencyLink_label = driver.find_element(By.XPATH, "//span[contains(text(), 'Agency Official Website Link')]")
    agencyLink_input = driver.find_element(By.XPATH, "//input[@id='agn_website']")

    agencyHeadName_label = driver.find_element(By.XPATH, "//span[contains(text(), 'Name of Agency Head')]")
    agencyHeadFirstName_input = driver.find_element(By.XPATH, "//input[@id='agn_head_fname']")
    agencyHeadMI_input = driver.find_element(By.XPATH, "//input[@id='agn_head_mi']")
    agencyHeadSurname_input = driver.find_element(By.XPATH, "//input[@id='agn_head_lname']")
    agencyHeadSuffix_input = driver.find_element(By.XPATH, "//input[@id='agn_head_sfx']")

    close_button = driver.find_element(By.CSS_SELECTOR, "svg.fa-xmark")
    cancel_button = driver.find_element(By.XPATH, "//button[normalize-space()='Cancel']")
    save_button = driver.find_element(By.XPATH, "//button[normalize-space()='Save']")

    print("/*********Agency / Institution*********/")
    test_cases = [
        (agencyLogo_label and agencyLogo_upload_modal, "'Agency Logo' label and 'Upload Modal"),
        (agency_modal, "Agency/Institution form"),
        (agencyName_label and agencyName_input, "'Agency Name' label and input"),
        (alias_label and alias_input, "'Alias' label and input"),
        (agencyGroup_label and agencyGroup_dropdown, "'Agency Group' label and dropdown"),
        (agencyLink_label and agencyLink_input, "'Agency Official Website Link' label and input"),
        (agencyHeadName_label, "'Name of Agency Head' label"),
        (agencyHeadFirstName_input, "'First Name' input"),
        (agencyHeadMI_input, "'Middle Initial' input"),
        (agencyHeadSurname_input, "'Surname' input"),
        (agencyHeadSuffix_input, "'Suffix' input"),
        (close_button, "Close button"),
        (cancel_button, "Cancel button"),
        (save_button, "Save button")
    ]

    for i, (condition, description) in enumerate(test_cases):
        check_element(condition, description, i)

    time.sleep(5)

# TEST CASE 14: Uploading Agency Logo Image
def test_agency_logo_image_upload():
    print("\nTest Case 14: Uploading and Removing Agency Logo Image with Confirmation and Success Alert")

    image_path = r"C:\xampp\htdocs\Automation_ISSP\07_02_25\source\DOST_Logo.png"

    if not os.path.exists(image_path):
        print("❌ Test Failed 14: Image file not found at path:", image_path)
        return

    try:
        wait = WebDriverWait(driver, 10)

        # Reveal  file input and upload image
        file_input = driver.find_element(By.XPATH, "//div[contains(@class, 'image-upload')]//input[@type='file']")
        driver.execute_script("arguments[0].style.display = 'block';", file_input)
        file_input.send_keys(image_path)

        wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'image-preview')]//img")))
        wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'image-preview')]//span[contains(text(), 'DOST_Logo.png')]")))

        print("✅ Test Case 14 Passed: Image uploaded and preview displayed successfully")
        time.sleep(1)

        # Click the X icon
        delete_icon = driver.find_element(By.XPATH, "//div[contains(@class, 'image-preview')]//span[contains(@class, 'delete-icon')]")
        driver.execute_script("arguments[0].click();", delete_icon)
        time.sleep(2)
        # Wait and click "Delete" in first confirmation modal
        delete_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'swal2-confirm') and normalize-space(text())='Delete']")))
        delete_button.click()
        time.sleep(2)
        # Wait and click "OK" in success modal
        ok_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'swal2-confirm') and normalize-space(text())='OK']")))
        ok_button.click()
        time.sleep(2)
        # Wait for preview to disappear
        preview_removed = False
        try:
            wait.until(EC.invisibility_of_element_located((By.XPATH, "//div[contains(@class, 'image-preview')]")))
            preview_removed = True
        except:
            preview_removed = False

        try:
            assert preview_removed, "❌ Remove Failed: Image preview still present"
            print("✅ Remove Success: Image preview removed after OK confirmation")
        except AssertionError as ae:
            print(str(ae))

    except Exception as e:
        print("❌ Test Case 14 Failed with Exception:", str(e))

# TEST CASE 15: All inputs left with empty fields
def test_empty_fields():
    print("********* ADD AGENCY: ERROR TEST CASES *********/")
    print("\n/********* TEST CASE 15: Empty Entry Fields *********/")
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
        "agn_name": "Agency Name",
        "agn_code": "Alias",
        "agn_group": "Agency Group",
        "agn_website": "Website",
        "agn_head_fname": "Head First Name",
        "agn_head_lname": "Head Last Name"
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

# TEST CASE 16: Duplicate Agency Registration
def test_duplicate_entry():
    print("\n/********* TEST CASE 16: Duplicate Entry *********/")

    duplicate_data = {
        "agn_name": "Central Office",
        "agn_code": "CO",
        "agn_group": "Regional Offices",
        "agn_website": "https://www.dost.gov.ph/",
        "agn_head_fname": "Renato",
        "agn_head_mi": "U.",
        "agn_head_lname": "Solidum",
        "agn_head_sfx": "Jr."
    }

    # Fill the form
    for field_id, value in duplicate_data.items():
        input_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, field_id)))
        input_field.send_keys(value)
        time.sleep(2)

    # Submit
    save_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Save']")))
    save_button.click()
    print("Save button clicked.")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'Agency')]"))
    )

    time.sleep(5)
    agency_name_ok = is_duplicate_error_displayed("agn_name")
    website_ok = is_duplicate_error_displayed("agn_website")

    try:
        assert agency_name_ok and website_ok, (
            "❌ Test Case 16 Failed:\n"
            + (" - Agency Name duplicate error not found or not visible.\n" if not agency_name_ok else "")
            + (" - Website duplicate error not found or not visible." if not website_ok else "")
        )
        print("✅ Test Case 16 Passed: Duplicate Agency Name and Website errors are shown.")
    
    except AssertionError as ae:
        print(str(ae))

# TEST CASE 17:Invalid Website Link Format
def test_invalid_website_link():
    print("\n/********* TEST CASE 17: Invalid Website Link *********/")

    invalid_url = "Lorem ipsum dolor sit amet, consectetuer adipiscing"

    # Wait for the website input field and enter invalid URL
    agencyLink_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "agn_website"))
    )
    agencyLink_input.clear()
    agencyLink_input.send_keys(Keys.CONTROL + "a")
    agencyLink_input.send_keys(Keys.DELETE)
    agencyLink_input.send_keys(invalid_url)

    # Click Save
    save_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Save']")))
    save_button.click()
    print("Save button clicked.")

    # Check for error message
    try:
        error_elem = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//p[contains(text(), 'Please enter a valid website URL.')]")))
        try:
            assert error_elem.is_displayed(), "❌ Test Case 17 Failed: Error message not visible."
            print("✅ Test Case 17 Passed: Invalid website URL error appeared.")
        except AssertionError as ae:
            print(str(ae))
    except:
        print("❌ Test Case 17 Failed: Validity error message not found.")

# TEST CASE 18: Other Invalid Formats
def test_invalid_field_formats():
    print("\n/********* TEST CASE 18: Invalid Formats *********/")

    long_input = "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo"

    agency_name_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "agn_name")))
    agency_name_input.send_keys(Keys.CONTROL + "a")
    agency_name_input.send_keys(Keys.DELETE)
    agency_name_input.send_keys("New Name")

    # Input fields to test with invalid (too long) strings
    invalid_inputs = {
        "agn_code": long_input,
        "agn_head_mi": long_input,
        "agn_head_sfx": long_input
    }

    for field_id, input_value in invalid_inputs.items():
        input_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, field_id))
        )
        input_elem.send_keys(Keys.CONTROL + "a")
        input_elem.send_keys(Keys.DELETE)
        input_elem.send_keys(input_value)
        time.sleep(1)

    # Click Save
    save_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Save']"))
    )
    save_button.click()
    print("Save button clicked.")
    time.sleep(3)

    expected_errors = {
        "agn_code": "Agency Code / Alias should not exceed 8 characters.",
        "agn_head_mi": "Middle Initial should not exceed 5 character.",
        "agn_head_sfx": "Suffix should not exceed 10 characters."
    }

    all_passed = True
    for field_id, expected_text in expected_errors.items():
        try:
            field_elem = driver.find_element(By.ID, field_id)
            grandparent = field_elem.find_element(By.XPATH, "./ancestor::div[2]")
            error_elem = grandparent.find_element(By.CSS_SELECTOR, "p.text-error")

            assert error_elem.is_displayed(), f"❌ {field_id}: Error message not visible."
            assert expected_text in error_elem.text, f"❌ {field_id}: Incorrect error message. Expected to find: '{expected_text}'"

            print(f"✅ {field_id}: Correct error message displayed.")

        except AssertionError as ae:
            print(str(ae))
            all_passed = False
        except Exception as e:
            print(f"❌ {field_id}: Error message not found. Exception: {e}")
            all_passed = False

    if all_passed:
        print("\n✅ Test Case 18 Passed: All invalid format errors appeared as expected.")
    else:
        print("\n❌ Test Case 18 Failed: One or more error messages missing or incorrect.")

# TEST CASE 19: Valid Inputs with agency code 'ASTIDEMO'
def test_valid_entry_addition():
    print("\n/********* CREATE AGENCY/INSTITUTION: SUCCESSFUL TEST CASE *********/")
    print("\n/********* TEST CASE 19: Valid Entry Inputs *********/")
    
     # Clear relevant fields
    agencyName_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "agn_name")))
    alias_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "agn_code")))
    agencyLink_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "agn_website")))
    agencyHeadFirstName_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "agn_head_fname")))
    agencyHeadMI_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "agn_head_mi")))
    agencyHeadSurname_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "agn_head_lname")))
    agencyHeadSuffix_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "agn_head_sfx")))

    for input_elem in [agencyName_input, alias_input, agencyLink_input, agencyHeadFirstName_input, agencyHeadMI_input, agencyHeadSurname_input, agencyHeadSuffix_input]:
        time.sleep(1)
        input_elem.clear()
        input_elem.send_keys(Keys.CONTROL + "a")
        input_elem.send_keys(Keys.DELETE)

    # Fill input values
    input_data = {
        "agn_name": "Advanced Science and Technology Institute - Demo",
        "agn_code": "ASTIDEMO",
        "agn_group": "Regional Offices",
        "agn_website": "https://www.asti-demo.dost.gov.ph",
        "agn_head_fname": "FirstName",
        "agn_head_mi": "Z.",
        "agn_head_lname": "LastName",
        "agn_head_sfx": "III"
    }

    for field_id, value in input_data.items():
        input_elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, field_id)))
        input_elem.send_keys(value)
        time.sleep(2)

    print("✅ Inputted valid agency details.")

    # Submit
    save_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Save']")))
    save_button.click()
    print("Save button clicked.")

    # Wait for confirmation alert
    try:
        WebDriverWait(driver, 25).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//h2[@class='swal2-title' and contains(text(), 'added successfully')]")
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

    # Go back to Library page
    driver.get("http://10.10.99.23/library")

    # Wait for table to load
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//table//tbody/tr"))
    )

    # Validate row
    expected_values = {
        "alias": input_data["agn_code"],
        "agency_name": input_data["agn_name"],
        "agency_head": f"{input_data['agn_head_fname']} {input_data['agn_head_mi']} {input_data['agn_head_lname']} {input_data['agn_head_sfx']}".strip(),
        "website": input_data["agn_website"]
    }

    rows = driver.find_elements(By.XPATH, "//table//tbody/tr")
    target_row = next((row for row in rows if row.find_elements(By.TAG_NAME, "td")[0].text.strip() == expected_values["alias"]), None)

    if target_row:
        cells = target_row.find_elements(By.TAG_NAME, "td")
        actual_values = {
            "alias": cells[0].text.strip(),
            "agency_name": cells[1].text.strip(),
            "agency_head": cells[2].text.strip(),
            "website": cells[3].text.strip()
        }
        try:
            assert actual_values == expected_values, "❌ Test Case 19 Failed: Data mismatch in one or more columns."
            print("✅ Test Case 19 Passed: All values matched in the identified row.")

        except AssertionError as ae:
            print(str(ae))
    else:
        print("❌ Test Case 19 Failed: Could not find row with alias 'ASTIDEMO'")

# TEST CASE 20: Buttons
def test_cancel_button_redirect():
    print("\n/********* TEST CASE 20: Buttons *********/")

    try:
        # Wait and click 'Add New'
        add_new_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Add New']]"))
        )
        add_new_button.click()
        print("✅ Add New button clicked.")
    except Exception as e:
        print(f"❌ Failed to click 'Add New' button: {e}")
        return

    try:
        # Wait for Cancel button and click it
        cancel_button = driver.find_element(By.XPATH, "//button[normalize-space()='Cancel']")

        cancel_button.click()
        print("✅ Cancel button clicked.")
    except Exception as e:
        print(f"❌ Failed to click 'Cancel' button: {e}")
        return

    try:
        # Verify redirection back to Library
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//p[@class='mt-5 page-title' and text()='Library']"))
        )
        print("✅ Test Case 20 Passed: Redirected to Library page after Cancel.")
    except:
        print("❌ Test Case 20 Failed: 'Library' title not found after Cancel.")

# TEST CASE 21: Update Entry with agency code 'ASTIDEMO'
def update_recent_agency_entry():
    print("\n\n/********* TEST CASE 21: UPDATE Recent Agency Entry *********/")
    
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//table//tbody/tr")))
    time.sleep(5)
    rows = driver.find_elements(By.XPATH, "//table//tbody/tr")
    target_row = None
    
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if cells and cells[0].text.strip() == "ASTIDEMO":
            target_row = row
            break

    if target_row:
        target_row.click()
        print("✅ Target row clicked. Modal should appear.")
        
    time.sleep(5)  

    # Locate input fields
    agencyName_input            = driver.find_element(By.ID, "agn_name")
    alias_input                 = driver.find_element(By.ID, "agn_code")
    agencyLink_input            = driver.find_element(By.ID, "agn_website")
    agencyGroup_dropdown        = driver.find_element(By.ID, "agn_group")
    agencyHeadFirstName_input   = driver.find_element(By.ID, "agn_head_fname")
    agencyHeadMI_input          = driver.find_element(By.ID, "agn_head_mi")
    agencyHeadSurname_input     = driver.find_element(By.ID, "agn_head_lname")
    agencyHeadSuffix_input      = driver.find_element(By.ID, "agn_head_sfx")
    save_button                 = driver.find_element(By.XPATH, "//button[normalize-space()='Save']")

    # Clear and update input fields
    fields_to_update = [
        agencyName_input, alias_input, agencyLink_input,
        agencyHeadFirstName_input, agencyHeadMI_input,
        agencyHeadSurname_input, agencyHeadSuffix_input
    ]

    for input_elem in fields_to_update:
        time.sleep(1)
        input_elem.clear()
        input_elem.send_keys(Keys.CONTROL + "a")
        input_elem.send_keys(Keys.DELETE)

    # Fill in new test values
    time.sleep(1)
    agencyName_input.send_keys("Advanced Science and Technology Institute - Demo - Edited")
    time.sleep(1)
    alias_input.send_keys("ASTIDEMO")
    time.sleep(1)
    agencyGroup_dropdown.send_keys("Office of the Secretary")
    time.sleep(1)
    agencyLink_input.send_keys("https://websiteReTest.gov.ph/")
    time.sleep(1)
    agencyHeadFirstName_input.send_keys("T_FN_")
    time.sleep(1)
    agencyHeadMI_input.send_keys("T_MI")
    time.sleep(1)
    agencyHeadSurname_input.send_keys("TM_SN_")
    time.sleep(1)
    agencyHeadSuffix_input.send_keys("TM_SFX_")
    time.sleep(1)

    # Click save and confirm update
    save_button.click()
    print("✅ Save button clicked.")

    try:
        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//h2[text()='Agency / Institution updated successfully.']")
            )
        )
        print("✅ Update confirmation dialog appeared.")

        ok_button = driver.find_element(By.CSS_SELECTOR, "button.swal2-confirm")
        ok_button.click()
        print("✅ OK button clicked.")
    except:
        print("❌ Update confirmation message not found.")
        return

    # Reload table and verify update
    driver.get("http://10.10.99.23/library")
    time.sleep(5)

    target_row = None
    rows = driver.find_elements(By.XPATH, "//table//tbody/tr")
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if cells and cells[0].text.strip() == "ASTIDEMO":
            target_row = row
            break
    
    alias_val = cells[0].text.strip()
    agency_name_val = cells[1].text.strip()
    agency_head_val = cells[2].text.strip()
    website_val = cells[3].text.strip()
    
    expected_values = {
        "alias": "ASTIDEMO",
        "agency_name": "Advanced Science and Technology Institute - Demo - Edited",
        "agency_head": "T_FN_ T_MI. TM_SN_ TM_SFX_",
        "website": "https://websiteReTest.gov.ph/"
    }
    #
    try:
        assert (
            alias_val == expected_values["alias"] and
            agency_name_val == expected_values["agency_name"] and
            agency_head_val == expected_values["agency_head"] and
            website_val == expected_values["website"]
        ), "❌ Test Case 21 Failed: One or more values did not update correctly."

        print("✅ Test Case 21 Passed: Agency updated and reflected correctly in the table.")

    except AssertionError as ae:
        print(str(ae))
        if alias_val != expected_values["alias"]:
            print(f" - Alias mismatch: expected '{expected_values['alias']}', got '{alias_val}'")
        if agency_name_val != expected_values["agency_name"]:
            print(f" - Agency Name mismatch: expected '{expected_values['agency_name']}', got '{agency_name_val}'")
        if agency_head_val != expected_values["agency_head"]:
            print(f" - Agency Head mismatch: expected '{expected_values['agency_head']}', got '{agency_head_val}'")
        if website_val != expected_values["website"]:
            print(f" - Website mismatch: expected '{expected_values['website']}', got '{website_val}'")

# TEST CASE 22: Delete Entry with agency code 'ASTIDEMO'
def delete_recent_agency_entry():
    target_alias="ASTIDEMO"
    print("\n\n/********* TEST CASE 22: DELETE Recent Agency Entry *********/")
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
        if len(columns) >= 4:
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
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "agn_name")))
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