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


def main():
    test_ict_item_category_modal()
    time.sleep(5)
    test_empty_ict_category_field()
    time.sleep(5)
    test_valid_ict_category_entry()
    time.sleep(5)
    test_update_ict_category_entry()
    time.sleep(5)
    test_delete_ict_category_entry()
    time.sleep(5)
    print("/********* END OF THE TEST *********/")

    driver.quit()

def test_ict_item_category_modal():
    print("/********* TEST CASES 1–5: ICT Item Category (CREATE) *********/")
    try:
        modal_title = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//p[contains(@class, 'modal-title') and contains(text(), 'ICT Item Category')]")))
        ict_category_label = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//p[contains(@class, 'modal-title') and normalize-space(text())='ICT Item Category']")))
        input_field = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "cat_name")))
        cancel_btn = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//button[normalize-space()='Cancel']")))
        save_btn = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//button[normalize-space()='Save']")))

        def check_displayed(element, description, index):
            if element and element.is_displayed():
                print(f"✅ Test Case {index} Passed: {description} is visible.")
            else:
                print(f"❌ Test Case {index} Failed: {description} is not visible.")
            time.sleep(1)

        # Run checks
        test_cases = [
            (modal_title, "ICT Item Category modal"),
            (ict_category_label, "'ICT Item Category' label"),
            (input_field, "Input field 'cat_name'"),
            (cancel_btn, "Cancel button"),
            (save_btn, "Save button"),
        ]

        for i, (element, desc) in enumerate(test_cases, start=1):
            check_displayed(element, desc, i)

    except Exception as e:
        print(f"❌ Error during ICT Item Category checks: {str(e)}")

def test_empty_ict_category_field():
    print("\n/********* TEST CASE 6: Empty entry fields *********/")
    try:
        # Wait for input and save button to be present
        input_field = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "cat_name")))
        save_btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Save']")))

        input_field.clear()
        time.sleep(1)
        save_btn.click()
        time.sleep(2)

        error_msg = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,"//p[contains(@class, 'text-error') and normalize-space(text())='This field is required.']")))
        if error_msg and error_msg.is_displayed():
            print("✅ Test Case 6 Passed: Required field error message displayed.")
        else:
            print("❌ Test Case 6 Failed: Error message not displayed.")
    except Exception as e:
        print(f"❌ Exception in Test Case 6: {str(e)}")

    time.sleep(5)

def test_valid_ict_category_entry():
    print("\n/********* TEST CASE 7: Valid entry inputs *********/")
    try:
        input_field = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "cat_name")))
        save_btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Save']")))

        input_field.clear()
        input_field.send_keys("ICT_CATEGORY_TEST")
        time.sleep(1)

        save_btn.click()
        time.sleep(2)

        # Wait for success message
        success_msg = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH,
                "//h2[@id='swal2-title' and normalize-space()='ICT Item Category added successfully.']"))
        )
        print("✅ Confirmation popup appeared.")

        # Popup
        ok_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH,
                "//button[@class='swal2-confirm swal2-styled swal2-default-outline' and text()='OK']"))
        )
        ok_btn.click()
        print("✅ Entry added successfully")

        if success_msg.is_displayed():
            print("✅ Test Case 7 Passed: Valid entry accepted and success message displayed.")
        else:
            print("❌ Test Case 7 Failed: Success message not visible.")

    except Exception as e:
        print(f"❌ Exception in Test Case 7: {str(e)}")

    time.sleep(5)

print("/*********  ICT Item Category (UPDATE) *********/")

def test_update_ict_category_entry():
    old_value="ICT_CATEGORY_TEST"
    new_value="ICT_CATEGORY_RETEST"

    print("\n/********* TEST CASE 8: UPDATING ICT Categories *********/")
    try:
        time.sleep(5)
        rows = driver.find_elements(By.XPATH, "//table//tbody/tr")
        target_row = None

        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if cells and cells[0].text.strip() == old_value:
                target_row = row
                break

        if not target_row:
            print(f"❌ Test Case 8 Failed: Could not find row with '{old_value}'.")
            return

        category_val = target_row.find_element(By.TAG_NAME, "td").text.strip()
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target_row)
        driver.execute_script("arguments[0].click();", target_row)
        print(f"✅ Clicked row with category: '{category_val}'")
        time.sleep(3)

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "cat_name")))
        input_field = driver.find_element(By.ID, "cat_name")
        input_field.clear()
        input_field.send_keys(new_value)
        time.sleep(1)

        save_btn = driver.find_element(By.XPATH, "//button[normalize-space()='Save']")
        save_btn.click()
        print("✅ Save button clicked.")
        time.sleep(5)

        success_msg = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,"//h2[@id='swal2-title' and normalize-space()='ICT Item Category updated successfully.']")))
        print("✅ Update confirmation dialog appeared.")

        ok_btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,"//button[contains(@class, 'swal2-confirm') and text()='OK']")))
        ok_btn.click()
        print("✅ Confirm update dialog dismissed.")
        time.sleep(5)

        # Re-check table for updated value
        rows = driver.find_elements(By.XPATH, "//table//tbody/tr")
        update_found = any(
            row.find_element(By.TAG_NAME, "td").text.strip() == new_value
            for row in rows if row.find_elements(By.TAG_NAME, "td")
        )

        if update_found:
            print("✅ Test Case 8 Passed: Update reflected on the table.")
        else:
            print("❌ Test Case 8 Failed: Update not reflected on the table.")

    except Exception as e:
        print(f"❌ Test Case 8 Failed: Exception occurred - {str(e)}")

def test_delete_ict_category_entry():
    category_name="ICT_CATEGORY_RETEST"
    print(f"\n/********* TEST CASE 9: DELETE '{category_name}' *********/")
    try:
        time.sleep(3)
        rows = driver.find_elements(By.XPATH, "//table//tbody/tr")
        target_row = None

        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if cells and cells[0].text.strip() == category_name:
                target_row = row
                break

        if not target_row:
            print(f"❌ Test Case 9 Failed: Could not find row with '{category_name}'.")
            return

        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target_row)
        driver.execute_script("arguments[0].click();", target_row)
        print(f"✅ Clicked row with category: '{category_name}'")
        time.sleep(3)

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "cat_name")))
        time.sleep(2)

        delete_btn = driver.find_element(By.XPATH, "//button[normalize-space()='Delete']")
        delete_btn.click()
        print("✅ Delete button clicked.")
        time.sleep(3)

        confirm_delete_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH,
                "//button[contains(@class, 'swal2-confirm') and normalize-space(text())='Delete']"))
        )
        confirm_delete_btn.click()
        print("✅ Confirm delete clicked.")
        time.sleep(3)

        success_msg = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH,
                "//h2[@id='swal2-title' and normalize-space()='ICT Item Category deleted successfully.']"))
        )

        if success_msg.is_displayed():
            print("✅ Success message displayed for deletion.")
            ok_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH,
                    "//button[contains(@class, 'swal2-confirm') and text()='OK']"))
            )
            ok_btn.click()
            print("✅ Success popup dismissed.")
        else:
            print("❌ Test Case 9 Failed: Success message not displayed.")
            return

        time.sleep(3)
        # Re-verify deletion
        rows = driver.find_elements(By.XPATH, "//table//tbody/tr")
        deleted = all(
            row.find_element(By.TAG_NAME, "td").text.strip() != category_name
            for row in rows if row.find_elements(By.TAG_NAME, "td")
        )

        if deleted:
            print(f"✅ Test Case 9 Passed: '{category_name}' entry successfully deleted.")
        else:
            print(f"❌ Test Case 9 Failed: '{category_name}' still exists in the table.")

    except Exception as e:
        print(f"❌ Test Case 9 Failed: Exception occurred - {str(e)}")

if __name__ == "__main__":
    main()