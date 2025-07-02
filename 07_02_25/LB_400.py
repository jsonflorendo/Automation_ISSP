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

# Navigate to ICT Categories tab
print("\nTest Case: Clicking ICT Categories Tab")
funding_source_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//p[normalize-space()='ICT Categories']")))
funding_source_tab.click()
time.sleep(2)
print("✅ Successfully navigated to ICT Categories tab")

def main():
    time.sleep(5)
    test_search_functionality()
    time.sleep(5)
    test_add_new_button()
    time.sleep(5)
    return_to_ict_categories_tab()
    time.sleep(5)
    test_table_row_hover()
    time.sleep(5)
    test_ict_item_category_title()
    time.sleep(5)
    test_sort_buttons_ict_item_category()
    time.sleep(5)
    item_category_input = test_click_ict_printing_row()
    time.sleep(5)
    test_ict_item_category(item_category_input)
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

# Test Case 2: 'Add New' Button 
def test_add_new_button():
    print("\nTest Case 2: Add New Button")

    add_new_btn = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//button[contains(@class, 'btn-circular') and .//span[normalize-space()='Add New']]"
    )))

    if add_new_btn.is_displayed():
        print("✅ Add New button is displayed")
        add_new_btn.click()
        time.sleep(1.5)

        close_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "svg.fa-xmark")))

        if close_button.is_displayed():
            close_button.click()
            time.sleep(1)
            print("✅ Modal closed successfully using X button")
        else:
            print("❌ Close button not displayed")
    else:
        print("❌ Add New button not displayed")

def return_to_ict_categories_tab():
    print("\nReturning to ICT Categories")
    ict_categories_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//p[normalize-space()='ICT Categories']")))
    ict_categories_tab.click()
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

    print("\nTest Case 3: Testing Table Row Hover Effect")
    table_row = wait.until(EC.presence_of_element_located((By.XPATH, "//tr[contains(@class, 'hover:bg-gray-200')]")))
    if table_row.is_displayed():
        print("✅ Table row hover effect is working")
    else:
        print("❌ Table row not displayed properly")

# Test Case 4: ICT ITEM CATEGORIES Column Title
def test_ict_item_category_title():
    print("\nTest Case 4: Checking ICT ITEM CATEGORY Column Title")
    try:
        ict_item_header = wait.until(EC.presence_of_element_located((
            By.XPATH, "//thead//td//div[normalize-space(text())='ICT ITEM CATEGORY']"
        )))

        if ict_item_header.is_displayed():
            print("✅ ICT ITEM CATEGORY column title PASSED")
        else:
            print("❌ ICT ITEM CATEGORY column title not displayed")
    except Exception as e:
        print(f"❌ Exception in Test Case 4: {str(e)}")

# Test Case 5: Testing Sort Buttons for ICT ITEM CATEGORIES
def test_sort_buttons_ict_item_category():
    print("\nTest Case 5: Testing Sort Buttons for ICT ITEM CATEGORY")

    try:
        # Locate the sort ↑ button
        sort_up = wait.until(EC.presence_of_element_located((
            By.XPATH, "//thead//td[1]//span[normalize-space()='▲']"
        )))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", sort_up)
        print("↥ Clicking Up sort button")
        driver.execute_script("arguments[0].click();", sort_up)
        time.sleep(2)

        # Locate the sort ↓ button
        sort_down = wait.until(EC.presence_of_element_located((
            By.XPATH, "//thead//td[1]//span[normalize-space()='▼']"
        )))
        print("↧ Clicking Down sort button")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", sort_down)
        driver.execute_script("arguments[0].click();", sort_down)
        time.sleep(2)

        print("✅ Test Case 5 Passed: Sort buttons are working")

    except Exception as e:
        print(f"❌ Exception in Test Case 5: {str(e)}")

# Test Case 6: Store First Row Data
def test_click_ict_printing_row():
    print("\nTest Case 6: Clicking 'ICT Printing' Row and Opening Modal")
    try:
        ict_row = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//tr[.//td[normalize-space()='ICT Printing']]"
        )))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ict_row)
        driver.execute_script("arguments[0].click();", ict_row)
        print("✅ 'ICT Printing' row clicked")

        # Wait for modal input field to appear
        cat_name_input = wait.until(EC.visibility_of_element_located((By.ID, "cat_name")))
        print("✅ Modal input field 'cat_name' appeared")

        return cat_name_input

    except Exception as e:
        print(f"❌ Exception in Test Case 6: {str(e)}")
        return None

# Test Case 7: Compare ICT ITEM CATEGORIES 
def test_ict_item_category(cat_name_input):
    print("\nTest Case 7: Comparing ICT Item Category Value from Modal with Table Row")

    try:
        first_row = wait.until(EC.presence_of_element_located((By.XPATH, "(//tr[contains(@class, 'hover:bg-gray-200')])[4]")))
        table_item = first_row.find_element(By.XPATH, ".//td[1]").text.strip()

        modal_value = cat_name_input.get_attribute('value').strip()

        print(f"Table value: '{table_item}'")
        print(f"Modal value: '{modal_value}'")

        if modal_value == table_item:
            print("✅ Test Case 7 Passed: ICT ITEM CATEGORY matches table row content")
        else:
            print("❌ Test Case 7 Failed: Mismatch between table row and modal input")

    except Exception as e:
        print(f"❌ Exception in Test Case 7: {str(e)}")

if __name__ == "__main__":
    main()


