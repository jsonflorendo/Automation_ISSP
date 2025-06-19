from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

import sys
import time

sys.path.append('../Automation_ISSP')  
from Login.login import login, driver
login() 


wait = WebDriverWait(driver, 15)

time.sleep(3)
if len(driver.window_handles) > 1:
    driver.switch_to.window(driver.window_handles[-1])


driver.get("http://10.10.99.23/library")
print("Reached the Library panel.")
driver.execute_script("window.scrollBy(0, 1000);")
time.sleep(15)

add_new_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[2]/div[3]/main/div/div[3]/div/div/div[1]/div/button/div/span")))

try:
    add_new_button.click()
    print("Add New button clicked.")
except (NoSuchElementException):
    print("Add New button not found or not clickable.")

time.sleep(5)
agencyLogo_label            = driver.find_element(By.XPATH, "//span[contains(@class, 'label-text') and contains(text(), 'Agency Logo')]")
agencyLogo_modal            = driver.find_element(By.XPATH,"//div[contains(@class, 'drop-zone')]")
agency_modal                = driver.find_element(By.XPATH, "//div[contains(@class, 'rounded-pnl')]//p[contains(text(), 'Agency / Institution')]/ancestor::div[contains(@class, 'rounded-pnl')]//form")
agencyName_label            = driver.find_element(By.XPATH, "//span[contains(@class, 'label-text') and contains(text(), 'Agency Name')]")
agencyName_input            = driver.find_element(By.XPATH, "//input[@id='agn_name']")
alias_label                 = driver.find_element(By.XPATH, "//span[contains(text(), 'Alias') and .//i[contains(text(), '(short name)')]]")
alias_input                 = driver.find_element(By.XPATH, "//input[@id='agn_code']")
agencyGroup_label           = driver.find_element(By.XPATH, "//span[contains(text(), 'Agency Group')]")
agencyGroup_dropdown        = driver.find_element(By.XPATH, "//select[@id='agn_group']")
agencyLink_label            = driver.find_element(By.XPATH, "//span[contains(text(), 'Agency Official Website Link')]")
agencyLink_input            = driver.find_element(By.XPATH, "//input[@id='agn_website']")
agencyHeadName_label        = driver.find_element(By.XPATH, "//span[contains(text(), 'Name of Agency Head')]")
agencyHeadFirstName_input   = driver.find_element(By.XPATH, "//input[@id='agn_head_fname']")
agencyHeadMI_input          = driver.find_element(By.XPATH, "//input[@id='agn_head_mi']")
agencyHeadSurname_input     = driver.find_element(By.XPATH, "//input[@id='agn_head_lname']")
agencyHeadSuffix_input      = driver.find_element(By.XPATH, "//input[@id='agn_head_sfx']")
close_button                = driver.find_element(By.CSS_SELECTOR, "svg.fa-xmark")
cancel_button               = driver.find_element(By.CSS_SELECTOR, "button.bg-white.text-gray-700")
save_button                 = driver.find_element(By.CSS_SELECTOR, "button.bg-blue-900.no_spacing.text-white")

print("/********* Agency / Institution (ADD) *********/")

def check_element(element, description, index):
    if element:
        print(f"✅ Test Case {index}: {description} found successfully")
    else:
        print(f"❌ Test Case {index} Failed: {description} not found")
    time.sleep(1)

test_cases = [
    (agencyLogo_label and agencyLogo_modal, "Agency Logo and Upload Modal"),
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

time.sleep(5)
for i, (condition, description) in enumerate(test_cases):
    check_element(condition, description, i)

print("/n/********* ADD AGENCY: ERROR TEST CASES *********/")

# TEST CASE 14: All inputs left with empty fields
print("/********* TEST CASE 14: Empty Entry Fields *********/")
time.sleep(15)
save_button = driver.find_element(By.CSS_SELECTOR, "button.bg-blue-900.no_spacing.text-white")
save_button.click()
print("Save button clicked.")
time.sleep(5)

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "p.text-error")))

required_field_ids = ["agn_name", "agn_code", "agn_group", "agn_website", "agn_head_fname", "agn_head_lname"]
all_errors_found = True

for field_id in required_field_ids:
    try:
        field_elem = driver.find_element(By.XPATH, f"//*[@id='{field_id}']")
        grandparent = field_elem.find_element(By.XPATH, "./ancestor::div[2]")
        error_elem = grandparent.find_element(By.CSS_SELECTOR, "p.text-error")

        if "This field is required." in error_elem.text:
            continue
        else:
            print(f"❌ Field '{field_id}' error text mismatch.")
            all_errors_found = False
    except Exception as e:
        print(f"❌ Error message for field '{field_id}' not found.")
        all_errors_found = False

if all_errors_found:
    print("✅ Test Case 14: All error messages displayed correctly for empty fields.")
else:
    print("❌ Test Case 14 Failed: One or more error messages missing or incorrect.")

time.sleep(10)

# TEST CASE 15: Duplicate Agency Registration
print("/********* TEST CASE 15: Duplicate Entry *********/")
driver.find_element(By.ID, "agn_name").send_keys("Central Office")
time.sleep(1)
driver.find_element(By.ID, "agn_code").send_keys("CO")
time.sleep(1)
driver.find_element(By.ID, "agn_group").send_keys("Regional Offices")
time.sleep(1)
driver.find_element(By.ID, "agn_website").send_keys("https://www.dost.gov.ph/")
time.sleep(1)
driver.find_element(By.ID, "agn_head_fname").send_keys("Renato")
time.sleep(1)
driver.find_element(By.ID, "agn_head_mi").send_keys("U.")
time.sleep(1)
driver.find_element(By.ID, "agn_head_lname").send_keys("Solidum")
time.sleep(1)
driver.find_element(By.ID, "agn_head_sfx").send_keys("Jr.")
time.sleep(1)
save_button.click()
print("Save button clicked.")

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'Agency')]")))
time.sleep(10)

try:
    agency_name_container = driver.find_element(By.XPATH, "//input[@id='agn_name']/parent::*")
    agency_name_error = agency_name_container.find_element(By.CSS_SELECTOR, "p.text-error")
    agency_name_ok = "already exists" in agency_name_error.text and agency_name_error.is_displayed()
except:
    agency_name_ok = False
try:
    agency_site_container = driver.find_element(By.XPATH, "//input[@id='agn_website']/parent::*")
    agency_site_error = agency_site_container.find_element(By.CSS_SELECTOR, "p.text-error")
    agency_site_ok = "already exists" in agency_site_error.text and agency_site_error.is_displayed()
except:
    agency_site_ok = False

if agency_name_ok and agency_site_ok:
    print("✅ Test Case 15 Passed: Duplicate Agency Name and Website errors are shown.")
else:
    print("❌ Test Case 15 Failed:")
    if not agency_name_ok:
        print(" - Agency Name duplicate error not found or not visible.")
    if not agency_site_ok:
        print(" - Website duplicate error not found or not visible.")
time.sleep(5)

# TEST CASE 16:Invalid Website Link Format
print("/********* TEST CASE 16: Invalid Website Link *********/")
time.sleep(5)

agencyLink_input.clear()
agencyLink_input.send_keys(Keys.CONTROL + "a")  
agencyLink_input.send_keys(Keys.DELETE)
agencyLink_input.send_keys("Lorem ipsum dolor sit amet, consectetuer adipiscing")

save_button.click()
print("Save button clicked.")

try:
    error_elem = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//p[contains(text(), 'Please enter a valid website URL.')]")
        )
    )
    if error_elem.is_displayed():
        print("✅ Test Case 16 Passed: Invalid website URL error appeared.")
    else:
        print("❌ Test Case 16 Failed: Error message is not visible.")
except:
    print("❌ Test Case 16 Failed: Validity error message not found.")


# TEST CASE 1.16: Other Invalid Formats
print("/********* TEST CASE 17: Invalid Formats *********/")
time.sleep(5)

agencyName_input.clear()
agencyName_input.send_keys(Keys.CONTROL + "a")  
agencyName_input.send_keys(Keys.DELETE)
agencyName_input.send_keys("New Name")

long_input = "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo"
for input_elem in [alias_input, agencyHeadMI_input, agencyHeadSuffix_input]:
    time.sleep(5)
    input_elem.clear()
    input_elem.send_keys(Keys.CONTROL + "a")
    input_elem.send_keys(Keys.DELETE)
    input_elem.send_keys(long_input)

save_button.click()
print("Save button clicked.")
time.sleep(10)
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

        if expected_text in error_elem.text and error_elem.is_displayed():
            continue
        else:
            print(f"❌ {field_id}: Error message incorrect or not visible.")
            all_passed = False
    except:
        print(f"❌ {field_id}: Error message not found.")
        all_passed = False

if all_passed:
    print("\n✅ Test Case 17 Passed: All invalid format errors appeared as expected.")
else:
    print("\n❌ Test Case 17 Failed: One or more error messages missing or incorrect.")


time.sleep(5)
print("\n/********* ADD AGENCY: SUCCESSFUL TEST CASE *********/")
print("/********* TEST CASE 18: Valid Entry Inputs *********/")
for input_elem in [agencyName_input, alias_input, agencyLink_input, agencyHeadFirstName_input,  agencyHeadMI_input, agencyHeadSurname_input, agencyHeadSuffix_input]:
    time.sleep(1)
    input_elem.clear()
    input_elem.send_keys(Keys.CONTROL + "a")
    input_elem.send_keys(Keys.DELETE)

time.sleep(1)
agencyName_input.send_keys("Advanced Science and Technology Institute - Demo - EDITED")
time.sleep(1)
alias_input.send_keys("ASTIDEMO")
time.sleep(1)
agencyGroup_dropdown.send_keys("Regional Offices")
time.sleep(1)
agencyLink_input.send_keys("https://www.asti-demo.dost.gov.ph")
time.sleep(1)
agencyHeadFirstName_input.send_keys("FirstName")
time.sleep(1)
agencyHeadMI_input.send_keys("Z.")
time.sleep(1)
agencyHeadSurname_input.send_keys("LastName")
time.sleep(1)
agencyHeadSuffix_input.send_keys("III")
time.sleep(1)
print("Inputted details successfully.")
save_button.click()
print("Save button clicked.")
time.sleep(10)

success_alert = WebDriverWait(driver, 25).until(
    EC.visibility_of_element_located((By.XPATH, "//h2[@class='swal2-title' and contains(text(), 'added successfully')]"))
)
print("✅ Confirmation popup appeared.")
time.sleep(5)
ok_button = driver.find_element(By.CSS_SELECTOR, "button.swal2-confirm")
ok_button.click()
print("✅ Entry added successfully")
print("OK button clicked.")
driver.get("http://10.10.99.23/library")
time.sleep(15)

WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, "//table//tbody/tr"))
)


rows = driver.find_elements(By.XPATH, "//table//tbody/tr")
target_row = None

for row in rows:
    cells = row.find_elements(By.TAG_NAME, "td")
    if cells and cells[0].text.strip() == "ASTIDEMO": 
        target_row = row
        break

expected_values = {
    "alias": "ASTIDEMO",
    "agency_name": "Advanced Science and Technology Institute - Demo - EDITED",
    "agency_head": "FirstName Z. LastName III",
    "website": "https://www.asti-demo.dost.gov.ph"
}

if target_row:
    columns = target_row.find_elements(By.TAG_NAME, "td")
    alias_val = columns[0].text.strip()
    agency_name_val = columns[1].text.strip()
    agency_head_val = columns[2].text.strip()
    website_val = columns[3].text.strip()

    if (alias_val == expected_values["alias"] and
        agency_name_val == expected_values["agency_name"] and
        agency_head_val == expected_values["agency_head"] and
        website_val == expected_values["website"]):
        print("✅ Test Case 18 Passed: All values matched in the identified row.")
    else:
        print("❌ Test Case 18 Failed: Data mismatch in one or more columns.")
        print(f"Alias: expected '{expected_values['alias']}', got '{alias_val}'")
        print(f"Agency Name: expected '{expected_values['agency_name']}', got '{agency_name_val}'")
        print(f"Agency Head: expected '{expected_values['agency_head']}', got '{agency_head_val}'")
        print(f"Website: expected '{expected_values['website']}', got '{website_val}'")
else:
    print("❌ Test Case 18 Failed: Could not find row with alias 'ASTIDEMO'")


print("/********* TEST CASE 19: Buttons *********/")
time.sleep(5)
add_new_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Add New']]")))

try:
    add_new_button.click()
    print("Add New button clicked.")
except (NoSuchElementException):
    print("Add New button not found or not clickable.")

time.sleep(15)

cancel_button = driver.find_element(By.CSS_SELECTOR, "button.bg-white.text-gray-700")
cancel_button.click()
print("Cancel button clicked.")

driver.get("http://10.10.99.23/library")
time.sleep(10)
library_title_elements = driver.find_elements(By.XPATH, "//p[@class='mt-5 page-title' and text()='Library']")
if library_title_elements and library_title_elements[0].is_displayed():
    print("✅ Test Case 19 Passed: Redirected to Library page after Cancel.")
else:
    print("❌ Test Case 19 Failed: 'Library' title not found after Cancel.")



# / * UPDATING AGENCY INSTANCE */ 
time.sleep(10)
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, "//table//tbody/tr"))
)

# Find all rows in the table
rows = driver.find_elements(By.XPATH, "//table//tbody/tr")
target_row = None

# Look for the row with alias "ASTIDEMO"
for row in rows:
    cells = row.find_elements(By.TAG_NAME, "td")
    if cells and cells[0].text.strip() == "ASTIDEMO":
        target_row = row
        break
print("\n\n")
# If target row is found, print values and click
if target_row:
    columns = target_row.find_elements(By.TAG_NAME, "td")
    print(f" Original Alias:        {columns[0].text.strip()}")
    print(f" Original Agency Name:  {columns[1].text.strip()}")
    print(f" Original Agency Head:  {columns[2].text.strip()}")
    print(f" Original Website:      {columns[3].text.strip()}")

    time.sleep(10)
    target_row.click()
    time.sleep(10)
    print("✅ Target row clicked. Modal should appear.")
else:
    print("❌ Test Case 20 Failed: Row with alias 'ASTIDEMO' not found.")

# TEST CASE 2.12: Save button
time.sleep(1)
if save_button:
    print("✅ Test Case 20: Save button found successfully")
else:
    print("❌ Test Case 20 Failed: Save button not found")


# TEST CASE 20: UPDATE Recent Agency entry
print("\n\n/********* TEST CASE 21: UPDATE Recent Agency Entry *********/")
time.sleep(15)

agencyName_input            = driver.find_element(By.XPATH, "//input[@id='agn_name']")
alias_input                 = driver.find_element(By.XPATH, "//input[@id='agn_code']")
agencyLink_input            = driver.find_element(By.XPATH, "//input[@id='agn_website']")
agencyGroup_dropdown        = driver.find_element(By.XPATH, "//select[@id='agn_group']")
agencyHeadFirstName_input   = driver.find_element(By.XPATH, "//input[@id='agn_head_fname']")
agencyHeadMI_input          = driver.find_element(By.XPATH, "//input[@id='agn_head_mi']")
agencyHeadSurname_input     = driver.find_element(By.XPATH, "//input[@id='agn_head_lname']")
agencyHeadSuffix_input      = driver.find_element(By.XPATH, "//input[@id='agn_head_sfx']")
close_button                = driver.find_element(By.CSS_SELECTOR, "svg.fa-xmark")
delete_button               = driver.find_element(By.XPATH, "//button[normalize-space()='Delete']")
save_button                 = driver.find_element(By.XPATH, "//button[normalize-space()='Save']")

for input_elem in [
    agencyName_input, alias_input, agencyLink_input,
    agencyHeadFirstName_input, agencyHeadMI_input,
    agencyHeadSurname_input, agencyHeadSuffix_input]:
    time.sleep(1)
    input_elem.clear()
    input_elem.send_keys(Keys.CONTROL + "a")
    input_elem.send_keys(Keys.DELETE)

agencyName_input.send_keys("T_NAME_")
time.sleep(1)
alias_input.send_keys("T_ALIAS_")
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

# Click save button
save_button.click()
print("✅ Save button clicked.")

# Wait until the success message appears
WebDriverWait(driver, 15).until(
    EC.visibility_of_element_located((By.XPATH, "//h2[text()='Agency / Institution updated successfully.']"))
)
print("✅ Update confirmation dialog appeared.")

# Click OK button
ok_button = driver.find_element(By.CSS_SELECTOR, "button.swal2-confirm")
ok_button.click()
print("✅ OK button clicked.")

driver.get("http://10.10.99.23/library")

WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.XPATH, "//table//tbody/tr"))
)
rows = driver.find_elements(By.XPATH, "//table//tbody/tr")
last_row = rows[-1]
columns = last_row.find_elements(By.TAG_NAME, "td")

alias_val = columns[0].text.strip()
agency_name_val = columns[1].text.strip()
agency_head_val = columns[2].text.strip()
website_val = columns[3].text.strip()

expected_values = {
    "alias": "T_ALIAS_",
    "agency_name": "T_NAME_",
    "agency_head": "T_FN_ T_MI. TM_SN_ TM_SFX_",
    "website": "https://websiteReTest.gov.ph/"
}

print(f"   Alias:         {alias_val}")
print(f"   Agency Name:   {agency_name_val}")
print(f"   Agency Head:   {agency_head_val}")
print(f"   Website:       {website_val}")

# Validate
if (
    alias_val == expected_values["alias"] and
    agency_name_val == expected_values["agency_name"] and
    agency_head_val == expected_values["agency_head"] and
    website_val == expected_values["website"]
):
    print("✅ Test Case Passed 21: Agency updated and reflected in the table.")
else:
    print("❌ Test Case Failed 21: Updated values not reflected correctly in the table.")


# TEST CASE 22: DELETE Recent Agency entry
print("\n\n/********* TEST CASE 22: DELETE Recent Agency entry *********/")
time.sleep(10)
WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.XPATH, "//table//tbody/tr"))
)

time.sleep(3)

def find_row_by_alias(alias):
    rows = driver.find_elements(By.XPATH, "//table//tbody/tr")
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if cells and cells[0].text.strip() == alias:
            return row
    return None

target_alias = "T_ALIAS_"
target_row = find_row_by_alias(target_alias)

if target_row:
    columns = target_row.find_elements(By.TAG_NAME, "td")
    if len(columns) >= 4:
        alias_to_delete = columns[0].text.strip()
        print(f" Alias to delete: {alias_to_delete}")
    else:
        print("❌ Not enough columns found in the row")
        alias_to_delete = ""
else:
    print(f"❌ Could not find row with alias '{target_alias}'")
    alias_to_delete = ""


if target_row:
    time.sleep(1)
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(target_row)
    )

    click_successful = False
    if not click_successful:
        try:
            target_row.click()
            print("T_ALIAS_ row clicked successfully.")
            click_successful = True
        except:
            click_successful = False
else:
    print("❌ Could not get last row for clicking")
time.sleep(10)
modal_appeared = False
try:
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, "agn_name"))
    )
    modal_appeared = True
    print("Modal appeared successfully.")
    time.sleep(2)
except:
    modal_appeared = False
    print("❌ Modal did not appear")

delete_clicked = False
if modal_appeared:
    try:
        delete_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH, "//button[normalize-space()='Delete']"
            ))
        )

        if delete_button:
            time.sleep(1)

            delete_button.click()
            print("Delete button clicked. Waiting for confirmation prompt...")
            delete_clicked = True
        else:
            print("❌ Delete button not found")
    except:
        print("❌ Error finding or clicking delete button")
else:
    print("❌ Cannot click delete button - modal did not appear")
time.sleep(10)
confirmation_appeared = False
if delete_clicked:
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h2[text()='Are you sure you want to delete this item?']"))
        )
        confirmation_appeared = True
        print("✅ Delete confirmation dialog appeared.")
    except:
        confirmation_appeared = False
        print("❌ Delete confirmation dialog did not appear")
else:
    print("❌ Cannot wait for confirmation - delete button was not clicked")

delete_confirmed = False
if confirmation_appeared:
    try:
        confirm_delete_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'swal2-confirm') and text()='Delete']"))
        )

        if confirm_delete_btn:
            confirm_delete_btn.click()
            print("✅ Confirm delete clicked.")
            delete_confirmed = True
        else:
            print("❌ Confirm delete button not found")
    except:
        print("❌ Error confirming delete")
else:
    print("❌ Cannot confirm delete - confirmation dialog did not appear")
time.sleep(10)

alert_closed = False

ok_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.swal2-confirm"))
)

if ok_button:
    ok_button.click()
    print("Success alert closed.")
    alert_closed = True
    time.sleep(2)
else:
    print("❌ OK button not found")

time.sleep(10)
page_reloaded = False
driver.get("http://10.10.99.23/library")
try:
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//table//tbody"))
    )
    page_reloaded = True
    print("✅ Page reloaded successfully.")
    time.sleep(2)
except:
    page_reloaded = False
    print("❌ Error reloading page")

# Gather all remaining aliases in the table
remaining_aliases = []
if page_reloaded:
    rows = driver.find_elements(By.XPATH, "//table//tbody/tr")

    if len(rows) > 0:
        for row in rows:
            columns = row.find_elements(By.TAG_NAME, "td")
            if len(columns) > 0:
                alias = columns[0].text.strip()
                if alias:  # Only add non-empty aliases
                    remaining_aliases.append(alias)

        print(f" Remaining aliases: {remaining_aliases}")
    else:
        print(" No rows found in table after deletion.")
else:
    print("❌ Cannot gather aliases - page did not reload properly")

if len(alias_to_delete) > 0:
    if alias_to_delete not in remaining_aliases:
        print(f"✅ Test Case 22 Passed: '{alias_to_delete}' entry successfully deleted from the table.")
    else:
        print(f"❌ Test Case 22 Failed: '{alias_to_delete}' still found in the table.")
else:
    print("❌ Test Case 21 Failed: Could not capture alias_to_delete for verification.")

print("/********* END OF THE TEST *********/")
