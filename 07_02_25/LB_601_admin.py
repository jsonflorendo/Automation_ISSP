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

# Navigate to User Accounts tab
user_acc_tab = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//ul/li[6]//p[contains(text(), 'User Accounts')]")))
user_acc_tab.click()
print("✅ Test Case 0 Passed: User Accounts tab clicked.")
time.sleep(20)

def main():
    time.sleep(5)
    test_user_accounts_add_modal(driver)  # Test 1-18
    time.sleep(5)
    test_required_field_errors(driver)    # Test 19
    time.sleep(5)
    test_add_user_account_success(driver)
    time.sleep(5)
    test_update_user_account(driver)
    time.sleep(5)
    test_delete_user_account(driver)
    time.sleep(5)
    print("/***************** END OF THE TEST *****************/")
    driver.quit()


def test_user_accounts_add_modal(driver):
    print("/*********  User Accounts (ADD) *********/")
    wait = WebDriverWait(driver, 20)

    try:
        add_new_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Add New']]")))
        add_new_btn.click()
        print("✅ Add New button clicked.")
    except NoSuchElementException:
        print("❌ Add New button not found or not clickable.")
        return

    time.sleep(10)

    try:
        elements_to_check = [
            (wait.until(EC.visibility_of_element_located((By.XPATH, "//p[contains(text(), 'User Account')]"))), "User account modal"),
            (wait.until(EC.visibility_of_element_located((By.XPATH, "//span[normalize-space(text())='Employee Name']"))), "Employee Name label"),
            (wait.until(EC.visibility_of_element_located((By.ID, "usr_fname"))), "First Name input"),
            (wait.until(EC.visibility_of_element_located((By.ID, "usr_mname"))), "Middle Name input"),
            (wait.until(EC.visibility_of_element_located((By.ID, "usr_lname"))), "Surname input"),
            (wait.until(EC.visibility_of_element_located((By.ID, "usr_sfx"))), "Suffix input"),
            (wait.until(EC.visibility_of_element_located((By.XPATH, "//span[normalize-space(text())='Email Address']"))), "Email Address label"),
            (wait.until(EC.visibility_of_element_located((By.ID, "usr_email"))), "Email Address input"),
            (wait.until(EC.visibility_of_element_located((By.XPATH, "//span[normalize-space(text())='Contact Number']"))), "Contact Number label"),
            (wait.until(EC.visibility_of_element_located((By.ID, "usr_contact"))), "Contact Number input"),
            (wait.until(EC.visibility_of_element_located((By.XPATH, "//span[normalize-space(text())='Position']"))), "Position label"),
            (wait.until(EC.visibility_of_element_located((By.ID, "usr_position"))), "Position input"),
            (wait.until(EC.visibility_of_element_located((By.XPATH, "//span[normalize-space(text())='Access Level']"))), "Access Level label"),
            (wait.until(EC.visibility_of_element_located((By.ID, "usr_level"))), "Access Level input"),
            (wait.until(EC.visibility_of_element_located((By.XPATH, "//span[normalize-space(text())='Agency']"))), "Agency label"),
            (wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Select Agency']"))), "Agency input"),
            (wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Cancel']"))), "Cancel button"),
            (wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Invite']"))), "Invite button")
        ]
    except Exception as e:
        print(f"❌ Exception while locating modal elements: {e}")
        return

    for index, (element, description) in enumerate(elements_to_check, start=1):
        if element and element.is_displayed():
            print(f"✅ Test Case {index} Passed: {description} appeared.")
        else:
            print(f"❌ Test Case {index} Failed: {description} doesn't appear.")
        time.sleep(1)

# # Test 19: All inputs left with empty fields
def test_required_field_errors(driver):
    print("/n/********* ADD USER ACCOUNT: ERROR TEST CASES *********/")
    print("/***************** TEST CASE 19 *****************/")
    wait = WebDriverWait(driver, 20)
    
    time.sleep(15)  

    try:
        # Click the Invite button
        invite_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Invite']")))
        invite_btn.click()
        print("✅ INVITE button clicked.")
    except Exception as e:
        print(f"❌ Failed to click Invite button: {e}")
        return

    time.sleep(5)

    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "p.text-error")))
    except Exception as e:
        print(f"❌ Error messages did not appear in time: {e}")
        return

    required_field_ids = ["usr_fname", "usr_lname", "usr_email", "usr_contact", "usr_position", "usr_agency"]
    all_errors_found = True

    for field_id in required_field_ids:
        try:
            field_elem = driver.find_element(By.ID, field_id)
            grandparent = field_elem.find_element(By.XPATH, "./ancestor::div[2]")
            error_elem = grandparent.find_element(By.CSS_SELECTOR, "p.text-error")

            error_text = error_elem.text.strip()
            if "This field is required." in error_text:
                print(f"   ✅ Field '{field_id}' correctly shows the required error.")
            else:
                print(f"   ❌ Field '{field_id}' error text mismatch. Found: '{error_text}'")
                all_errors_found = False

        except Exception as e:
            print(f"❌ Error message for field '{field_id}' not found. Exception: {e}")
            all_errors_found = False

    if all_errors_found:
        print("✅ Test Case 19 Passed: All required field errors were found and correct.")
    else:
        print("❌ Test Case 19 Failed: Some required field errors are missing or incorrect.")

# Test 20: SUCCESSFUL TEST CASE
def test_add_user_account_success(driver):
    print("\n/********* ADD USER ACCOUNT: SUCCESSFUL TEST CASE *********/")
    print("/***************** TEST CASE 20 *****************/")
    wait = WebDriverWait(driver, 20)
    time.sleep(5)

    def fill_input(by_locator, value):
        input_elem = wait.until(EC.visibility_of_element_located(by_locator))
        input_elem.clear()
        input_elem.send_keys(Keys.CONTROL + "a")
        input_elem.send_keys(Keys.DELETE)
        input_elem.send_keys(value)
        time.sleep(1)

    # Fill required fields
    fill_input((By.ID, "usr_fname"), "firstNameTest")
    fill_input((By.ID, "usr_mname"), "X.")
    fill_input((By.ID, "usr_lname"), "surnameTest")
    fill_input((By.ID, "usr_sfx"), "II")
    fill_input((By.ID, "usr_email"), "emailTest@dost.gov.ph")
    fill_input((By.ID, "usr_contact"), "090909090")
    fill_input((By.ID, "usr_position"), "positionTest")

    # Access Level
    access_level_input = wait.until(EC.visibility_of_element_located((By.ID, "usr_level")))
    access_level_input.click()
    time.sleep(1)
    access_level_input.send_keys(Keys.ARROW_DOWN)
    access_level_input.send_keys(Keys.ARROW_DOWN)
    access_level_input.send_keys(Keys.ENTER)

    # Agency
    agency_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Select Agency']")))
    agency_input.click()
    agency_input.send_keys("Bureau of Customs")
    agency_input.send_keys(Keys.ARROW_DOWN)
    agency_input.send_keys(Keys.ENTER)

    # Submit
    time.sleep(1)
    invite_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Invite']")))
    invite_btn.click()
    print("✅ Invite button clicked.")
    time.sleep(20)

    # Confirmation modal
    try:
        modal = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "swal2-popup")))
        success_title = modal.find_element(By.CLASS_NAME, "swal2-title")
        if "User Account added successfully" in success_title.text:
            print("✅ Confirmation popup appeared: " + success_title.text)
        else:
            print("❌ Unexpected confirmation message:", success_title.text)

        ok_button = modal.find_element(By.CSS_SELECTOR, "button.swal2-confirm")
        ok_button.click()
        print("✅ OK button clicked.")
    except Exception as e:
        print(f"❌ Error handling confirmation popup: {e}")
        return

    # Validate new entry exists in the table
    driver.get("http://10.10.99.23/library")
    time.sleep(10)

    try:
        user_acc_tab = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//ul/li[6]//p[contains(text(), 'User Accounts')]")
        ))
        user_acc_tab.click()
        print("✅ User Accounts tab clicked.")

        search_input = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//input[@type='text' and contains(@class, 'search-width')]")
        ))
        search_input.send_keys("firstNameTest")
        search_input.send_keys(Keys.ENTER)
        time.sleep(5)

        wait.until(EC.presence_of_element_located((By.XPATH, "//table//tbody/tr")))
        rows = driver.find_elements(By.XPATH, "//table//tbody/tr")
        target_row = None

        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if cells and cells[0].text.strip() == "surnameTest, firstNameTest X. II":
                target_row = row
                break

        if target_row:
            result = target_row.find_element(By.TAG_NAME, "td").text.strip()
            print(f"✅ Test Case 20 Passed: Found row with: '{result}'")
        else:
            print("❌ Test Case 20 Failed: Could not find row with 'surnameTest, firstNameTest X. II'")
    except Exception as e:
        print(f"❌ Error during table lookup: {e}")

    time.sleep(5)

# Test 21: UPDATE USER ACCOUNT
def test_update_user_account(driver):
    print("\n/************** UPDATE USER ACCOUNT *************/")
    print("/***************** TEST CASE 21 *****************/")
    wait = WebDriverWait(driver, 20)
    time.sleep(5)

    def fill_input(by_locator, value):
        input_elem = wait.until(EC.visibility_of_element_located(by_locator))
        input_elem.clear()
        input_elem.send_keys(Keys.CONTROL + "a")
        input_elem.send_keys(Keys.DELETE)
        input_elem.send_keys(value)
        time.sleep(1)

    # Click target row (assumes already searched previously)
    try:
        target_row = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//table//tbody/tr[td[contains(text(), 'firstNameTest')]]")
        ))
        target_row.click()
        print("✅ Target row clicked.")
    except Exception as e:
        print(f"❌ Failed to click target row: {e}")
        return

    time.sleep(10)

    # Fill updated values
    fill_input((By.ID, "usr_fname"), "firstNameRetest")
    fill_input((By.ID, "usr_lname"), "surnameRetest")
    fill_input((By.ID, "usr_email"), "emailRetest@dost.gov.ph")
    fill_input((By.ID, "usr_position"), "positionRetest")

    # Click Save
    try:
        save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Save']")))
        save_btn.click()
        print("✅ Save button clicked.")
    except Exception as e:
        print(f"❌ Save button error: {e}")
        return

    time.sleep(10)

    # Confirmation modal
    try:
        success_alert = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//h2[@class='swal2-title' and contains(text(), 'successfully')]"))
        )
        print("✅ Confirm update dialog appeared.")

        ok_button = driver.find_element(By.CSS_SELECTOR, "button.swal2-confirm")
        ok_button.click()
        print("✅ OK button clicked.")
    except Exception as e:
        print(f"❌ Confirmation modal failed: {e}")
        return

    # Reload and verify update
    driver.get("http://10.10.99.23/library")
    time.sleep(10)

    try:
        user_acc_tab = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//ul/li[6]//p[contains(text(), 'User Accounts')]")
        ))
        user_acc_tab.click()
        print("✅ User Accounts tab clicked.")

        search_input = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//input[@type='text' and contains(@class, 'search-width')]")
        ))
        search_input.send_keys("firstNameRetest")
        search_input.send_keys(Keys.ENTER)
        time.sleep(5)

        wait.until(EC.presence_of_element_located((By.XPATH, "//table//tbody/tr")))
        rows = driver.find_elements(By.XPATH, "//table//tbody/tr")
        updated_row = None

        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if cells and cells[0].text.strip() == "surnameRetest, firstNameRetest X. II":
                updated_row = row
                break

        if updated_row:
            result = updated_row.find_element(By.TAG_NAME, "td").text.strip()
            print(f"✅ Test Case 21 Passed: Found updated row: '{result}'")
        else:
            print("❌ Test Case 21 Failed: Could not find updated row with 'surnameRetest, firstNameRetest X. II'")

    except Exception as e:
        print(f"❌ Error during search verification: {e}")

    time.sleep(5)

# Test 22: DELETE USER ACCOUNT
def test_delete_user_account(driver):
    print("\n/************** DELETE USER ACCOUNT *************/")
    print("/***************** TEST CASE 22 *****************/")
    wait = WebDriverWait(driver, 20)
    time.sleep(5)

    # Search for the target row
    driver.get("http://10.10.99.23/library")
    time.sleep(10)

    try:
        user_acc_tab = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//ul/li[6]//p[contains(text(), 'User Accounts')]")
        ))
        user_acc_tab.click()
        print("✅ User Accounts tab clicked.")
    except Exception as e:
        print(f"❌ Failed to open User Accounts tab: {e}")
        return

    try:
        search_input = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//input[@type='text' and contains(@class, 'search-width')]")
        ))
        search_input.send_keys("firstNameRetest")
        search_input.send_keys(Keys.ENTER)
        time.sleep(5)

        rows = driver.find_elements(By.XPATH, "//table//tbody/tr")
        target_row = None

        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if cells and cells[0].text.strip() == "surnameRetest, firstNameRetest X. II":
                target_row = row
                break

    except Exception as e:
        print(f"❌ Error during row search: {e}")
        return

    if not target_row:
        print("❌ Test Case 22 Failed: 'surnameRetest, firstNameRetest X. II' row not found.")
        return

    try:
        target_row.click()
        print("✅ Row with 'surnameRetest, firstNameRetest X. II' clicked.")
        time.sleep(2)

        delete_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Delete']")))
        delete_btn.click()
        print("✅ Delete button clicked.")
        time.sleep(5)

        confirm_delete_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//button[contains(@class,'swal2-confirm') and text()='Delete']"
        )))
        print("✅ Delete confirmation dialog appeared.")
        confirm_delete_btn.click()
        print("✅ Confirmed deletion by clicking OK.")
        time.sleep(1)

        ok_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//button[contains(@class,'swal2-confirm') and text()='OK']"
        )))
        ok_btn.click()
        print("✅ Success message displayed.")
    except Exception as e:
        print(f"❌ Deletion process failed: {e}")
        return

    # Validate deletion
    time.sleep(10)
    try:
        user_acc_tab = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//ul/li[6]//p[contains(text(), 'User Accounts')]")
        ))
        user_acc_tab.click()
        print("✅ User Accounts tab reloaded.")
    except Exception as e:
        print(f"❌ Failed to reload User Accounts tab: {e}")
        return

    try:
        search_input = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//input[@type='text' and contains(@class, 'search-width')]")
        ))
        search_input.send_keys("surnameRetest")
        search_input.send_keys(Keys.ENTER)
        time.sleep(5)

        rows_after = driver.find_elements(By.XPATH, "//table//tbody/tr")
        still_exists = any(
            row.find_elements(By.TAG_NAME, "td") and
            row.find_elements(By.TAG_NAME, "td")[0].text.strip() == "surnameRetest, firstNameRetest X. II"
            for row in rows_after
        )

        if still_exists:
            print("❌ Test Case 22 Failed: Item was not deleted.")
        else:
            print("✅ Test Case 22 Passed: Item successfully deleted.")
    except Exception as e:
        print(f"❌ Error during final validation: {e}")

    time.sleep(5)

if __name__ == "__main__":
    main()
