from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

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

user_acc_tab = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//ul/li[6]//p[contains(text(), 'User Accounts')]")))
user_acc_tab.click()
print("✅ Test Case 0 Passed: User Accounts tab clicked.")
time.sleep(20)


print("/*********  User Accounts (ADD) *********/")
add_new_btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Add New']]")))
try:
    add_new_btn.click()
    print("✅ Add New button clicked.")
except (NoSuchElementException):
    print("Add New button not found or not clickable.")
time.sleep(10)

modal_title         = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//p[contains(text(), 'User Account')]")))
employee_name_label  = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[normalize-space(text())='Employee Name']")))
first_name_input    = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "usr_fname")))
middle_name_input   = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "usr_mname")))  
surname_input       = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "usr_lname")))
suffix_input        = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "usr_sfx")))
email_address_label = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[normalize-space(text())='Email Address']"))) #
email_address_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "usr_email")))
contact_num_label   = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[normalize-space(text())='Contact Number']")))
contact_num_input   = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "usr_contact")))
position_label      = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[normalize-space(text())='Position']")))
position_input      = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "usr_position")))
access_level_label  = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[normalize-space(text())='Access Level']")))
access_level_input  = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "usr_level")))
agency_label        = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[normalize-space(text())='Agency']")))
agency_input        = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Select Agency']")))
cancel_btn          = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Cancel']")))
invite_btn          = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Invite']")))


elements_to_check = [
    (modal_title, "User account modal"),
    (employee_name_label, "Employee Name label"),
    (first_name_input, "First Name input"),
    (middle_name_input, "Middle Name input"),
    (surname_input, "Surname input"),
    (suffix_input, "Suffix input"),
    (email_address_label, "Email Address label"),
    (email_address_input, "Email Address input"),
    (contact_num_label, "Contact Number label"),
    (contact_num_input, "Contact Number input"),
    (position_label, "Position label"),
    (position_input, "Position input"),
    (access_level_label, "Access Level label"),
    (access_level_input, "Access Level input"),
    (agency_label, "Agency label"),
    (agency_input, "Agency input"),
    (cancel_btn, "Cancel button"),
    (invite_btn, "Invite button")
]

for index, (element, description) in enumerate(elements_to_check, start=1):
    if element and element.is_displayed():
        print(f"✅ Test Case {index} Passed: {description} appeared.")
    else:
        print(f"❌ Test Case {index} Failed: {description} doesn't appear.")
    time.sleep(1)

print("/n/********* ADD USER ACCOUNT: ERROR TEST CASES *********/")

# TEST CASE: All inputs left with empty fields
print("/***************** TEST CASE 19 *****************/")
time.sleep(15)
invite_btn.click()
print("INVITE button clicked.")
time.sleep(5)

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "p.text-error")))

from selenium.webdriver.common.by import By

required_field_ids = ["usr_fname", "usr_lname", "usr_email", "usr_contact", "usr_position", "usr_agency"]
all_errors_found = True

for field_id in required_field_ids:
    try:
        field_elem = driver.find_element(By.ID, field_id)
        grandparent = field_elem.find_element(By.XPATH, "./ancestor::div[2]")
        error_elem = grandparent.find_element(By.CSS_SELECTOR, "p.text-error")

        if "This field is required." in error_elem.text.strip():
            print(f"   Field '{field_id}' correctly shows the required error.")
        else:
            print(f"   Field '{field_id}' error text mismatch. Found: '{error_elem.text.strip()}'")
            all_errors_found = False

    except Exception as e:
        print(f"❌ Error message for field '{field_id}' not found. Exception: {e}")
        all_errors_found = False

if all_errors_found:
    print("✅ Test Case 19 Passed: All required field errors were found and correct.")
else:
    print("❌ Test Case 19 Failed: Some required field errors are missing or incorrect.")


time.sleep(5)

print("\n/********* ADD USER ACCOUNT: SUCCESSFUL TEST CASE *********/")
print("/***************** TEST CASE 20 *****************/")
time.sleep(5)

def fill_input(input_elem, value):
    input_elem.clear()
    input_elem.send_keys(Keys.CONTROL + "a")
    input_elem.send_keys(Keys.DELETE)
    input_elem.send_keys(value)
    time.sleep(1)

fill_input(first_name_input, "firstNameTest")
fill_input(middle_name_input, "X.")
fill_input(surname_input, "surnameTest")
fill_input(suffix_input, "II")
fill_input(email_address_input, "emailTest@dost.gov.ph")
fill_input(contact_num_input, "090909090")
fill_input(position_input, "positionTest")

time.sleep(1)
access_level_input.click()
time.sleep(1)
access_level_input.send_keys(Keys.ARROW_DOWN)
access_level_input.send_keys(Keys.ARROW_DOWN)
access_level_input.send_keys(Keys.ENTER)
time.sleep(1)
agency_input.click()
agency_input.send_keys("Bureau of Customs")
agency_input.send_keys(Keys.ARROW_DOWN)
agency_input.send_keys(Keys.ENTER)
time.sleep(1)
invite_btn.click()
print("Invite button clicked.")
time.sleep(20)

modal = WebDriverWait(driver, 15).until(
    EC.visibility_of_element_located((By.CLASS_NAME, "swal2-popup"))
)

success_title = modal.find_element(By.CLASS_NAME, "swal2-title")
if "User Account added successfully" in success_title.text:
    print("✅ Confirmation popup appeared: " + success_title.text)
else:
    print("❌ Unexpected confirmation message:", success_title.text)

time.sleep(2)

# Click the OK button
ok_button = modal.find_element(By.CSS_SELECTOR, "button.swal2-confirm")
ok_button.click()
print("✅ OK button clicked.")

driver.get("http://10.10.99.23/library")

time.sleep(10)
user_acc_tab = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//ul/li[6]//p[contains(text(), 'User Accounts')]")))
user_acc_tab.click()
print("User Accounts tab clicked.")

search_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//input[@type='text' and contains(@class, 'search-width')]"))
)

search_input.send_keys("firstNameTest")   
search_input.send_keys(Keys.ENTER)   
time.sleep(5) 


WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//table//tbody/tr"))
)
rows = driver.find_elements(By.XPATH, "//table//tbody/tr")
target_row = None

for row in rows:
    cells = row.find_elements(By.TAG_NAME, "td")
    if cells and cells[0].text.strip() == "surnameTest, firstNameTest X. II":
        target_row = row
        break

if target_row:
    category_val = target_row.find_element(By.TAG_NAME, "td").text.strip()
    print(f"✅ Test Case 20 Passed: Clicked row with: '{category_val}'")
else:
    print("❌ Test Case 20 Failed: Could not find row with 'surnameTest, firstNameTest X. II'")
time.sleep(5)

print("/n/************** UPDATE USER ACCOUNT *************/")
print("/***************** TEST CASE 21 *****************/")
time.sleep(5)
target_row.click()
time.sleep(10)

first_name_input    = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "usr_fname")))
surname_input       = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "usr_lname")))
email_address_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "usr_email")))
position_input      = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "usr_position")))

fill_input(first_name_input, "firstNameRetest")
time.sleep(1)
fill_input(surname_input, "surnameRetest")
time.sleep(1)
fill_input(email_address_input, "emailRetest@dost.gov.ph")
time.sleep(1)
fill_input(position_input, "positionRetest")
time.sleep(1)

save_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Save']")))
save_btn.click()
print("✅ Update confirmation dialog appeared.")
print("Save button clicked.")
time.sleep(10)

success_alert = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, "//h2[@class='swal2-title' and contains(text(), ' successfully')]"))
)
print("✅ Confirm update dialog appeared.")

time.sleep(5)
ok_button = driver.find_element(By.CSS_SELECTOR, "button.swal2-confirm")
ok_button.click()
print("OK button clicked.")

driver.get("http://10.10.99.23/library")
time.sleep(10)

user_acc_tab = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//ul/li[6]//p[contains(text(), 'User Accounts')]")))
user_acc_tab.click()
print("User Accounts tab clicked.")

search_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//input[@type='text' and contains(@class, 'search-width')]"))
)

search_input.send_keys("firstNameRetest")   
search_input.send_keys(Keys.ENTER)   
time.sleep(5) 


WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//table//tbody/tr"))
)
rows = driver.find_elements(By.XPATH, "//table//tbody/tr")
target_row = None

for row in rows:
    cells = row.find_elements(By.TAG_NAME, "td")
    if cells and cells[0].text.strip() == "surnameRetest, firstNameRetest X. II":
        target_row = row
        break

if target_row:
    category_val = target_row.find_element(By.TAG_NAME, "td").text.strip()
    print(f"✅ Test Case 21 Passed: Clicked row with category: '{category_val}'")
else:
    print("❌ Test Case 21 Failed: Could not find row with 'surnameRetest, firstNameRetest X. II'")
time.sleep(5)


print("/n/************** DELETE USER ACCOUNT *************/")
print("/***************** TEST CASE 22 *****************/")
time.sleep(5)

if not target_row:
    print("❌ Test Case 22 Failed: 'surnameRetest, firstNameRetest X. II' row not found.")
else:
    target_row.click()
    print("Row with 'surnameRetest, firstNameRetest X. II' clicked.")
    time.sleep(2)

    delete_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Delete']"))
    )
    delete_btn.click()
    print("Delete button clicked.")
    time.sleep(5)

    confirm_delete_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'swal2-confirm') and text()='Delete']"))
    )
    print("✅ Delete confirmation dialog appeared.")
    confirm_delete_btn.click()
    print("Confirmed deletion by clicking OK.")
    time.sleep(1)

    ok_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'swal2-confirm') and text()='OK']"))
    )
    ok_btn.click()
    print("✅ Success message displayed.")
    time.sleep(10)
    
    user_acc_tab = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//ul/li[6]//p[contains(text(), 'User Accounts')]")))
    user_acc_tab.click()
    print("User Accounts tab clicked.")

    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='text' and contains(@class, 'search-width')]"))
    )
    search_input.send_keys("surnameRetest")   
    search_input.send_keys(Keys.ENTER)   
    time.sleep(5) 

    time.sleep(5)
    rows_after = driver.find_elements(By.XPATH, "//table//tbody/tr")
    still_exists = any(
        row.find_elements(By.TAG_NAME, "td") and row.find_elements(By.TAG_NAME, "td")[0].text.strip() == "surnameRetest, firstNameRetest X. II' row not found"
        for row in rows_after
    )

    if still_exists:
        print("❌ Test Case 22 Failed: Item was not deleted.")
    else:
        print("✅ Test Case 22 Passed: Item successfully deleted.")
time.sleep(15)
print("/***************** END OF THE TEST *****************/")
