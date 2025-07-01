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

ict_items_tab = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//ul/li[4]//label[contains(text(), 'ICT Items')]")))
ict_items_tab.click()
print("✅ Test Case 0 Passed: ICT Items tab clicked.")
time.sleep(10)

print("/*********  ICT Items (ADD) *********/")
add_new_btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Add New']]")))
try:
    add_new_btn.click()
    print("✅ Add New button clicked.")
except (NoSuchElementException):
    print("Add New button not found or not clickable.")
time.sleep(10)

modal_title                 = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//p[contains(text(), 'ICT Item')]")))
ict_category_label          = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[normalize-space(text())='Item Category']")))
item_category_dropdown      = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='itm_category']//div[@class='vs__dropdown-toggle']")))
allotment_class_label       = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[normalize-space(text())='Allotment Class']")))
allotment_class_desc        = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//p[normalize-space(text())='Classify the item into Allotment Class']")))
allotment_class_dropdown    = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//select[@id='rr_allot_class']")))
parent_item_label           = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[normalize-space(text())='Parent Item']")))
parent_item_dropdown        = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='itm_parent']//div[@class='vs__dropdown-toggle']")))
item_name_label             = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[normalize-space(text())='Item Name']")))
item_name_input             = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "itm_name")))
item_specs_label            = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//span[normalize-space(text())='Item Specifications']")))
item_specs_desc             = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "itm_desc")))
est_cost_label              = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//span[normalize-space(text())='Estimated Cost']")))
est_cost_input              = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "itm_cost")))
unit_measure_label          = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//span[normalize-space(text())='Unit of Measure']")))
unit_measure_dropdown       = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Select Unit']")))
close_button                = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "svg.fa-xmark")))
cancel_btn                  = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Cancel']")))
save_btn                    = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Save']")))


def check_displayed(element, test_case_num, description, positive_msg=None, negative_msg=None):
    if element and element.is_displayed():
        print(f"✅ Test Case {test_case_num} Passed: {positive_msg or description} is visible.")
    else:
        print(f"❌ Test Case {test_case_num} Failed: {negative_msg or description} is not visible.")
    time.sleep(1)  

test_cases = [
    (modal_title, 1, "ICT Item modal", "ICT Item modal appeared", "ICT Item modal didn't appear"),
    (ict_category_label, 2, "'Item Category' label"),
    (item_category_dropdown, 3, "ICT Item dropdown"),
    (ict_category_label, 4, "'Allotment Class' label"),
    (allotment_class_desc, 5, "'Allotment Class' description"),
    (allotment_class_dropdown, 6, "Allotment Class dropdown"),
    (parent_item_label, 7, "'Parent Item' label"),
    (parent_item_dropdown, 8, "Parent Item dropdown"),
    (item_name_label, 9, "'Item Name' label"),
    (item_name_input, 10, "'Item Name' input"),
    (item_specs_label, 11, "'Item Specifications' label"),  # assuming label repeated intentionally
    (item_specs_label, 12, "'Item Specifications' textarea"),
    (est_cost_label, 13, "'Estimated Cost' label"),
    (est_cost_input, 14, "'Estimated Cost' input"),
    (unit_measure_label, 15, "'Unit of Measure' label"),
    (unit_measure_dropdown, 16, "'Unit of Measure' dropdown"),
    (close_button, 17, "Close button", "Close button found", "Close button not found"),
    (cancel_btn, 18, "Cancel button"),
    (save_btn, 19, "Save button")
]

for element, num, desc, *messages in test_cases:
    check_displayed(element, num, desc, *messages)


print("/n/********* ADD ICT Items: ERROR TEST CASES *********/")

# TEST CASE: All inputs left with empty fields

print("/********* TEST CASE 20 *********/")
time.sleep(15)
save_btn.click()
print("Save button clicked.")
time.sleep(5)

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "p.text-error")))

# Define field selectors
required_fields = [
    ("itm_category", "div"),
    ("rr_allot_class", "select"),
    ("itm_name", "input"),
    ("itm_cost", "input"),
    ("vs3__combobox", "div"),
]

all_errors_found = True

for field_id, tag in required_fields:
    try:
        field_element = driver.find_element(By.ID, field_id)

        # Special case for 'itm_cost' which is wrapped in a div
        if field_id == "itm_cost":
            parent_div = field_element.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[2]/form/div[7]/div[1]")
            error_elem = parent_div.find_element(By.XPATH, ".//p[contains(@class, 'text-error')]")
        # Special case for 'vs3__combobox' (Unit of Measure) which is inside nested structure
        elif field_id == "vs3__combobox":
            container_div = field_element.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div[2]/form/div[7]/div[3]")
            error_elem = container_div.find_element(By.XPATH, ".//p[contains(@class, 'text-error')]")
        else:
            # General: Error Message is a following <p> sibling
            error_elem = field_element.find_element(By.XPATH, "following-sibling::p[contains(@class, 'text-error')]")

        if "This field is required." in error_elem.text:
            continue
        else:
            print(f"❌ Field '{field_id}' error text mismatch: '{error_elem.text}'")
            all_errors_found = False

    except Exception as e:
        print(f"❌ Error message for field '{field_id}' not found: {e}")
        all_errors_found = False
if all_errors_found:
    print("✅ Test Case 20: All error messages displayed correctly for empty fields.")
else:
    print("❌ Test Case 20 Failed: One or more error messages missing or incorrect.")


# TEST CASE 21: Duplicate ICT Items Registration
time.sleep(10)
print("/********* TEST CASE 21 *********/")
item_category_dropdown      = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='itm_category']//div[@class='vs__dropdown-toggle']")))
allotment_class_dropdown    = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//select[@id='rr_allot_class']")))
parent_item_dropdown        = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='itm_parent']//div[@class='vs__dropdown-toggle']")))
item_name_input             = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "itm_name")))
item_specs_desc             = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "itm_desc")))
est_cost_input              = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "itm_cost")))
unit_measure_dropdown       = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Select Unit']")))


# 1. ITEM CATEGORY (searchable vue-select dropdown)
item_category_dropdown.click()
search_input_category = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.XPATH, "//div[@id='itm_category']//input[@class='vs__search']"))
)
search_input_category.send_keys("ICT SUPPLIES AND MATERIALS")
time.sleep(1)
search_input_category.send_keys(Keys.ARROW_DOWN)
search_input_category.send_keys(Keys.ENTER)
time.sleep(5)


# 2. ALLOTMENT CLASS (native <select>)
allotment_class_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "rr_allot_class"))
)
allotment_class_dropdown = Select(allotment_class_element)
allotment_class_dropdown.select_by_visible_text("Maintenance and Other Operating Expenses")
time.sleep(5)

# 4. ITEM NAME (text input)
item_name_input.clear()
item_name_input.send_keys("All-in-one computer")
time.sleep(5)

# 5. ITEM DESCRIPTION (text input)
item_specs_desc.clear()
item_specs_desc.send_keys("High-end unit\nWith printer")
time.sleep(5)

# 6. ESTIMATED COST (text input — avoid comma formatting)
est_cost_input.clear()
est_cost_input.send_keys("100000.00")  
time.sleep(5)

# 2. ALLOTMENT CLASS AGAIN (Value changes for no reason?)
allotment_class_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "rr_allot_class"))
)
allotment_class_dropdown = Select(allotment_class_element)
allotment_class_dropdown.select_by_visible_text("Maintenance and Other Operating Expenses")
time.sleep(5)

# 7. UNIT MEASURE (searchable vue-select dropdown)
unit_measure_dropdown.click()
unit_measure_dropdown.send_keys("pc")
time.sleep(1)
unit_measure_dropdown.send_keys(Keys.ARROW_DOWN)
unit_measure_dropdown.send_keys(Keys.ENTER)

save_btn.click()
print("Save button clicked.")

time.sleep(10)

try:
    item_name_container = driver.find_element(By.XPATH, "//input[@id='itm_name']/parent::*")
    item_name_error = item_name_container.find_element(By.CSS_SELECTOR, "p.text-error")
    item_name_ok = (
        "already exists" in item_name_error.text.lower() 
        and item_name_error.is_displayed()
    )
except:
    item_name_ok = False

if item_name_ok:
    print("✅ Test Case 21 Passed: Duplicate Item Name error is shown.")
    item_name_input.clear()
    item_specs_desc.clear()
    est_cost_input.clear()

    select = Select(driver.find_element(By.ID, "rr_allot_class"))
    select.select_by_index(0)

    search_input_category.clear()

    parent_item_input = driver.find_element(By.XPATH, "//div[@id='itm_parent']//input[@class='vs__search']")
    parent_item_input.clear()
    unit_measure_input = driver.find_element(By.XPATH, "//input[contains(@class, 'vs__search') and @type='search']") 
    unit_measure_input.clear()

else:
    print("❌ Test Case 21 Failed: Item Name duplicate error not found or not visible.")
time.sleep(5)

time.sleep(5)
print("\n/********* ADD ICT Items: SUCCESSFUL TEST CASE *********/")
print("/********* TEST CASE 22 *********/")

# 1. ITEM CATEGORY (searchable vue-select dropdown)
item_category_dropdown.click()
search_input_category = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.XPATH, "//div[@id='itm_category']//input[@class='vs__search']"))
)
search_input_category.send_keys("ICT SUPPLIES AND MATERIALS")
time.sleep(1)
search_input_category.send_keys(Keys.ARROW_DOWN)
search_input_category.send_keys(Keys.ENTER)
time.sleep(5)


# 2. ALLOTMENT CLASS (native <select>)
allotment_class_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "rr_allot_class"))
)
allotment_class_dropdown = Select(allotment_class_element)
allotment_class_dropdown.select_by_visible_text("Maintenance and Other Operating Expenses")
time.sleep(5)

# 4. ITEM NAME (text input)
item_name_input.clear()
item_name_input.send_keys("ITEM_NAME_TEST")
time.sleep(5)

# 5. ITEM DESCRIPTION (text input)
item_specs_desc.clear()
item_specs_desc.send_keys("ITEM_DESCRIPTION_TEST")
time.sleep(5)

# 6. ESTIMATED COST (text input — avoid comma formatting)
est_cost_input.clear()
est_cost_input.send_keys("0.00")  
time.sleep(5)

# 2. ALLOTMENT CLASS AGAIN (Value changes for no reason?)
allotment_class_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "rr_allot_class"))
)
allotment_class_dropdown = Select(allotment_class_element)
allotment_class_dropdown.select_by_visible_text("Maintenance and Other Operating Expenses")
time.sleep(5)

# 7. UNIT MEASURE (searchable vue-select dropdown)
unit_measure_dropdown.click()
unit_measure_dropdown.send_keys("pc")
time.sleep(1)
unit_measure_dropdown.send_keys(Keys.ARROW_DOWN)
unit_measure_dropdown.send_keys(Keys.ENTER)
save_btn.click()
print("Save button clicked.")

time.sleep(10)

success_alert = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, "//h2[@class='swal2-title' and contains(text(), 'added successfully')]"))
)
print("✅ Confirmation popup appeared.")
time.sleep(5)
ok_button = driver.find_element(By.CSS_SELECTOR, "button.swal2-confirm")
ok_button.click()
print("✅ Entry added successfully")
print("OK button clicked.")
driver.get("http://10.10.99.23/library")
time.sleep(10)
ict_items_tab = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//ul/li[4]//label[contains(text(), 'ICT Items')]")))
ict_items_tab.click()
print("ICT Items tab clicked.")

# Wait for search bar to appear
search_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//input[@type='text' and contains(@class, 'search-width')]"))
)

# Clear and enter your search term
search_input.send_keys("ITEM_NAME_TEST")   
search_input.send_keys(Keys.ENTER)   
time.sleep(15) 

WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.XPATH, "//table//tbody/tr"))
)
rows = driver.find_elements(By.XPATH, "//table//tbody/tr")
target_row = None

for row in rows:
    cells = row.find_elements(By.TAG_NAME, "td")
    if cells and cells[0].text.strip() == "ITEM_NAME_TEST":
        target_row = row
        break

if target_row:
    category_val = target_row.find_element(By.TAG_NAME, "td").text.strip()
    print(f"✅ Test Case 22 Passed: Clicked row with category: '{category_val}'")
else:
    print("❌ Test Case 22 Failed: Could not find row with 'ITEM_NAME_TEST'")
time.sleep(5)


print("/*********  ICT Item (UPDATE) *********/")
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//table//tbody/tr"))
)
rows = driver.find_elements(By.XPATH, "//table//tbody/tr")
target_row = None

for row in rows:
    cells = row.find_elements(By.TAG_NAME, "td")
    if cells and cells[0].text.strip() == "ITEM_NAME_TEST":
        target_row = row
        break

print("\n/********* TEST CASE 23: UPDATING ITEM_NAME_TEST *********/")
time.sleep(15)
target_row.click()
time.sleep(10)

item_name_input             = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "itm_name")))
item_specs_desc             = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "itm_desc")))

# ITEM NAME (text input)
item_name_input.clear()
item_name_input.send_keys("ITEM_NAME_RETEST")
time.sleep(5)

# ITEM DESCRIPTION (text input)
item_specs_desc.clear()
item_specs_desc.send_keys("ITEM_DESCRIPTION_RETEST")
time.sleep(5)
save_btn                    = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Save']")))
save_btn.click()
print("Save button clicked.")

time.sleep(10)

success_alert = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, "//h2[@class='swal2-title' and contains(text(), ' successfully')]"))
)
print("✅ Update confirmation dialog appeared.")
time.sleep(5)
ok_button = driver.find_element(By.CSS_SELECTOR, "button.swal2-confirm")
ok_button.click()
print("✅ Confirm update dialog appeared.")
print("OK button clicked.")

driver.get("http://10.10.99.23/library")
time.sleep(10)

ict_items_tab = WebDriverWait(driver, 25).until(EC.element_to_be_clickable((By.XPATH, "//ul/li[4]//label[contains(text(), 'ICT Items')]")))
ict_items_tab.click()
print("ICT Items tab clicked.")
search_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//input[@type='text' and contains(@class, 'search-width')]"))
)
search_input.send_keys("ITEM_NAME_RETEST")   
search_input.send_keys(Keys.ENTER)   
time.sleep(5) 

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//table//tbody/tr"))
)
rows = driver.find_elements(By.XPATH, "//table//tbody/tr")
target_row = None

for row in rows:
    cells = row.find_elements(By.TAG_NAME, "td")
    if cells and cells[0].text.strip() == "ITEM_NAME_RETEST":
        target_row = row
        break

if target_row:
    category_val = target_row.find_element(By.TAG_NAME, "td").text.strip()
    print(f"✅ Test Case 23 Passed: Clicked row with category: '{category_val}'")
else:
    print("❌ Test Case 23 Failed: Could not find row with 'ITEM_NAME_TEST'")
time.sleep(5)


print("\n/********* TEST CASE 24: DELETING ITEM_NAME_RETEST *********/")
time.sleep(5)
# Step 1: Find the target row
rows = driver.find_elements(By.XPATH, "//table//tbody/tr")
target_row = None

for row in rows:
    cells = row.find_elements(By.TAG_NAME, "td")
    if cells and cells[0].text.strip() == "ITEM_NAME_RETEST":
        target_row = row
        break

if not target_row:
    print("❌ Test Case 9 Failed: 'ITEM_NAME_RETEST' row not found.")
else:
    target_row.click()
    print("Row with 'ITEM_NAME_RETEST' clicked.")
    time.sleep(2)

    # Step 2: Click Delete button in confirmation dialog
    delete_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Delete']"))
    )
    delete_btn.click()
    print("Delete button clicked.")
    time.sleep(5)
    # Step 3: Click OK in success dialog
    confirm_delete_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'swal2-confirm') and text()='Delete']"))
    )
    print("✅ Delete confirmation dialog appeared.")
    confirm_delete_btn.click()
    print("Confirmed deletion by clicking OK.")
    time.sleep(1)
    # Step 4: Wait for success message (modal with text: 'deleted successfully') 
    success_msg = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//h2[text()='ICT Item deleted successfully.']"))
    )

    print("✅ Success message displayed.")
    time.sleep(1)
    # Step 5: Click OK button on success modal (if still present)
    try:
        ok_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'swal2-confirm') and text()='OK']"))
        )
        ok_btn.click()
        print("Success modal OK button clicked.")
    except:
        print("Success modal OK button not found or already dismissed.")
    time.sleep(10)

    ict_items_tab = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//ul/li[4]//label[contains(text(), 'ICT Items')]")))
    ict_items_tab.click()

    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='text' and contains(@class, 'search-width')]"))
    )
    search_input.send_keys("ITEM_NAME_RETEST")   
    search_input.send_keys(Keys.ENTER)   
    time.sleep(5) 

    # Step 6: Re-check if item is deleted
    time.sleep(5)
    rows_after = driver.find_elements(By.XPATH, "//table//tbody/tr")
    still_exists = any(
        row.find_elements(By.TAG_NAME, "td") and row.find_elements(By.TAG_NAME, "td")[0].text.strip() == "ITEM_NAME_RETEST"
        for row in rows_after
    )

    if still_exists:
        print("❌ Test Case 24 Failed: Item was not deleted.")
    else:
        print("✅ Test Case 24 Passed: Item successfully deleted.")


print("/********* END OF THE TEST *********/")
time.sleep(15)