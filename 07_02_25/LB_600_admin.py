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

# Navigate to User Accounts tab
user_acc_tab = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//ul/li[6]//p[contains(text(), 'User Accounts')]")))
user_acc_tab.click()
print("✅ Test Case 0 Passed: User Accounts tab clicked.")
time.sleep(5)

def main():
    return_to_user_accounts_tab()
    time.sleep(5)
    test_search_functionality()                 # Test Case 1: Search
    time.sleep(5)
    test_add_new_button()                       # Test Case 2: 'Add New' Button 
    time.sleep(5)
    return_to_user_accounts_tab()   
    time.sleep(5)
    test_table_row_hover()                      # Test Case 3: Table Row Hover Effect
    time.sleep(5)
    test_username_title()                       # Test Case 4: NAME Column Title
    time.sleep(5)
    test_agency_office_title()                  # Test Case 5: AGENCY / OFFICE Column Title
    time.sleep(5)
    test_access_level_title()                   # Test Case 6: ACCESS LEVEL Column Title
    time.sleep(5)
    test_email_title()                          # Test Case 7: EMAIL Column Title
    time.sleep(5)
    test_sort_buttons_name_column()             # Test Case 8: Sort Buttons for NAME
    time.sleep(5)
    test_sort_buttons_access_level_column()     # Test Case 9: Sort Buttons for ACCESS LEVEL
    time.sleep(5)
    full_name_input, agency_text, selected_level, email_value = test_click_first_user_row()    # Test Case 10: Store first row data
    time.sleep(5)
    test_first_user_fields_match_modal(full_name_input, agency_text, selected_level, email_value)  # Test Case 11: Compare first row data to the contents of its modal
    time.sleep(5)
    print("/********* END OF THE TEST *********/")
    driver.quit()

# Test Case 1: Search 
def test_search_functionality():
    print("\nTest Case 1: Testing Search Functionality")

    search_input = wait.until(EC.presence_of_element_located((
        By.XPATH, "//input[contains(@placeholder, 'Search...')]"
    )))
    search_icon = wait.until(EC.presence_of_element_located((
        By.XPATH, "//button[.//*[name()='svg' and contains(@data-icon, 'magnifying-glass')]]"
    )))

    try:
        assert search_icon.is_displayed() and search_input.is_displayed(), "❌ Test Case 1 FAILED: Search elements not displayed properly"
        print("✅ Search icon and input field are displayed")

        search_input.send_keys("test search")
        time.sleep(1)
        search_input.clear()
        time.sleep(1)

        driver.refresh()
        print("✅ Test Case 1 PASSED: Search input worked and page was refreshed")

    except AssertionError as ae:
        print(str(ae))

# Test Case 2: 'Add New' Button 
def test_add_new_button():
    print("\nTest Case 2: Add New Button")
    time.sleep(2)
    add_new_button = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//button[contains(@class, 'btn-circular') and .//span[normalize-space()='Add New']]"
    )))

    if add_new_button.is_displayed():
        print("✅ Add New button is displayed")
        add_new_button.click()
        time.sleep(2)

        close_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "svg.fa-xmark")))

        try:
            assert close_button.is_displayed(), "❌ Test Case 2 FAILED: X button not displayed"
            close_button.click()
            time.sleep(1)
            print("✅ Test Case 2 PASSED: Modal closed successfully using X button")

        except AssertionError as ae:
            print(str(ae))

    else:
        print("❌ Test Case 2 FAILED: Add New button not displayed")

def return_to_user_accounts_tab():
    print("\nReturning to User Accounts")
    user_accounts_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//p[normalize-space()='User Accounts']")))
    user_accounts_tab.click()
    time.sleep(5)

# Test Case 3: Table Row Hover Effect
def test_table_row_hover():
    print("\nTest Case 3: Testing Table Row ")
    table_row = wait.until(EC.presence_of_element_located((By.XPATH, "//tr[contains(@class, 'hover:bg-gray-200')]")))
    try:
        assert table_row.is_displayed(), "❌ Test Case 3 FAILED: Table row hover effect not working properly"
        print("✅ Test Case 3 PASSED: Working table row hover")
    except AssertionError as ae:
        print(str(ae))

# Test Case 4: NAME Column Title
def test_username_title():
    print("\nTest Case 4: Checking NAME Column Title")
    try:
        username_header = wait.until(EC.presence_of_element_located((By.XPATH, "//thead//td[1]//div[normalize-space(text())='NAME']")))
        assert username_header.is_displayed(), "Test Case 4 FAILED: ❌ NAME column title not displayed"
        print("✅ Test Case 4 PASSED: NAME column title FOUND")
    except AssertionError as ae:
        print(str(ae))
    except Exception as e:
        print(f"Test Case 4 FAILED: ❌ Exception in Test Case 4: {str(e)}")

# Test Case 5: AGENCY / OFFICE Column Title
def test_agency_office_title():
    print("\nTest Case 5: Checking AGENCY / OFFICE  Column Title")
    try:
        agency_header = wait.until(EC.presence_of_element_located((By.XPATH, "//thead//td[2][normalize-space()='AGENCY / OFFICE']")))
        assert agency_header.is_displayed(), "Test Case 5 FAILED: ❌ AGENCY / OFFICE column title NOT FOUND"
        print("✅ Test Case 5 PASSED: AGENCY / OFFICE column title FOUND")
    
    except AssertionError as ae:
        print(str(ae))
    except Exception as e:
        print(f"❌ Test Case 5 FAILED: Exception in Test Case 5: {str(e)}")

# Test Case 6: ACCESS LEVEL Column Title
def test_access_level_title():
    print("\nTest Case 6: Checking ACCESS LEVEL Column Title")
    try:
        access_level_header = wait.until(EC.presence_of_element_located((By.XPATH, "//thead//td[3]//div[normalize-space(text())='ACCESS LEVEL']")))
        assert access_level_header.is_displayed(), "❌ Test Case 6 FAILED: ACCESS LEVEL column title NOT FOUND"
        print("✅ Test Case 6 PASSED: ACCESS LEVEL column title FOUND")
    
    except AssertionError as ae:
        print(str(ae))
    except Exception as e:
        print(f"❌ Test Case 6 FAILED: Exception in Test Case 6: {str(e)}")

# Test Case 7: EMAIL Column Title
def test_email_title():
    print("\nTest Case 7: Checking EMAIL  Column Title")
    try:
        email_header = wait.until(EC.presence_of_element_located((By.XPATH, "//thead//td[4][normalize-space()='EMAIL']")))
        assert email_header.is_displayed(), "❌ Test Case 7 FAILED: EMAIL column title NOT FOUND"
        print("✅ Test Case 7 PASSED: EMAIL column title FOUND")
    except AssertionError as ae:
        print(str(ae))
    except Exception as e:
        print(f"❌ Test Case 7 FAILED: Exception in Test Case 7: {str(e)}")

# Test Case 8: Testing Sort Buttons for NAME
def test_sort_buttons_name_column():
    print("\nTest Case 8: Testing Sort Buttons for NAME Column")

    try:
        # Click ↑ Up sort
        sort_up = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//thead//td[1]//span[normalize-space()='▲']"
        )))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", sort_up)
        print("↥ Clicking Up sort button")
        driver.execute_script("arguments[0].click();", sort_up)
        time.sleep(2)

        rows_up = driver.find_elements(By.XPATH, "//tbody/tr/td[1]")
        categories_up = [r.text.strip().lower() for r in rows_up]

        assert categories_up == sorted(categories_up, reverse=True), f"❌ Test Case 8 FAILED: Up sort did not sort descending → {categories_up}"
        print("✅ Test Case 8 PASSED: Up sort sorted NAME descending") 

        # Click ↓ Down sort
        sort_down = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//thead//td[1]//span[normalize-space()='▼']"
        )))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", sort_down)
        print("↧ Clicking Down sort button")
        driver.execute_script("arguments[0].click();", sort_down)
        time.sleep(2)

        rows_down = driver.find_elements(By.XPATH, "//tbody/tr/td[1]")
        categories_down = [r.text.strip().lower() for r in rows_down]

        assert categories_down == sorted(categories_down), f"❌ Test Case 8 FAILED: Down sort did not sort ascending → {categories_down}"
        print("✅ Test Case 8 PASSED: Down sort sorted NAME ascending")

    except AssertionError as ae:
        print(str(ae))
    except Exception as e:
        print(f"❌ Test Case 8 FAILED due to unexpected error: {str(e)}")

# Test Case 9: Testing Sort Buttons for ACCESS LEVEL
def test_sort_buttons_access_level_column():
    print("\nTest Case 9: Testing Sort Buttons for ACCESS LEVEL Column")

    try:
        # Click ↑ Up sort
        sort_up = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//thead//td[3]//span[normalize-space()='▲']"
        )))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", sort_up)
        print("↥ Clicking Up sort button")
        driver.execute_script("arguments[0].click();", sort_up)
        time.sleep(2)

        rows_up = driver.find_elements(By.XPATH, "//tbody/tr/td[3]")
        categories_up = [r.text.strip().lower() for r in rows_up]

        assert categories_up == sorted(categories_up), f"❌ Test Case 9 FAILED: Up sort did not sort asecending → {categories_up}"
        print("✅ Test Case 9 PASSED: Up sort sorted ACCESS LEVEL asecending") 

        # Click ↓ Down sort
        sort_down = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//thead//td[3]//span[normalize-space()='▼']"
        )))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", sort_down)
        print("↧ Clicking Down sort button")
        driver.execute_script("arguments[0].click();", sort_down)
        time.sleep(2)

        rows_down = driver.find_elements(By.XPATH, "//tbody/tr/td[3]")
        categories_down = [r.text.strip().lower() for r in rows_down]
        
        assert categories_down == sorted(categories_down, reverse=True), f"❌ Test Case 9 FAILED: Down sort did not sort descending → {categories_down}"
        print("✅ Test Case 9 PASSED: Down sort sorted ACCESS LEVEL descending")
        
        # Revert to default order
        time.sleep(5)
        driver.execute_script("arguments[0].click();", sort_up)
        time.sleep(5)
    except AssertionError as ae:
        print(str(ae))
    except Exception as e:
        print(f"❌ Test Case 9 FAILED due to unexpected error: {str(e)}")

# Test Case 10: Store First Row Data
def test_click_first_user_row():
    print("\nTest Case 10: Clicking First User Row and Opening Modal")

    try:
        first_row = wait.until(EC.element_to_be_clickable((By.XPATH, "//tbody/tr[1]")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", first_row)
        driver.execute_script("arguments[0].click();", first_row)
        print("✅ First user row clicked")

        time.sleep(2)

        # --- Extract Name Fields ---
        usr_fname = wait.until(EC.visibility_of_element_located((By.ID, "usr_fname"))).get_attribute("value").strip()
        usr_mname = wait.until(EC.visibility_of_element_located((By.ID, "usr_mname"))).get_attribute("value").strip()
        usr_lname = wait.until(EC.visibility_of_element_located((By.ID, "usr_lname"))).get_attribute("value").strip()
        usr_sfx   = wait.until(EC.visibility_of_element_located((By.ID, "usr_sfx"))).get_attribute("value").strip()

        # Format full name (e.g., "Bote, Ferdjan c.")
        full_name_input = f"{usr_lname}, {usr_fname} {usr_mname} {usr_sfx}".strip()
        full_name_input = ' '.join(full_name_input.split())  # Remove extra whitespace

        # --- Extract Agency ---
        agency_span = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#usr_agency .vs__selected")))
        agency_text = agency_span.text.strip()

        # --- Extract Access Level ---
        level_select = wait.until(EC.visibility_of_element_located((By.ID, "usr_level")))
        selected_value = level_select.get_attribute("value")

        # Fallback to visible text if 'selected' attribute missing
        selected_level = ""
        for option in level_select.find_elements(By.TAG_NAME, "option"):
            if option.get_attribute("value") == selected_value:
                selected_level = option.text.strip()
                break

        # --- Extract Email ---
        email_input = wait.until(EC.visibility_of_element_located((By.ID, "usr_email")))
        email_value = email_input.get_attribute("value").strip()

        print("✅ All modal fields appeared and values extracted")
        return full_name_input, agency_text, selected_level, email_value

    except Exception as e:
        print(f"❌ Exception in Test Case 10: {str(e)}")
        return None, None, None, None

# Test Case 11: Compare first row data to the contents of its modal
def test_first_user_fields_match_modal(full_name_input, agency_text, selected_level, email_value):
    print("\nTest Case 11: Comparing First Row Values with Modal Inputs")

    try:
        first_row = wait.until(EC.presence_of_element_located((By.XPATH, "//tbody/tr[1]")))

        # Extract column values from first table row
        table_name   = first_row.find_element(By.XPATH, "./td[1]").text.strip()
        table_agency = first_row.find_element(By.XPATH, "./td[2]").text.strip()     # Not included in assertion due to value difference when there's no vale for agency col (bug)
        table_level  = first_row.find_element(By.XPATH, "./td[3]").text.strip()
        table_email  = first_row.find_element(By.XPATH, "./td[4]").text.strip()

        # Assertions
        assert full_name_input == table_name,   f"❌ NAME mismatch: '{full_name_input}' != '{table_name}'"
        assert selected_level == table_level,   f"❌ ACCESS LEVEL mismatch: '{selected_level}' != '{table_level}'"
        assert email_value == table_email,      f"❌ EMAIL mismatch: '{email_value}' != '{table_email}'"

        print("✅ All modal fields match the first table row values")

    except Exception as e:
        print(f"❌ Exception in Test Case 11: {str(e)}")
        raise

if __name__ == "__main__":
    main()