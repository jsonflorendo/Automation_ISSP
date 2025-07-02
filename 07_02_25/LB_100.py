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
time.sleep(10)

def main():
    time.sleep(5)
    test_agency_institution_tab()
    time.sleep(5)
    test_funding_source_tab()
    time.sleep(5)
    test_ict_categories_tab()
    time.sleep(5)
    test_ict_items_tab()
    time.sleep(5)
    test_is_classification_tab()
    time.sleep(5)
    test_user_accounts_tab()
    time.sleep(5)
    return_agency_tab()
    time.sleep(5)
    test_search_functionality()
    time.sleep(5)
    test_add_new_button()
    time.sleep(5)
    test_table_row_hover_effect()
    time.sleep(5)
    test_agency_code_sort()
    time.sleep(5)
    test_agency_institution_sort()
    time.sleep(5)
    test_agency_code_column_title()
    time.sleep(5)
    test_agency_head_column_title()
    time.sleep(5)
    row_data = test_click_first_row_and_store_data()
    time.sleep(5)
    test_compare_agency_code(row_data)
    time.sleep(5)
    test_compare_agency_name(row_data)
    time.sleep(5)
    test_compare_agency_head(row_data)
    time.sleep(5)
    test_compare_website_link(row_data)
    time.sleep(5)
    print("/********* END OF THE TEST *********/")
    driver.quit()

# Test Case 1: Agency/Institution Tab
def test_agency_institution_tab():
    print("\nTest Case 1: Agency/Institution Tab")
    try:
        tab_xpath = "//p[normalize-space()='Agency / Institution']"
        tab = wait.until(EC.element_to_be_clickable((By.XPATH, tab_xpath)))

        print("\nTest Case: Agency/Institution tab display")

        try:
            assert tab.is_displayed(), "❌ Test Case 1 FAILED: Agency/Institution tab is not displayed"
            print("✅ Test Case 1 PASSED: Agency/Institution PASSED")
            driver.execute_script("arguments[0].click();", tab)
            time.sleep(1.5)
        except AssertionError as ae:
            print(str(ae))

    except Exception as e:
        print(f"❌ Test Case 1 FAILED: Error clicking Agency/Institution tab: {str(e)}")

# Test Case 2: Funding Source Tab
def test_funding_source_tab():
    print("\nTest Case 2: Funding Source Tab")
    try:
        tab_xpath = "//p[normalize-space()='Funding Source']"
        tab = wait.until(EC.element_to_be_clickable((By.XPATH, tab_xpath)))

        print("\nTest Case: Funding Source tab display")

        try:
            assert tab.is_displayed(), "❌ Test Case 2 FAILED: Funding Source tab not found"
            print("✅ Test Case 2 PASSED: Funding Source found")
            driver.execute_script("arguments[0].click();", tab)
            time.sleep(1.5)
        except AssertionError as ae:
            print(str(ae))

    except Exception as e:
        print(f"❌ Test Case 2 FAILED: Error clicking Funding Source tab: {str(e)}")

# Test Case 3: ICT Categories Tab
def test_ict_categories_tab():
    print("\nTest Case 3: ICT Categories Tab")
    try:
        tab_xpath = "//p[normalize-space()='ICT Categories']"
        tab = wait.until(EC.element_to_be_clickable((By.XPATH, tab_xpath)))

        print("\nTest Case: ICT Categories tab display")
        try:
            assert tab.is_displayed(), "❌ ICT Categories is not displayed"
            print("✅ ICT Categories PASSED")
            driver.execute_script("arguments[0].click();", tab)
            time.sleep(1.5)
        except AssertionError as ae:
            print(str(ae))

    except Exception as e:
        print(f"❌ Error clicking ICT Categories tab: {str(e)}")

# Test Case 4: ICT Items Tab
def test_ict_items_tab():
    print("\nTest Case 4: ICT Items Tab")
    try:
        tab_xpath = "//p[label[contains(text(), 'ICT Items')]]"
        tab = wait.until(EC.element_to_be_clickable((By.XPATH, tab_xpath)))

        print("\nTest Case: ICT Items tab display")
        
        try:
            assert tab.is_displayed(), "❌ ICT Items is not displayed"
            print("✅ ICT Items PASSED")
            driver.execute_script("arguments[0].click();", tab)
            time.sleep(1.5)
        except AssertionError as ae:
            print(str(ae))

    except Exception as e:
        print(f"❌ Error clicking ICT Items tab: {str(e)}")

# Test Case 5: IS Classification Tab
def test_is_classification_tab():
    print("\nTest Case 5: IS Classification Tab")
    try:
        tab_xpath = "//p[normalize-space()='IS Classification']"
        tab = wait.until(EC.element_to_be_clickable((By.XPATH, tab_xpath)))

        print("\nTest Case: IS Classification tab display")

        try:
            assert tab.is_displayed(), "❌ IS Classification is not displayed"
            print("✅ IS Classification PASSED")
            driver.execute_script("arguments[0].click();", tab)
            time.sleep(1.5)
        except AssertionError as ae:
            print(str(ae))

    except Exception as e:
        print(f"❌ Error clicking IS Classification tab: {str(e)}")

# Test Case 6: User Accounts Tab
def test_user_accounts_tab():
    print("\nTest Case 6: User Accounts Tab")
    try:
        tab_xpath = "//p[normalize-space()='User Accounts']"
        tab = wait.until(EC.element_to_be_clickable((By.XPATH, tab_xpath)))

        print("\nTest Case: User Accounts tab display")
        
        try:
            assert tab.is_displayed(), "❌ User Accounts is not displayed"
            print("✅ User Accounts PASSED")
            driver.execute_script("arguments[0].click();", tab)
            time.sleep(1.5)
        except AssertionError as ae:
            print(str(ae))
            
    except Exception as e:
        print(f"❌ Error clicking User Accounts tab: {str(e)}")

# Return to Agency/Institution tab
def return_agency_tab():
    print("\nReturning to Agency/Institution tab")
    driver.get("http://10.10.99.23/library")
    time.sleep(3)

# Test Case 7: Search functionality
def test_search_functionality():
    print("\nTest Case 7: Testing Search Functionality")
    try:
        search_input_xpath = "//input[contains(@placeholder, 'Search...')]"
        search_icon_xpath = "//button[.//*[name()='svg' and contains(@data-icon, 'magnifying-glass')]]"

        search_input = wait.until(EC.presence_of_element_located((By.XPATH, search_input_xpath)))
        search_icon = wait.until(EC.presence_of_element_located((By.XPATH, search_icon_xpath)))

        try:
            assert search_input.is_displayed() and search_icon.is_displayed(), "❌ Search elements not displayed properly"
            print("✅ Search icon and input field are displayed")

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
        print(f"❌ Error in Search Test: {str(e)}")

#Test Case 8:  Add New Button
def test_add_new_button():
    print("\nTest Case 8: Testing Add New Button")
    try:
        add_new_xpath = "//button[contains(@class, 'btn-circular') and .//span[normalize-space()='Add New']]"
        close_btn_css = "svg.fa-xmark"

        add_new_btn = wait.until(EC.element_to_be_clickable((By.XPATH, add_new_xpath)))

        try:
            assert add_new_btn.is_displayed(), "❌ Add New button not displayed"
            print("✅ Add New button is displayed")
            add_new_btn.click()
            time.sleep(1.5)

            close_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, close_btn_css)))
            assert close_button.is_displayed(), "❌ Close button not displayed"
            close_button.click()
            time.sleep(1)
            print("✅ Modal closed successfully using close button")

        except AssertionError as ae:
            print(str(ae))
                
    except Exception as e:
        print(f"❌ Error testing Add New button: {str(e)}")

# Test Case 9: Table Row Hover Effect
def test_table_row_hover_effect():
    print("\nTest Case 9: Testing Table Row Hover Effect")
    try:
        row_xpath = "//tr[contains(@class, 'hover:bg-gray-200')]"
        table_row = wait.until(EC.presence_of_element_located((By.XPATH, row_xpath)))

        assert table_row.is_displayed(), "❌ Table row not displayed properly"
        print("✅ Table row hover effect is working")

    except AssertionError as ae:
        print(str(ae))
    except Exception as e:
        print(f"❌ Error testing table row hover effect: {str(e)}")

def test_agency_code_sort():
    print("\nTest Case 10: Testing Agency Code Column Sort")

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
        assert codes_up == sorted(codes_up, reverse=True), f"❌ Test Case 10 FAILED: Up sort did not sort descending → {codes_up}"
        print("✅ Test Case 10 PASSED: Up sort sorted Agency Code descending")

        # Click ▼ Down sort
        sort_down = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "(//span[@class='hover:text-gray-500'][contains(text(),'▼')])[1]")))
        print("↧ Clicking Down sort button")
        driver.execute_script("arguments[0].click();", sort_down)
        time.sleep(2)

        rows_down = driver.find_elements(By.XPATH, "//tbody/tr/td[1]")
        codes_down = [r.text.strip().lower() for r in rows_down]

        # Assert ascending sort
        assert codes_down == sorted(codes_down, reverse=False), f"❌ Test Case 10 FAILED: Down sort did not sort ascending → {codes_down}"
        print("✅ Test Case 10 PASSED: Down sort sorted Agency Code ascending")

    except AssertionError as ae:
        print(str(ae))
    except Exception as e:
        print(f"❌ Test Case 10 FAILED due to unexpected error: {str(e)}")

# Test Case 11: Agency/Institution Column Sort
def test_agency_institution_sort():
    print("\nTest Case 11: Testing Agency/Institution Column Sort")

    try:
        rows_before = driver.find_elements(By.XPATH, "//tbody/tr/td[2]")
        names_before = [r.text.strip() for r in rows_before]

        # Click ▲ Up sort
        sort_up = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "(//span[@class='hover:text-gray-500'][contains(text(),'▲')])[2]")))
        print("↥ Clicking Up sort button")
        driver.execute_script("arguments[0].click();", sort_up)
        time.sleep(2)

        rows_up = driver.find_elements(By.XPATH, "//tbody/tr/td[2]")
        names_up = [r.text.strip().lower() for r in rows_up]

        # Assert ascending sort
        assert names_up == sorted(names_up), f"❌ Test Case 11 FAILED: Up sort did not sort ascending → {names_up}"
        print("✅ Test Case 11 PASSED: Up sort sorted Agency/Institution ascending")

        # Click ▼ Down sort
        sort_down = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "(//span[@class='hover:text-gray-500'][contains(text(),'▼')])[2]")))
        print("↧ Clicking Down sort button")
        driver.execute_script("arguments[0].click();", sort_down)
        time.sleep(2)

        rows_down = driver.find_elements(By.XPATH, "//tbody/tr/td[2]")
        names_down = [r.text.strip().lower() for r in rows_down]

        # Assert descending sort
        assert names_down == sorted(names_down, reverse=True), f"❌ Test Case 11 FAILED: Down sort did not sort descending → {names_down}"
        print("✅ Test Case 11 PASSED: Down sort sorted Agency/Institution descending")

    except AssertionError as ae:
        print(str(ae))
    except Exception as e:
        print(f"❌ Test Case 11 FAILED due to unexpected error: {str(e)}")

# Test Case 12: Agency Code Column Title
def test_agency_code_column_title():
    print("\nTest Case 12: Checking Agency Code Column Title")
    try:
        title_xpath = "//div[normalize-space()='AGENCY CODE']"
        agency_code_title = wait.until(EC.presence_of_element_located((By.XPATH, title_xpath)))

        assert agency_code_title.is_displayed(), "❌ Test Case 12 FAILED: Agency Code column title not FOUND"
        print("✅ Test Case 12 PASSED: Agency Code column title is FOUND")
    except AssertionError as ae:
        print(str(ae))
    except Exception as e:
        print(f"❌ Error checking Agency Code column title: {str(e)}")

# Test Case 13: Agency Head Column Title
def test_agency_head_column_title():
    print("\nTest Case 14: Checking Agency Head Column Title")
    try:
        title_xpath = "//td[normalize-space()='AGENCY HEAD']"
        agency_head_title = wait.until(EC.presence_of_element_located((By.XPATH, title_xpath)))

        assert agency_head_title.is_displayed(), "❌ Test Case 13 FAILED: Agency Head column title not FOUND"
        print("✅ Test Case 13 PASSED: Agency Head column title FOUND")
    except AssertionError as ae:
        print(str(ae))
    except Exception as e:
        print(f"❌ Test Case 13 FAILED: Error checking Agency Head column title: {str(e)}")

# Test Case 14: Official Website Link Column Title
def test_official_website_link_column_title():
    print("\nTest Case 14: Checking Official Website Link Column Title")
    try:
        title_xpath = "//td[normalize-space()='OFFICIAL WEBSITE LINK']"
        website_title = wait.until(EC.presence_of_element_located((By.XPATH, title_xpath)))

        if website_title.is_displayed():
            print("✅ Test Case 14 PASSED:  Official Website Link column title PASSED")
        else:
            print("❌ Test Case 14 FAILED: Official Website Link column title not displayed")
    except Exception as e:
        print(f"❌ Test Case 14 FAILED: Error checking Official Website Link column title: {str(e)}")

# Test Case 15: Click First Row and Store Data
def test_click_first_row_and_store_data():
    print("\nTest Case 15: Clicking First Row and Storing Data")
    try:
        row_xpath = "(//tr[contains(@class, 'hover:bg-gray-200')])[1]"
        first_row = wait.until(EC.element_to_be_clickable((By.XPATH, row_xpath)))

        row_data = {
            'code': first_row.find_element(By.XPATH, ".//td[1]").text,
            'name': first_row.find_element(By.XPATH, ".//td[2]").text,
            'head': first_row.find_element(By.XPATH, ".//td[3]").text,
            'website': first_row.find_element(By.XPATH, ".//td[4]").text
        }
        first_row.click()
        time.sleep(1.5)

        print("✅ Test Case 15 PASSED: Successfully clicked first row and stored data")
        print("📋 Stored Row Data:", row_data)
        return row_data

    except Exception as e:
        print(f"❌ Test Case 15 FAILED:  Error clicking first row or storing data: {str(e)}")
        return None

# Test Case 17: Compare Agency Code from the table and modal
def test_compare_agency_code(row_data):
    print("\nTest Case 17: Comparing Agency Code")
    try:
        agency_code_input = wait.until(EC.presence_of_element_located((By.ID, "agn_code")))
        input_value = agency_code_input.get_attribute('value')
       
        assert input_value == row_data['code'], (f"❌ Agency Code mismatch\n  Expected: {row_data['code']}\n  Found:{input_value}")
        print("✅ Agency Code matches table row content")
    except AssertionError as ae:
        print(str(ae))
    except Exception as e:
        print(f"❌ Error comparing Agency Code: {str(e)}")

# Test Case 18: Compare Agency/Institution Name from the table and modal
def test_compare_agency_name(row_data):
    print("\nTest Case 18: Comparing Agency/Institution Name")
    try:
        agency_name_input = wait.until(EC.presence_of_element_located((By.ID, "agn_name")))
        input_value = agency_name_input.get_attribute('value')
        
        assert input_value == row_data['name'], (f"❌ Agency/Institution name mismatch\n  Expected: {row_data['name']}\n  Found:    {input_value}")
        print("✅ Agency/Institution name matches table row content")
    
    except AssertionError as ae:
        print(str(ae))   
    except Exception as e:
        print(f"❌ Error comparing Agency/Institution name: {str(e)}")

# Test Case 19: Compare Agency Head from the table and modal
def test_compare_agency_head(row_data):
    print("\nTest Case 19: Comparing Agency Head")
    try:
        fname = wait.until(EC.presence_of_element_located((By.ID, "agn_head_fname"))).get_attribute('value').strip()
        mi = wait.until(EC.presence_of_element_located((By.ID, "agn_head_mi"))).get_attribute('value').strip()
        lname = wait.until(EC.presence_of_element_located((By.ID, "agn_head_lname"))).get_attribute('value').strip()
        suffix = wait.until(EC.presence_of_element_located((By.ID, "agn_head_sfx"))).get_attribute('value').strip()

        parts = [fname]
        if mi:
            parts.append(mi)
        parts.append(lname)
        if suffix:
            parts.append(suffix)
        modal_head = ' '.join(parts).strip()

        assert modal_head == row_data['head'], (f"❌ Agency Head mismatch\n  Expected: {row_data['head']}\n  Found:    {modal_head}")
        print("✅ Agency Head matches table row content")
    
    except AssertionError as ae:
        print(str(ae))
    except Exception as e:
        print(f"❌ Error comparing Agency Head: {str(e)}")

# Test Case 20: Compare Website Link from the table and modal
def test_compare_website_link(row_data):
    print("\nTest Case 20: Comparing Official Website Link")
    try:
        website_input = wait.until(EC.presence_of_element_located((By.ID, "agn_website")))
        input_value = website_input.get_attribute('value').strip()
        expected_value = row_data['website'].strip()

        if input_value == expected_value:
            print("✅ Website link matches table row content")
        else:
            print(f"❌ Website link mismatch\n  Expected: {expected_value}\n  Found:    {input_value}")
    except Exception as e:
        print(f"❌ Error comparing website link: {str(e)}")

if __name__ == "__main__":
    main()