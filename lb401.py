from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

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

ict_category_tab = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//ul/li[3]/p[normalize-space()='ICT Categories']")))
ict_category_tab.click()
print("✅ Test Case 0 Passed: ICT Categories tab clicked.")
time.sleep(10)

print("/*********  ICT Item Category (ADD) *********/")
add_new_btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Add New']]")))
try:
    time.sleep(10)
    add_new_btn.click()
    print("✅ Add New button clicked.")
except (NoSuchElementException):
    print("Add New button not found or not clickable.")
time.sleep(10)

modal_title         = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//p[contains(@class, 'modal-title') and contains(text(), 'ICT Item Category')]")))
ict_category_label  = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//p[contains(@class, 'modal-title') and normalize-space(text())='ICT Item Category']")))
input_field         = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "cat_name")))
cancel_btn          = driver.find_element(By.XPATH, "//button[normalize-space()='Cancel']")
save_btn            = driver.find_element(By.XPATH, "//button[normalize-space()='Save']")


def check_displayed(element, description, index):
    if element and element.is_displayed():
        print(f"✅ Test Case {index} Passed: {description} is visible.")
    else:
        print(f"❌ Test Case {index} Failed: {description} is not visible.")
    time.sleep(1)

test_cases = [
    (modal_title, "ICT Item Category modal"),
    (ict_category_label, "'ICT Item Category' label"),
    (input_field, "Input field 'cat_name'"),
    (cancel_btn, "Cancel button"),
    (save_btn, "Save button"),
]

for i, (element, desc) in enumerate(test_cases, start=1):
    check_displayed(element, desc, i)

print("\n/********* TEST CASE 6: Empty entry fields *********/")
input_field.clear()
time.sleep(1) 
save_btn.click()
time.sleep(10)
error_msg = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((
        By.XPATH,
        "//p[contains(@class, 'text-error') and normalize-space(text())='This field is required.']"
    ))
)
if error_msg and error_msg.is_displayed():
    print("✅ Test Case 6 Passed: Required field error message displayed.")
else:
    print("❌ Test Case 6 Failed: Error message not displayed.")
time.sleep(5)

# Test Case 7: Valid entry
print("\n/********* TEST CASE 7: Valid entry inputs *********/")
input_field.clear()
input_field.send_keys("ICT_CATEGORY_TEST")  

# Click save button
save_btn.click()
time.sleep(10)
# Check that no error message appears
success_msg = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((
        By.XPATH,
        "//h2[@id='swal2-title' and normalize-space()='ICT Item Category added successfully.']"
    ))
)
print("✅ Confirmation popup appeared.")
time.sleep(5)
ok_btn = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//button[@class='swal2-confirm swal2-styled swal2-default-outline' and text()='OK']"
        ))
    )
ok_btn.click()
print("✅ Entry added successfully")
if success_msg.is_displayed() and success_msg.text.strip() == "ICT Item Category added successfully.":
    print("✅ Test Case 7 Passed: Valid entry accepted and success message displayed.")
else:
    print("❌ Test Case 7 Failed: No success message after valid entry.")


print("/*********  ICT Item Category (UPDATE) *********/")
print("\n/********* TEST CASE 8: UPDATING ICT Categories *********/")
time.sleep(20)

rows = driver.find_elements(By.XPATH, "//table//tbody/tr")
target_row = None

for row in rows:
    cells = row.find_elements(By.TAG_NAME, "td")
    if cells and cells[0].text.strip() == "ICT_CATEGORY_TEST":
        target_row = row
        break

if not target_row:
    print("❌ Test Case 8 Failed: Could not find row with 'ICT_CATEGORY_TEST'.")
else:
    category_val = target_row.find_element(By.TAG_NAME, "td").text.strip()
    target_row.click()
    print(f"✅ Clicked row with category: '{category_val}'")
    time.sleep(10)
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "cat_name"))
    )

    input_field = driver.find_element(By.ID, "cat_name")
    input_field.clear()
    input_field.send_keys("ICT_CATEGORY_RETEST")
    time.sleep(1)  # short delay to allow typing animation if needed
    time.sleep(5)
    save_btn = driver.find_element(By.XPATH, "//button[normalize-space()='Save']")
    save_btn.click()
    time.sleep(10)
    try:
        success_msg = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//h2[@id='swal2-title' and normalize-space()='ICT Item Category updated successfully.']"
            ))
        )
        time.sleep(5)
        print("✅ Update confirmation dialog appeared.")
        ok_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//button[contains(@class, 'swal2-confirm') and text()='OK']"
                ))
            )
        print("✅ Confirm update dialog appeared.")
        ok_btn.click()
        time.sleep(5)

        rows = driver.find_elements(By.XPATH, "//table//tbody/tr")
        target_row = None

        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if cells and cells[0].text.strip() == "ICT_CATEGORY_RETEST":
                target_row = row
                break

        if not target_row:
            print("❌ Test Case 8 Failed: Update not reflected on the table.")
        else:
            print("✅ Test Case 8 Passed: Update reflected on the table.")

    except:
        print("❌ Test Case 8 Failed: Success message not displayed after update.")

# Test Case 9: DELETE 'ICT_CATEGORY_TEST'
print("\n/********* TEST CASE 9: DELETE 'ICT_CATEGORY_RETEST' *********/")
time.sleep(5)

rows = driver.find_elements(By.XPATH, "//table//tbody/tr")
target_row = None

# Find the row by exact text match
for row in rows:
    cells = row.find_elements(By.TAG_NAME, "td")
    if cells and cells[0].text.strip() == "ICT_CATEGORY_RETEST":
        target_row = row
        break

if not target_row:
    print("❌ Test Case 9 Failed: Could not find row with 'ICT_CATEGORY_RETEST'.")
else:
    category_val = target_row.find_element(By.TAG_NAME, "td").text.strip()
    target_row.click()
    print(f"✅ Clicked row with category: '{category_val}'")

    time.sleep(10)
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "cat_name"))
    )
    time.sleep(5)

    # Click the Delete button
    delete_btn = driver.find_element(By.XPATH, "//button[normalize-space()='Delete']")
    delete_btn.click()
    time.sleep(5)

    # Confirm the delete in modal
    confirm_delete_btn = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//button[contains(@class, 'swal2-confirm') and normalize-space(text())='Delete']"
        ))
    )
    print("✅ Delete confirmation dialog appeared.")
    confirm_delete_btn.click()
    time.sleep(5)   
    success_msg = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((
            By.XPATH,
            "//h2[@id='swal2-title' and normalize-space()='ICT Item Category deleted successfully.']"
        ))
    )
    time.sleep(2)

    if success_msg.is_displayed():
        print("✅ Success message displayed for deletion.")
    
        ok_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//button[contains(@class, 'swal2-confirm') and text()='OK']"
            ))
        )
        ok_btn.click()
        time.sleep(5)

        # Re-check table for deleted row
        rows = driver.find_elements(By.XPATH, "//table//tbody/tr")
        target_row = None
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if cells and cells[0].text.strip() == "ICT_CATEGORY_RETEST":
                target_row = row
                break

        if target_row:
            print("❌ Test Case 9 Failed: DELETE not reflected on the table.")
        else:
            print("✅ Test Case 9 Passed: DELETE reflected on the table.")
    else:
        print("❌ Test Case 9 Failed: Success message not displayed after deletion.")

time.sleep(5)

print("/********* END OF THE TEST *********/")