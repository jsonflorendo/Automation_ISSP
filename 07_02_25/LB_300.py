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


# Navigate to Funding Source tab
print("\nTest Case: Clicking Funding Source Tab")
funding_source_tab = wait.until(EC.element_to_be_clickable((
    By.XPATH, "//p[normalize-space()='Funding Source']"
)))
funding_source_tab.click()
time.sleep(2)
print("✅ Test Case 0 PASSED: Successfully navigated to Funding Source tab")


def main():
    time.sleep(5)
    test_search_functionality()
    time.sleep(5)
    test_add_new_button()
    time.sleep(5)
    return_to_funding_source_tab()
    time.sleep(5)
    test_table_row_hover()
    time.sleep(5)
    test_funding_source_code_title()
    time.sleep(5)
    test_funding_source_title()
    time.sleep(5)
    funding_source_code_sort_btn()
    time.sleep(5)
    test_funding_source_sort_btn()
    time.sleep(5)
    return_to_funding_source_tab()
    time.sleep(5)
    row_data = click_first_row()
    time.sleep(5)
    test_funding_source_code(row_data)
    time.sleep(5)
    test_funding_source_name(row_data)
    time.sleep(5)
    test_close_btn()
    time.sleep(5)

    print("/********* END OF THE TEST *********/")
    driver.quit()


# Test Case 1: Search 
def test_search_functionality():
    print("\nTest Case 1: Testing Search Functionality")

    search_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[contains(@placeholder, 'Search...')]")))
    search_icon = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[.//*[name()='svg' and contains(@data-icon, 'magnifying-glass')]]")))

    try:
        assert search_icon.is_displayed() and search_input.is_displayed(), \
            "❌ Test Case 1 FAILED: Search elements not displayed properly"
        print("✅ Search icon and input field are displayed")

        search_input.send_keys("test search")
        time.sleep(1)
        search_input.clear()
        time.sleep(1)

        driver.refresh()
        print("✅ Test Case 1 PASSED: Search input worked and page was refreshed")

    except AssertionError as ae:
        print(str(ae))


# Test Case 2: Add New Button and Modal
def test_add_new_button():
    print("\nTest Case 2: Add New Button")

    add_new_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn-circular') and .//span[normalize-space()='Add New']]")))

    if add_new_button.is_displayed():
        print("✅ Add New button is displayed")
        add_new_button.click()
        time.sleep(1.5)

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

# Return to Funding Source tab
def return_to_funding_source_tab():
    print("\nReturning to Funding Source tab")
    funding_source_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//p[normalize-space()='Funding Source']")))
    funding_source_tab.click()
    time.sleep(5)

# Test Case 3: Table Row Hover 
def test_table_row_hover():
    print("\nTest Case 3: Testing Table Row ")
    table_row = wait.until(EC.presence_of_element_located((By.XPATH, "//tr[contains(@class, 'hover:bg-gray-200')]")))
    try:
        assert table_row.is_displayed(), "❌ Test Case 3 FAILED: Table row hover effect not working properly"
        print("✅ Test Case 3 PASSED: Working table row hover")
    except AssertionError as ae:
        print(str(ae))
    
# Test Case 4: Funding Source Code Column Title
def test_funding_source_code_title():
    print("\nTest Case 4: Checking Funding Source Code Column Title")
    fscode_header = wait.until(EC.presence_of_element_located((By.XPATH, "//thead//td[1]//div[contains(text(), 'FUNDING SOURCE CODE')]")))
    
    try:
        assert fscode_header.is_displayed(), "❌ Test Case 4 FAILED: Funding Source Code column Title not found"
        print("✅ Test Case 4 PASSED: Funding source code title found")
    except AssertionError as ae:
        print(str(ae))
    

# Test Case 5: Funding Source Column Title
def test_funding_source_title():
    print("\nTest Case 5: Checking Funding Source Column Title")
    fs_title = wait.until(EC.presence_of_element_located((By.XPATH, "//thead//tr/td[2]//div[contains(text(), 'FUNDING SOURCE')]")))
    
    try:
        assert fs_title.is_displayed(), "❌ Test Case 5 PASSED: Funding Source column title not found"
        print("✅ Test Case 5 PASSED: Name of Funding Source table column title found")
    except AssertionError as ae:
        print(str(ae))

# Test Case 6: Checking Sort Buttons for Funding Source Code
def funding_source_code_sort_btn():
    print("\nTest Case 6: Checking Sort Buttons for Funding Source Code")

    # Get original order
    rows_before = driver.find_elements(By.XPATH, "//tbody/tr/td[1]")
    codes_before = [r.text.strip() for r in rows_before]

    # Click ▲ Up sort
    sort_up = wait.until(EC.element_to_be_clickable((By.XPATH, "//thead//td[1]//span[normalize-space()='▲']")))
    print("↥ Clicking Up sort button")
    driver.execute_script("arguments[0].click();", sort_up)
    time.sleep(2)

    rows_up = driver.find_elements(By.XPATH, "//tbody/tr/td[1]")
    codes_up = [r.text.strip() for r in rows_up]

    # Assert it's sorted ascending
    assert codes_up == sorted(codes_up), f"❌ Test Case 6 FAILED: Up sort did not sort ascending → {codes_up}"
    print("✅ Test Case 6 PASSED: Up sort sorted Funding Source Code ascending")

    # Click ▼ Down sort
    sort_down = wait.until(EC.element_to_be_clickable((By.XPATH, "//thead//td[1]//span[normalize-space()='▼']")))
    print("↧ Clicking Down sort button")
    driver.execute_script("arguments[0].click();", sort_down)
    time.sleep(2)

    rows_down = driver.find_elements(By.XPATH, "//tbody/tr/td[1]")
    codes_down = [r.text.strip() for r in rows_down]

    # Assert it's sorted descending
    assert codes_down == sorted(codes_down, reverse=True), f"❌ Test Case 6 FAILED: Down sort did not sort descending → {codes_down}"
    print("✅ Test Case 6 PASSED: Down sort sorted Funding Source Code descending")

# Test Case 7: Checking Sort Buttons for Funding Source
def test_funding_source_sort_btn():
    print("\nTest Case 7: Checking Sort Buttons for Funding Source")

    # Get original list 
    fs_before = driver.find_elements(By.XPATH, "//tbody/tr/td[2]")
    fs_values_before = [cell.text.strip() for cell in fs_before]

    # Click ▲ Up sort button
    fs_sort_up = wait.until(EC.element_to_be_clickable((By.XPATH, "//thead//td[2]//span[normalize-space()='▲']")))
    driver.execute_script("arguments[0].click();", fs_sort_up)
    print("↥ Clicking Up sort button")
    time.sleep(2)

    fs_up = driver.find_elements(By.XPATH, "//tbody/tr/td[2]")
    fs_values_up = [cell.text.strip() for cell in fs_up]

    assert fs_values_up == sorted(fs_values_up), \
        f"❌ Test Case 7 FAILED: Up sort did not sort Funding Source ascending → {fs_values_up}"
    print("✅ Test Case 7 PASSED: Funding Source sorted ascending")

    # Click ▼ Down sort button
    fs_sort_down = wait.until(EC.element_to_be_clickable((By.XPATH, "//thead//td[2]//span[normalize-space()='▼']")))
    driver.execute_script("arguments[0].click();", fs_sort_down)
    print("↧ Clicking Down sort button")
    time.sleep(2)

    fs_down = driver.find_elements(By.XPATH, "//tbody/tr/td[2]")
    fs_values_down = [cell.text.strip() for cell in fs_down]

    assert fs_values_down == sorted(fs_values_down, reverse=True), \
        f"❌ Test Case 7 FAILED: Down sort did not sort Funding Source descending → {fs_values_down}"
    print("✅ Test Case 7 PASSED: Funding Source sorted descending")

# Test Case 8: Getting First Row 
def click_first_row():
    print("\nTest Case 8: Clicking First Row")

    try:
        first_row = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//table//tbody/tr[1]")
        ))

        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", first_row)
        time.sleep(1)

        row_data = {
            'code': first_row.find_element(By.XPATH, "./td[1]").text.strip(),
            'name': first_row.find_element(By.XPATH, "./td[2]").text.strip()
        }
        driver.execute_script("arguments[0].click();", first_row)
        time.sleep(1.5)

        print(f"✅ Test Case 8 PASSED: Clicked row with code='{row_data['code']}' and name='{row_data['name']}'")

        return row_data
    except Exception as e:
        print("❌ Test Case 8 FAILED with Exception:", str(e))

# Test Case 9: Compare Funding Source Code from the table and modal
def test_funding_source_code(row_data):
    print("\nTest Case 9: Comparing Funding Source Code")
    
    fs_code_input = wait.until(EC.presence_of_element_located((By.ID, "fnd_code")))     
    
    try:
        assert fs_code_input.get_attribute('value') == row_data['code'], "❌ Test Case 9 FAILED: Funding Source Code mismatch"
        print("✅ Test Case 9 PASSED: Funding Source Code matches table row content")

    except AssertionError as ae:
        print(str(ae))

# Test Case 10: Compare Funding Source Name from the table and modal
def test_funding_source_name(row_data):
    print("\nTest Case 10: Comparing Funding Source Name")    
    fs_name_input = wait.until(EC.presence_of_element_located((By.ID, "fnd_name")))     

    try:
        assert fs_name_input.get_attribute('value') == row_data['name'], "❌ Test Case 10 FAILED: Funding Source Name mismatch"
        print("✅ Test Case 10 PASSED: Funding Source Name matches table row content")
    except AssertionError as ae:
        print(str(ae))

# Test Case 11: Close Button
def test_close_btn(): 
    print("\nTest Case 11: Testing Close Button")
    close_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "svg.fa-xmark")))

    try:
        assert close_button.is_displayed(), "❌ Test Case 11 FAILED: X button not displaye"
        close_button.click()
        time.sleep(1)
        print("✅ Test Case 11 PASSED: Modal closed successfully using Close button")
    except AssertionError as ae:
        print(str(ae))

if __name__ == "__main__":
    main()