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

# Navigate to Funding Source tab
funding_tab = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//ul/li[2]/p[normalize-space()='Funding Source']")))
funding_tab.click()
print("✅ Test Case 0 PASSED: Funding Source tab clicked.")
time.sleep(5)

add_new_btn = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Add New']]")))
try:
    add_new_btn.click()
    print("✅ Add New button clicked.")
except (NoSuchElementException):
    print("Add New button not found or not clickable.")
time.sleep(15)

def main():
    time.sleep(10)
    test_funding_source_modal_elements(driver, wait)
    time.sleep(5)
    test_empty_funding_fields_validation(driver, wait)
    time.sleep(5)
    test_valid_funding_source_entry(driver, wait)
    time.sleep(5)
    test_cancel_button_closes_modal(driver, wait)
    time.sleep(5)
    test_update_funding_source_entry(driver, wait)
    time.sleep(5)
    test_delete_funding_source_by_code(driver, wait)
    time.sleep(5)
    print("/********* END OF THE TEST *********/")
    driver.quit()

def test_funding_source_modal_elements(driver, wait):
    print("\nTest Cases 1–4: Funding Source Modal and Labels")
    
    try:
        elements_to_check = [
            ("//p[contains(@class, 'modal-title') and contains(text(), 'Funding Source')]", "Funding Source modal appeared"),
            ("//p[contains(@class, 'modal-title') and normalize-space(text())='Funding Source']", "'Funding Source' label"),
            ("//span[@class='flex flex-row label-text' and normalize-space(text())='Funding Source Code']", "'Funding Source Code' label"),
            ("//span[@class='flex flex-row label-text' and normalize-space(text())='Funding Source Name']", "'Funding Source Name' label"),
        ]

        for index, (xpath, description) in enumerate(elements_to_check, start=1):
            try:
                element = wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
                assert element.is_displayed(), f"❌ Test Case {index} FAILED: {description} is not visible."
                print(f"✅ Test Case {index} PASSED: {description} is visible.")
            except AssertionError as ae:
                print(str(ae))
            except Exception as e:
                print(f"❌ Test Case {index} FAILED: {description} not found. Error: {str(e)}")
            time.sleep(0.5)


    except Exception as e:
        print(f"❌ Test Case 1-4 FAILED: Error during Funding Source modal tests: {str(e)}")

def test_empty_funding_fields_validation(driver, wait):
    print("\n/***************** TEST CASE 5: Empty entry fields *****************/")
    try:
        code_input = wait.until(EC.presence_of_element_located((By.ID, "fnd_code")))
        name_input = wait.until(EC.presence_of_element_located((By.ID, "fnd_name")))

        # Clear both fields
        code_input.clear()
        time.sleep(1)
        name_input.clear()
        time.sleep(1)

        save_button = driver.find_element(By.XPATH, "//button[normalize-space()='Save']")
        save_button.click()
        time.sleep(2)

        # Check for error messages
        error_fnd_code = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='fnd_code']/following-sibling::p[contains(text(), 'This field is required.')]")))
        error_fnd_name = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='fnd_name']/following-sibling::p[contains(text(), 'This field is required.')]")))

        try:
            assert error_fnd_code.is_displayed() and error_fnd_name.is_displayed(), "❌ Test Case 5 FAILED: One or both required field errors not displayed."
            print("✅ Test Case 5 PASSED: Required field validations displayed.")

        except AssertionError as ae:
            print(str(ae))

    except Exception as e:
        print(f"❌ Test Case 5 FAILED: Exception occurred during validation test — {str(e)}")

def test_valid_funding_source_entry(driver, wait):
    print("/n/**************FUNDING SOURCE (CREATE) *************/")
    print("\n/***************** TEST CASE 6: Valid entry inputs *****************/")
    try:
        time.sleep(2)

        driver.find_element(By.ID, "fnd_code").send_keys("TEST1")
        time.sleep(1)
        driver.find_element(By.ID, "fnd_name").send_keys("Test Funding Source")
        time.sleep(1)

        # Click Save
        save_button = driver.find_element(By.XPATH, "//button[normalize-space()='Save']")
        save_button.click()
        time.sleep(2)

        # Wait for success popup
        confirmation_popup = wait.until(EC.visibility_of_element_located((
            By.XPATH, "//h2[contains(text(), 'Funding Source added successfully.')]"
        )))
        print("✅ Confirmation popup appeared.")

        # Click OK on the popup
        ok_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.swal2-confirm")))
        ok_button.click()
        print("✅ Confirmation popup dismissed.")
        print("✅ Entry added successfully.")
        time.sleep(3)  

        # Look for the added row
        rows = driver.find_elements(By.XPATH, "//table//tbody/tr")
        target_row = None

        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if cells and cells[0].text.strip() == "TEST1":
                target_row = cells
                break
        try:
            assert target_row and target_row[1].text.strip() == "Test Funding Source", \
                "❌ Test Case 6 Failed: Entry not found or incorrect."
            print("✅ Test Case 6 Passed: Entry appears in table.")
        except AssertionError as ae:
            print(str(ae))

    except Exception as e:
        print(f"❌ Test Case 6 Failed: Exception occurred — {str(e)}")

# Test Case 7: Cancel Button
def test_cancel_button_closes_modal(driver, wait):
    print("\n/***************** TEST CASE 7: Cancel button closes the modal *****************/")
    try:
        time.sleep(2)
        add_new_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn-circular') and .//span[normalize-space()='Add New']]")))
        add_new_btn.click()
        wait.until(EC.visibility_of_element_located((By.ID, "fnd_code")))
        time.sleep(1)

        # Click the Cancel button
        cancel_btn = driver.find_element(By.XPATH, "//button[normalize-space()='Cancel']")
        cancel_btn.click()
        time.sleep(2)

        # Check if modal is closed
        modal_closed = not driver.find_elements(By.XPATH, "//p[contains(@class, 'modal-title') and contains(text(), 'Funding Source')]")
        
        try: 
            assert modal_closed, "❌ Test Case 7 Failed: Modal still visible."
            print("✅ Test Case 7 Passed: Cancel button closed the modal.")
        except AssertionError as ae:
            print(str(ae))
        
    except Exception as e:
        print(f"❌ Test Case 7 Failed: Exception occurred — {str(e)}")

# Test Case 8: UPDATE
print("/***************** FUNDING SOURCE (UPDATE) *****************/")
def test_update_funding_source_entry(driver, wait, original_code="TEST1", new_code="TEST1-EDITED", new_name="Test Funding Source-Edited"):
    print("\n/********* TEST CASE 8: UPDATING LAST FUNDING SOURCE ENTRY *********/")
    try:
        time.sleep(2)
        rows = driver.find_elements(By.XPATH, "//table//tbody/tr")
        target_row_element = None

        # Find row with original code
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if cells and cells[0].text.strip() == original_code:
                target_row_element = row
                break

        if not target_row_element:
            print(f"❌ Test Case 8 Failed: Row with code '{original_code}' not found.")
            return

        driver.execute_script("arguments[0].click();", target_row_element)
        print("✅ Row clicked.")
        time.sleep(2)

        # Update form inputs
        code_input = wait.until(EC.visibility_of_element_located((By.ID, "fnd_code")))
        name_input = driver.find_element(By.ID, "fnd_name")

        code_input.clear()
        code_input.send_keys(new_code)
        name_input.clear()
        name_input.send_keys(new_name)

        # Save changes
        save_button = driver.find_element(By.XPATH, "//button[normalize-space()='Save']")
        save_button.click()
        print("✅ Save button clicked.")
        time.sleep(5)

        # Confirmation
        wait.until(EC.visibility_of_element_located((
            By.XPATH, "//h2[contains(text(), 'updated successfully')]"
        )))
        ok_button = driver.find_element(By.CSS_SELECTOR, "button.swal2-confirm")
        ok_button.click()
        print("✅ Update confirmation popup dismissed.")
        time.sleep(10)

        funding_tab = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//ul/li[2]/p[normalize-space()='Funding Source']")))
        funding_tab.click()
        time.sleep(10)

        # Verify updated row exists in table
        updated = False
        rows = driver.find_elements(By.XPATH, "//table//tbody/tr")
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if cells and cells[0].text.strip() == new_code and cells[1].text.strip() == new_name:
                updated = True
                break
        try: 
            assert updated, f"❌ Test Case 8 Failed: Mismatch after update → Code: {new_code}, Name: {new_name} not found."
            print("✅ Test Case 8 Passed: Updated values reflected in table.")
        except AssertionError as ae:
            print(str(ae))
    
    except Exception as e:
        print(f"❌ Test Case 8 Failed: Exception occurred — {str(e)}")

# Test Case 9: DELETE
def test_delete_funding_source_by_code(driver, wait):
    print(f"\n/********* TEST CASE 9: DELETE FUNDING SOURCE ENTRY 'TEST1-EDITED' *********/")
    try:
        time.sleep(2)
        funding_tab = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//ul/li[2]/p[normalize-space()='Funding Source']")))
        funding_tab.click()
        time.sleep(5)

        # Find row with specified code
        rows = driver.find_elements(By.XPATH, "//table//tbody/tr")
        target_row = None
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if cols and cols[0].text.strip() == "TEST1-EDITED":
                target_row = row
                break

        if not target_row:
            print(f"❌ Test Case 9 Failed: Entry with code 'TEST1-EDITED' not found.")
            return

        name_to_delete = target_row.find_elements(By.TAG_NAME, "td")[1].text.strip()

        # Click the row
        target_row.click()
        print(f"✅ Clicked row with Code: 'TEST1-EDITED', Name: '{name_to_delete}'")
        wait.until(EC.visibility_of_element_located((By.ID, "fnd_code")))
        time.sleep(1)

        # Click Delete button
        delete_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Delete']")))
        delete_button.click()
        print("✅ Delete button clicked.")
        time.sleep(5)
        
        # Confirm delete popup
        wait.until(EC.visibility_of_element_located((
            By.XPATH, "//h2[normalize-space()='Are you sure you want to delete this item?']"
        )))
        confirm_button = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//button[text()='Delete' and contains(@class, 'swal2-confirm')]"
        )))
        confirm_button.click()
        print("✅ Confirm delete clicked.")
        time.sleep(5)
        
        # Wait for confirmation message
        wait.until(EC.visibility_of_element_located((
            By.XPATH, "//h2[normalize-space()='Funding Source deleted successfully.']"
        )))
        print("✅ Delete success popup appeared.")

        # Click OK on success popup
        ok_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.swal2-confirm")))
        ok_button.click()
        print("✅ Delete success popup dismissed.")

        # Final verification
        time.sleep(5)
        rows_after = driver.find_elements(By.XPATH, "//table//tbody/tr")
        deleted = all(
            cols[0].text.strip() != "TEST1-EDITED"
            for row in rows_after
            if (cols := row.find_elements(By.TAG_NAME, "td"))
        )

        try: 
            assert deleted, f"❌ Test Case 9 Failed: 'TEST1-EDITED' still exists in the table."
            print(f"✅ Test Case 9 Passed: 'TEST1-EDITED' entry successfully deleted.")
        except AssertionError as ae:
            print(str(ae))

    except Exception as e:
        print(f"❌ Test Case 9 Failed: Exception occurred — {str(e)}")

if __name__ == "__main__":
    main()