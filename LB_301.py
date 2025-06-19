from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

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
time.sleep(10)

funding_tab = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//ul/li[2]/p[normalize-space()='Funding Source']")))

funding_tab.click()
print("✅ Test Case 0 Passed: Funding Source tab clicked.")
time.sleep(5)

print("/********* FUNDING SOURCE (ADD) *********/")
add_new_btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Add New']]")))
try:
    add_new_btn.click()
    print("✅ Add New button clicked.")
except (NoSuchElementException):
    print("Add New button not found or not clickable.")
time.sleep(15)

modal_title = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//p[contains(@class, 'modal-title') and contains(text(), 'Funding Source')]")))
funding_label = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//p[contains(@class, 'modal-title') and normalize-space(text())='Funding Source']")))
fundingCode_label = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,"//span[@class='flex flex-row label-text' and normalize-space(text())='Funding Source Code']")))      
fundingName_label = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,"//span[@class='flex flex-row label-text' and normalize-space(text())='Funding Source Name']")))


def check_displayed(element, description, index):
    if element and element.is_displayed():
        print(f"✅ Test Case {index} Passed: {description} is visible.")
    else:
        print(f"❌ Test Case {index} Failed: {description} is not visible.")
    time.sleep(0.5)

test_cases = [
    (modal_title, "Funding Source modal appeared"),
    (funding_label, "'Funding Source' label"),
    (fundingCode_label, "'Funding Source Code' label"),
    (fundingName_label, "'Funding Source Name' label"),
]


for i, (element, description) in enumerate(test_cases, start=1):
    check_displayed(element, description, i)

print("/n/************** ADD FUNDING SOURCE *************/")
print("/***************** TEST CASE 5: Empty entry fields *****************/")
code_input = wait.until(EC.presence_of_element_located((By.ID, "fnd_code")))
code_input.clear()
time.sleep(5)

name_input = driver.find_element(By.ID, "fnd_name")
name_input.clear()
time.sleep(5)

save_button = driver.find_element(By.XPATH,"/html/body/div[2]/div[2]/div/div[2]/form/div[5]/button")
save_button.click()
time.sleep(5)

error_fnd_code = WebDriverWait(driver, 5).until(
    EC.visibility_of_element_located((By.XPATH, "//input[@id='fnd_code']/following-sibling::p[contains(text(), 'required')]"))
)
error_fnd_name = driver.find_element(
    By.XPATH, "//input[@id='fnd_name']/following-sibling::p[contains(text(), 'required')]"
)

if error_fnd_code.is_displayed() and error_fnd_name.is_displayed():
    print("✅ Test Case 5 Passed: Required field validations displayed.")
else:
    print("❌ Test Case 5 Failed: Required field error missing.")

print("/***************** TEST CASE 6: Valid entry inputs *****************/")
time.sleep(5)
driver.find_element(By.ID, "fnd_code").send_keys("TEST1")
time.sleep(1)
driver.find_element(By.ID, "fnd_name").send_keys("Test Funding Source")
time.sleep(1)
save_button.click()
time.sleep(10)

confirmation_popup = WebDriverWait(driver, 15).until(
    EC.visibility_of_element_located((By.XPATH, "//h2[contains(text(), 'Funding Source added successfully.')]"))
)
print("✅ Confirmation popup appeared.")

ok_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.swal2-confirm"))
)
ok_button.click()
print("✅ Confirmation popup dismissed.")
print("✅ Entry added successfully.")
time.sleep(15)

rows = driver.find_elements(By.XPATH, "//table//tbody/tr")
last_row = rows[-1]
columns = last_row.find_elements(By.TAG_NAME, "td")

if columns[0].text.strip() == "TEST1" and columns[1].text.strip() == "Test Funding Source":
    print("✅ Test Case 6 Passed: Entry appears in table.")
else:
    print("❌ Test Case 6 Failed: Entry not found or incorrect.")

# Test Case 7: Cancel Button
time.sleep(5)
add_new_btn.click()
WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "fnd_code")))
time.sleep(5)
cancel_btn = driver.find_element(By.XPATH, "//button[normalize-space()='Cancel']")
cancel_btn.click()

time.sleep(2)
modal_closed = not driver.find_elements(By.XPATH, "//p[contains(@class, 'modal-title') and contains(text(), 'Funding Source')]")

if modal_closed:
    print("✅ Test Case 7 Passed: Cancel button closed the modal.")
else:
    print("❌ Test Case 7 Failed: Modal still visible.")
time.sleep(5)
print("/***************** FUNDING SOURCE (UPDATE) *****************/")
print("\n/********* TEST CASE 1.8: UPDATING LAST FUNDING SOURCE ENTRY *********/")

# Test Case 8: UPDATE DETAILS
time.sleep(5)
rows = driver.find_elements(By.XPATH, "//table//tbody/tr")
last_row = rows[-1]
columns = last_row.find_elements(By.TAG_NAME, "td")
last_row.click()
print("✅ Last row clicked.")
time.sleep(10)

code_input = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "fnd_code"))
)
name_input = driver.find_element(By.ID, "fnd_name")

code_input.clear()
code_input.send_keys("XYZ")
name_input.clear()
name_input.send_keys("Example Source")

save_button = driver.find_element(By.XPATH,"/html/body/div[2]/div[2]/div/div[2]/form/div[5]/button")
save_button.click()
print("✅ Save button clicked.")
time.sleep(10)

WebDriverWait(driver, 15).until(
    EC.visibility_of_element_located((By.XPATH, "//h2[contains(text(), 'updated successfully')]"))
)
ok_button = driver.find_element(By.CSS_SELECTOR, "button.swal2-confirm")
ok_button.click()
print("✅ Update confirmation popup dismissed.")

time.sleep(5)

rows = driver.find_elements(By.XPATH, "//table//tbody/tr")
last_row = rows[-1]
columns = last_row.find_elements(By.TAG_NAME, "td")

code_val = columns[0].text.strip()
name_val = columns[1].text.strip()

if code_val == "XYZ" and name_val == "Example Source":
    print("✅ Test Case 8 Passed: Updated values reflected in table.")
else:
    print(f"❌ Test Case 8 Failed: Mismatch after update → Code: {code_val}, Name: {name_val}")


# Test Case 9: DELETING LAST ROW
print("\n/********* TEST CASE 9: DELETE LAST FUNDING SOURCE ENTRY *********/")
time.sleep(5)
rows = driver.find_elements(By.XPATH, "//table//tbody/tr")
last_row = rows[-1]
columns = last_row.find_elements(By.TAG_NAME, "td")

code_to_delete = columns[0].text.strip()
name_to_delete = columns[1].text.strip()

last_row.click()
print(f"Clicked row with Code: '{code_to_delete}', Name: '{name_to_delete}'")

WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "fnd_code")))
time.sleep(5)

delete_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((
        By.XPATH, "//button[normalize-space()='Delete']"
    ))
)
time.sleep(5)
delete_button.click()
print("✅ Delete button clicked.")

WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((
        By.XPATH, "//h2[normalize-space()='Are you sure you want to delete this item?']"
    ))
)
time.sleep(5)

confirm_delete = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((
        By.XPATH, "//button[text()='Delete' and contains(@class, 'swal2-confirm')]"
    ))
)
confirm_delete.click()
print("✅ Confirm delete clicked.")

time.sleep(5)

WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((
        By.XPATH, "//h2[normalize-space()='Funding Source deleted successfully.']"
    ))
)
print("✅ Delete success popup appeared.")
time.sleep(5)

ok_button = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.swal2-confirm"))
)
ok_button.click()
print("✅ Delete success popup dismissed.")

time.sleep(5)
rows_after = driver.find_elements(By.XPATH, "//table//tbody/tr")

deleted = True
for row in rows_after:
    cols = row.find_elements(By.TAG_NAME, "td")
    if cols and cols[0].text.strip() == code_to_delete:
        deleted = False
        break

if deleted:
    print(f"✅ Test Case 9 Passed: '{code_to_delete}' entry successfully deleted.")
else:
    print(f"❌ Test Case 9 Failed: '{code_to_delete}' still exists in the table.")

time.sleep(10)

print("/********* END OF THE TEST *********/")