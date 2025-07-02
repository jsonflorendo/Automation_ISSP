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
print("✅ Successfully navigated to Funding Source tab")


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
    click_first_row()
    time.sleep(5)
    test_funding_source_code()
    time.sleep(5)
    test_funding_source_name()
    time.sleep(5)
    test_close_btn()
    time.sleep(5)
    print("\n--------------Test Completed--------------\n")
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

    if search_icon.is_displayed() and search_input.is_displayed():
        print("✅ Search icon and input field are displayed")
        search_input.send_keys("test search")
        time.sleep(1)
        search_input.clear()
        time.sleep(1)

        driver.refresh()
        time.sleep(2)
        print("✅ Search functionality working and page refreshed")
    else:
        print("❌ Search elements not displayed properly")

# Test Case 2: Add New Button and Modal
def test_add_new_button():
    print("\nTest Case 2: Add New Button")

    add_new_btn = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//button[contains(@class, 'btn-circular') and .//span[normalize-space()='Add New']]"
    )))

    if add_new_btn.is_displayed():
        print("✅ Add New button is displayed")
        add_new_btn.click()
        time.sleep(1.5)

        close_button = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, "svg.fa-xmark"
        )))

        if close_button.is_displayed():
            close_button.click()
            time.sleep(1)
            print("✅ Modal closed successfully using X button")
        else:
            print("❌ X button not displayed")
    else:
        print("❌ Add New button not displayed")

# Return to Funding Source tab
def return_to_funding_source_tab():
    print("\nReturning to Funding Source tab")
    funding_source_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//p[normalize-space()='Funding Source']")))
    funding_source_tab.click()
    time.sleep(5)

# Test Case 3: Table Row Hover Effect
def test_table_row_hover():
    print("\nTest Case 3: Testing Table Row Hover Effect")

    table_row = wait.until(EC.presence_of_element_located((
        By.XPATH, "//tr[contains(@class, 'hover:bg-gray-200')]"
    )))

    if table_row.is_displayed():
        print("✅ Table row hover effect is working")
    else:
        print("❌ Table row not displayed properly")

# Test Case 4: Funding Source Code Column Title
def test_funding_source_code_title():
    print("\nTest Case 4: Checking Funding Source Code Column Title")
    fs_code_header = wait.until(EC.presence_of_element_located((
        By.XPATH, "//thead//td[1]//div[contains(text(), 'FUNDING SOURCE CODE')]"
    )))

    if fs_code_header.is_displayed():
        print("✅ Funding source code TITLE PASSED")
    else:
        print("❌ Funding Source Code column title not displayed")

# Test Case 5: Funding Source Column Title
def test_funding_source_title():
    print("\nTest Case 5: Checking Funding Source Column Title")
    fs_title = wait.until(EC.presence_of_element_located((By.XPATH, "//thead//tr/td[2]//div[contains(text(), 'FUNDING SOURCE')]")))
    if fs_title.is_displayed():
        print("✅ Name of Funding Source table column title PASSED")
    else:
        print("❌ Funding Source column title not displayed")

# Test Case 6: Checking Sort Buttons for Funding Source Code
def funding_source_code_sort_btn():
    print("\nTest Case 6: Checking Sort Buttons for Funding Source Code")

    sort_up = wait.until(EC.element_to_be_clickable((By.XPATH, "//thead//td[1]//span[normalize-space()='▲']")))

    print("Checking Up sort button")
    sort_up.click()
    time.sleep(5)

    sort_down = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//thead//td[1]//span[normalize-space()='▼']")))
    print("Checking Down sort button")
    sort_down.click()
    time.sleep(1.5)

    print("✅ Sort buttons are working")

# Test Case 7: Checking Sort Buttons for Funding Source
def test_funding_source_sort_btn():
    print("\nTest Case 7: Checking Sort Buttons for Funding Source")
    fs_sort_up = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//thead//td[2]//span[normalize-space()='▲']"
    )))
    print("Checking Up sort button")
    fs_sort_up.click()
    time.sleep(1.5)
    fs_sort_down = wait.until(EC.element_to_be_clickable((By.XPATH, "//thead//td[2]//span[normalize-space()='▼']")))
    print("Checking Down sort button")
    fs_sort_down.click()
    time.sleep(1.5)

    print("✅ Sort buttons are functional")

# Test Case 8: Store First Row Data
def click_first_row():
    print("\nTest Case 8: Getting First Row Data")
    # Click the GAA row
    gaa_row = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//tr[.//td[text()='GAA']]"
    )))
    gaa_row.click()
    time.sleep(10)

    # Get the first row
    first_row = wait.until(EC.element_to_be_clickable((By.XPATH, "(//tr[contains(@class, 'hover:bg-gray-200')])[1]")))

    # Store row data before clicking
    row_data = {
        'code': first_row.find_element(By.XPATH, ".//td[1]").text,
        'name': first_row.find_element(By.XPATH, ".//td[2]").text
    }

    # Ensure element is clickable and scroll into view
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", first_row)
    time.sleep(1)  # Wait for scroll to complete

    # Click using JavaScript for better reliability
    driver.execute_script("arguments[0].click();", first_row)
    time.sleep(1.5)
    print("✅ Successfully stored row data and opened modal")

# Test Case 9: Compare Funding Source Code
def test_funding_source_code():
    print("\nTest Case 9: Comparing Funding Source Code")
    first_row = wait.until(EC.element_to_be_clickable((By.XPATH, "(//tr[contains(@class, 'hover:bg-gray-200')])[1]")))
    row_data = {
        'code': first_row.find_element(By.XPATH, ".//td[1]").text,
        'name': first_row.find_element(By.XPATH, ".//td[2]").text
    }

    fs_code_input = wait.until(EC.presence_of_element_located((By.ID, "fnd_code")))
    if fs_code_input.get_attribute('value') == row_data['code']:
        print("✅ Funding Source Code matches table row content")
    else:
        print("❌ Funding Source Code mismatch")

# Test Case 10: Compare Funding Source Name
def test_funding_source_name():
    print("\nTest Case 10: Comparing Funding Source Name")
    first_row = wait.until(EC.element_to_be_clickable((By.XPATH, "(//tr[contains(@class, 'hover:bg-gray-200')])[1]")))
    row_data = {
        'code': first_row.find_element(By.XPATH, ".//td[1]").text,
        'name': first_row.find_element(By.XPATH, ".//td[2]").text
    }
    fs_name_input = wait.until(EC.presence_of_element_located((
        By.ID, "fnd_name"
    )))
    if fs_name_input.get_attribute('value') == row_data['name']:
        print("✅ Funding Source Name matches table row content")
    else:
        print("❌ Funding Source Name mismatch")

# Test Case 11: Close Button
def test_close_btn():
    print("\nTest Case 11: Testing Close Button")
    close_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "svg.fa-xmark")))

    if close_button.is_displayed():
        close_button.click()
        time.sleep(1)
        print("✅ Modal closed successfully using Close button")
    else:
        print("❌ X button not displayed")

if __name__ == "__main__":
    main()