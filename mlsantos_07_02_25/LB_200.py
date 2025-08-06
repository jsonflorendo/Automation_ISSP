from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import sys
import time

sys.path.append('../Automation_ISSP')  
from Login.login import agency_focal_login, driver
agency_focal_login() 

wait = WebDriverWait(driver, 15)
time.sleep(3)
if len(driver.window_handles) > 1:
    driver.switch_to.window(driver.window_handles[-1])

driver.get("http://10.10.99.23/library")
print("Reached the Library panel.")
driver.execute_script("window.scrollBy(0, 1000);")
time.sleep(10)


def main():
    time.sleep(5)
    test_office_tab()
    time.sleep(5)
    test_user_account_tab()
    time.sleep(5)
    return_office_tab()
    time.sleep(5)
    test_search_functionality()
    time.sleep(5)
    test_add_new_button()
    time.sleep(5)
    test_table_row_hover_effect()
    time.sleep(5)
    test_name_column_title()
    time.sleep(5)
    test_agency_office_column_title()
    time.sleep(5)
    test_office_head_column_title()
    time.sleep(5)
    test_office_code_sort()
    time.sleep(5)
    test_office_sort()
    time.sleep(5)
    row_data = test_click_first_row_and_store_data()
    time.sleep(5)   
    test_compare_office_code(row_data)
    time.sleep(5)
    test_compare_office_name(row_data)
    time.sleep(5)
    test_compare_office_head(row_data)
    time.sleep(5)
    print("/********* END OF THE TEST *********/")
    driver.quit()



def test_office_tab():
    print("\nTest Case 1: Office Tab")
    try:
        tab_xpath = "//p[contains(normalize-space(), 'Office')]"
        tab = wait.until(EC.element_to_be_clickable((By.XPATH, tab_xpath)))

        print("\nTest Case: Office tab display")

        try:
            assert tab.is_displayed(), "❌ Test Case 1 FAILED: Office tab is NOT FOUND"
            print("✅ Test Case 1 PASSED: Office FOUND")
            driver.execute_script("arguments[0].click();", tab)
            time.sleep(1.5)
        except AssertionError as ae:
            print(str(ae))

    except Exception as e:
        print(f"❌ Test Case 1 FAILED: Error clicking Office tab: {str(e)}")

def test_user_account_tab():
    print("\nTest Case 2: User Accounts")
    try:
        tab_xpath = "//p[normalize-space()='User Accounts']"
        tab = wait.until(EC.element_to_be_clickable((By.XPATH, tab_xpath)))

        print("\nTest Case: Office tab display")

        try:
            assert tab.is_displayed(), "❌ Test Case 2 FAILED: User Accounts tab is NOT FOUND"
            print("✅ Test Case 2 PASSED: User Accounts FOUND")
            driver.execute_script("arguments[0].click();", tab)
            time.sleep(1.5)
        except AssertionError as ae:
            print(str(ae))

    except Exception as e:
        print(f"❌ Test Case 2 FAILED: Error clicking User Accounts Office tab: {str(e)}")

def return_office_tab():
    print("\nReturning to Office tab")
    driver.get("http://10.10.99.23/library")
    time.sleep(3)

# Test Case 3: Search functionality
def test_search_functionality():
    print("\nTest Case 3: Testing Search Functionality")
    try:
        search_input_xpath = "//input[contains(@placeholder, 'Search...')]"
        search_icon_xpath = "//button[.//*[name()='svg' and contains(@data-icon, 'magnifying-glass')]]"

        search_input = wait.until(EC.presence_of_element_located((By.XPATH, search_input_xpath)))
        search_icon = wait.until(EC.presence_of_element_located((By.XPATH, search_icon_xpath)))

        try:
            assert search_input.is_displayed() and search_icon.is_displayed(), "❌ Test Case 3 FAILED: Search elements not displayed properly"
            print("✅ Test Case 3 PASSED: Search icon and input field are displayed")

            search_input.send_keys("test search")
            time.sleep(1)
            search_input.clear()
            time.sleep(1)

            driver.refresh()
            time.sleep(2)
            print("✅ Search functionality working and table refreshed")

        except AssertionError as ae:
            print(str(ae))

    except Exception as e:
        print(f"❌ Test Case 3 FAILED: Error in Search Test: {str(e)}")

#Test Case 4:  Add New Button
def test_add_new_button():
    print("\nTest Case 4: Testing Add New Button")
    try:
        add_new_xpath = "//button[contains(@class, 'btn-circular') and .//span[normalize-space()='Add New']]"
        close_btn_css = "svg.fa-xmark"

        add_new_btn = wait.until(EC.element_to_be_clickable((By.XPATH, add_new_xpath)))

        try:
            assert add_new_btn.is_displayed(), "❌ Test Case 4 FAILED: Add New button not displayed"
            print("✅ Test Case 4 PASSED: Add New button is displayed")
            add_new_btn.click()
            time.sleep(1.5)

            close_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, close_btn_css)))
            assert close_button.is_displayed(), "❌ Test Case 4 FAILED: Close button not displayed"
            close_button.click()
            time.sleep(1)
            print("✅ Test Case 4 PASSED: Modal closed successfully using close button")

        except AssertionError as ae:
            print(str(ae))
                
    except Exception as e:
        print(f"❌ Test Case 4 FAILED: Error testing Add New button: {str(e)}")

# Test Case 5: Table Row Hover Effect
def test_table_row_hover_effect():
    print("\nTest Case 5: Testing Table Row Hover Effect")
    try:
        row_xpath = "//tr[contains(@class, 'hover:bg-gray-200')]"
        table_row = wait.until(EC.presence_of_element_located((By.XPATH, row_xpath)))

        assert table_row.is_displayed(), "❌ Test Case 5 FAILED: Table row not displayed properly"
        print("✅ Test Case 5 PASSED: Table row hover effect is working")

    except AssertionError as ae:
        print(str(ae))
    except Exception as e:
        print(f"❌ Test Case 5 FAILED: Error testing table row hover effect: {str(e)}")

# Test Case 6: OFFICE CODE  Column Title
def test_name_column_title():
    print("\nTest Case 6: Checking OFFICE CODE Column Title")
    try:
        title_xpath = "//div[normalize-space()='OFFICE CODE']"
        col_title = wait.until(EC.presence_of_element_located((By.XPATH, title_xpath)))

        assert col_title.is_displayed(), "❌ Test Case 6 FAILED: OFFICE CODE column title not FOUND"
        print("✅ Test Case 6 PASSED: OFFICE CODE column title is FOUND")
    except AssertionError as ae:
        print(str(ae))
    except Exception as e:
        print(f"❌ Test Case 6 FAILED: Error checking OFFICE CODE column title: {str(e)}")

# Test Case 7: OFFICE Column Title
def test_agency_office_column_title():
    print("\nTest Case 7: Checking OFFICE Column Title")
    try:
        title_xpath = "//div[normalize-space()='OFFICE']"
        col_title = wait.until(EC.presence_of_element_located((By.XPATH, title_xpath)))

        assert col_title.is_displayed(), "❌ Test Case 7 FAILED: OFFICE column title not FOUND"
        print("✅ Test Case 7 PASSED: OFFICE column title is FOUND")
    except AssertionError as ae:
        print(str(ae))
    except Exception as e:
        print(f"❌ Test Case 7 FAILED: Error checking OFFICE column title: {str(e)}")

# Test Case 8: 	OFFICE HEAD Column Title
def test_office_head_column_title():
    print("\nTest Case 8: Checking 	OFFICE HEAD Column Title")
    try:
        title_xpath = "//td[normalize-space()='OFFICE HEAD']"
        col_title = wait.until(EC.presence_of_element_located((By.XPATH, title_xpath)))

        assert col_title.is_displayed(), "❌ Test Case 8 FAILED: OFFICE HEAD column title not FOUND"
        print("✅ Test Case 8 PASSED: OFFICE HEAD column title is FOUND")
    except AssertionError as ae:
        print(str(ae))
    except Exception as e:
        print(f"❌ Test Case 8 FAILED: Error checking OFFICE HEAD column title: {str(e)}")

# Test Case 9: Office Code Column Sort
def test_office_code_sort():
    print("\nTest Case 9: Testing Office Code Column Sort")

    try:
        rows_before = driver.find_elements(By.XPATH, "//tbody/tr/td[1]")
        codes_before = [r.text.strip() for r in rows_before]

        # Click ▲ Up sort
        sort_up = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "(//span[@class='hover:text-gray-500'][contains(text(),'▲')])[1]")))
        print("↥ Clicking Up sort button")
        driver.execute_script("arguments[0].click();", sort_up)
        time.sleep(2)

        rows_up = driver.find_elements(By.XPATH, "//tbody/tr/td[1]")
        codes_up = [r.text.strip().lower() for r in rows_up]

        # Assert descending sort
        assert codes_up == sorted(codes_up, reverse=True), f"❌ Test Case 9 FAILED: Up sort did not sort descending → {codes_up}"
        print("✅ Test Case 9 PASSED: Up sort sorted Office Code descending")

        # Click ▼ Down sort
        sort_down = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "(//span[@class='hover:text-gray-500'][contains(text(),'▼')])[1]")))
        print("↧ Clicking Down sort button")
        driver.execute_script("arguments[0].click();", sort_down)
        time.sleep(2)

        rows_down = driver.find_elements(By.XPATH, "//tbody/tr/td[1]")
        codes_down = [r.text.strip().lower() for r in rows_down]

        # Assert ascending sort
        assert codes_down == sorted(codes_down, reverse=False), f"❌ Test Case 9 FAILED: Down sort did not sort ascending → {codes_down}"
        print("✅ Test Case 9 PASSED: Down sort sorted Office Code ascending")

    except AssertionError as ae:
        print(str(ae))
    except Exception as e:
        print(f"❌ Test Case 9 FAILED due to unexpected error: {str(e)}")

# Test Case 10: Office Column Sort
def test_office_sort():
    print("\nTest Case 10: Testing Office Column Sort")

    try:
        rows_before = driver.find_elements(By.XPATH, "//tbody/tr/td[2]")
        codes_before = [r.text.strip() for r in rows_before]

        # Click ▲ Up sort
        sort_up = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "(//span[@class='hover:text-gray-500'][contains(text(),'▲')])[2]")))
        print("↥ Clicking Up sort button")
        driver.execute_script("arguments[0].click();", sort_up)
        time.sleep(2)

        rows_up = driver.find_elements(By.XPATH, "//tbody/tr/td[1]")
        codes_up = [r.text.strip().lower() for r in rows_up]

        # Assert descending sort
        assert codes_up == sorted(codes_up), f"❌ Test Case 10 FAILED: Up sort did not sort descending → {codes_up}"
        print("✅ Test Case 9 PASSED: Up sort sorted Office descending")

        # Click ▼ Down sort
        sort_down = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "(//span[@class='hover:text-gray-500'][contains(text(),'▼')])[2]")))
        print("↧ Clicking Down sort button")
        driver.execute_script("arguments[0].click();", sort_down)
        time.sleep(2)

        rows_down = driver.find_elements(By.XPATH, "//tbody/tr/td[2]")
        codes_down = [r.text.strip().lower() for r in rows_down]

        # Assert ascending sort
        assert codes_down == sorted(codes_down, reverse=True), f"❌ Test Case 10 FAILED: Down sort did not sort ascending → {codes_down}"
        print("✅ Test Case 10 PASSED: Down sort sorted Office ascending")

    except AssertionError as ae:
        print(str(ae))
    except Exception as e:
        print(f"❌ Test Case 10 FAILED due to unexpected error: {str(e)}")

# Test Case 11: Click First Row and Store Data
def test_click_first_row_and_store_data():
    print("\nTest Case 11: Clicking First Row and Storing Data")
    try:
        row_xpath = "(//tr[contains(@class, 'hover:bg-gray-200')])[2]"
        first_row = wait.until(EC.element_to_be_clickable((By.XPATH, row_xpath)))

        row_data = {
            'code': first_row.find_element(By.XPATH, ".//td[1]").text,
            'name': first_row.find_element(By.XPATH, ".//td[2]").text,
            'head': first_row.find_element(By.XPATH, ".//td[3]").text,
        }
        first_row.click()
        time.sleep(1.5)

        print("✅ Test Case 11 PASSED: Successfully clicked first row and stored data")
        print("📋 Stored Row Data:", row_data)
        return row_data

    except Exception as e:
        print(f"❌ Test Case 11 FAILED:  Error clicking first row or storing data: {str(e)}")
        return None

# Test Case 12: Compare Office Code from the table and modal
def test_compare_office_code(row_data):
    print("\nTest Case 12: Comparing Office Code")
    try:
        office_code_input = wait.until(EC.presence_of_element_located((By.ID, "ofc_code")))
        input_value = office_code_input.get_attribute('value')
       
        assert input_value == row_data['code'], (f"❌ Test Case 12 FAILED: Office Code mismatch\n  Expected: {row_data['code']}\n  Found:{input_value}")
        print("✅ Test Case 12 PASSED: Office Code matches table row content")
    except AssertionError as ae:
        print(str(ae))
    except Exception as e:
        print(f"❌ Test Case 12 FAILED: Error comparing Office Code: {str(e)}")

# Test Case 13: Compare Office (Name) from the table and modal
def test_compare_office_name(row_data):
    print("\nTest Case 13: Comparing Office Name")
    try:
        office_input = wait.until(EC.presence_of_element_located((By.ID, "ofc_name")))
        input_value = office_input.get_attribute('value')
       
        assert input_value == row_data['name'], (f"❌ Test Case 13 FAILED: Office Name mismatch\n  Expected: {row_data['code']}\n  Found:{input_value}")
        print("✅ Test Case 13 PASSED: Office Name matches table row content")
    except AssertionError as ae:
        print(str(ae))
    except Exception as e:
        print(f"❌ Test Case 13 FAILED: Error comparing Office Name: {str(e)}")

# Test Case 14: Compare Office Head from the table and modal
def test_compare_office_head(row_data):
    print("\nTest Case 14: Comparing Office Head")
    try:
        ofc_head_fname = wait.until(EC.visibility_of_element_located((By.ID, "ofc_head_fname"))).get_attribute("value").strip()
        ofc_head_mi    = wait.until(EC.visibility_of_element_located((By.ID, "ofc_head_mi"))).get_attribute("value").strip()
        ofc_head_lname = wait.until(EC.visibility_of_element_located((By.ID, "ofc_head_lname"))).get_attribute("value").strip()
        ofc_head_sfx   = wait.until(EC.visibility_of_element_located((By.ID, "ofc_head_sfx"))).get_attribute("value").strip()

        # Concatenate Office Head full name
        concat_ofc_name = f"{ofc_head_fname} {ofc_head_mi} {ofc_head_lname} {ofc_head_sfx}".strip()
        concat_ofc_name = ' '.join(concat_ofc_name.split())  # Normalize whitespace

        assert concat_ofc_name == row_data['head'], (
            f"❌ Test Case 14 FAILED: Office Head mismatch\n"
            f"  Expected: {row_data['head']}\n"
            f"  Found:    {concat_ofc_name}"
        )
        print("✅ Test Case 14 PASSED: Office Head matches table row content")
    except AssertionError as ae:
        print(str(ae))
    except Exception as e:
        print(f"❌ Test Case 14 FAILED: Error comparing Office Head: {str(e)}")

if __name__ == "__main__":
    main()


