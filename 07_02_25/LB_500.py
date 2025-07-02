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

# Navigate to ICT Items tab
print("\nTest Case: Clicking ICT Items Tab")
ict_items_tab = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//ul/li[4]//label[contains(text(), 'ICT Items')]")))
ict_items_tab.click()
time.sleep(2)
print("✅ Successfully navigated to ICT Items tab")

def main():
    test_search_functionality()
    time.sleep(5)
    test_add_new_button()
    time.sleep(5)
    return_to_ict_items_tab()
    time.sleep(5)
    test_table_row_hover()
    time.sleep(5)
    test_ict_item_col_title()
    time.sleep(5)
    test_est_cost_col_title()
    time.sleep(5)
    test_specs_col_title()
    time.sleep(5)
    ict_items_sort_btn()
    time.sleep(5)
    name_input, cost_input, desc_input = test_click_cloud_live_site_row()
    time.sleep(5)
    test_ict_item(name_input, cost_input, desc_input)
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

    add_new_button = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//button[contains(@class, 'btn-circular') and .//span[normalize-space()='Add New']]"
    )))

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

def return_to_ict_items_tab():
    print("\nReturning to ICT Items")
    ict_items_tab = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//ul/li[4]//label[contains(text(), 'ICT Items')]")))
    ict_items_tab.click()
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

# Test Case 4: ICT ITEM  Column Title
def test_ict_item_col_title():
    print("\nTest Case 4: Checking ICT ITEMS Column Title")
    try:
        ict_item_header = wait.until(EC.presence_of_element_located((By.XPATH, "//thead//td[1]//div[normalize-space()='ICT ITEM']")))
        
        assert ict_item_header.is_displayed(), "❌ ICT ITEM Column title NOT FOUND"
        print("✅ ICT ITEM Column title FOUND")

    except AssertionError as ae:
        print(str(ae))
    except Exception as e:
        print(f"❌ Exception in Test Case 4: {str(e)}")

# Test Case 5: ESTIMATED COST PER UOM Column Title	
def test_est_cost_col_title():
    print("\nTest Case 5: Checking Estimated Cost Per UOM Column Title")
    try:
        est_cost_header = wait.until(EC.presence_of_element_located((
            By.XPATH, "//thead//td[2][normalize-space()='ESTIMATED COST PER UOM']"
        )))
        assert est_cost_header.is_displayed(), "❌ ESTIMATED COST PER UOM Column title NOT FOUND"
        print("✅ ESTIMATED COST PER UOM Column title FOUND")

    except AssertionError as ae:
        print(str(ae))
    except Exception as e:
        print(f"❌ Exception in Test Case 5: {str(e)}")

# Test Case 6: SPECIFICATIONS Column Title
def test_specs_col_title():
    print("\nTest Case 6: Checking SPECIFICATIONS Column Title")
    try:
        specs_header = wait.until(EC.presence_of_element_located((
            By.XPATH, "//thead//td[3][normalize-space()='SPECIFICATIONS']"
        )))
        assert specs_header.is_displayed(), "❌ SPECIFICATIONS Column title not displayed"
        print("✅ SPECIFICATIONS Column title PASSED")
    except AssertionError as ae:
        print(str(ae))
    except Exception as e:
        print(f"❌ Exception in Test Case 6: {str(e)}")

# Test Case 7: Checking Sort Buttons
def ict_items_sort_btn():
    print("\nTest Case 7: Checking Sort Buttons for ICT Items")

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

        assert categories_up == sorted(categories_up, reverse=True), f"❌ Test Case 5 FAILED: Up sort did not sort descending → {categories_up}"
        print("✅ Test Case 5 PASSED: Up sort sorted ICT ITEM descending") 

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

        assert categories_down == sorted(categories_down), f"❌ Test Case 7 FAILED: Down sort did not sort ascending → {categories_down}"
        print("✅ Test Case 7 PASSED: Down sort sorted ICT ITEM ascending")

    except AssertionError as ae:
        print(str(ae))
    except Exception as e:
        print(f"❌ Test Case 7 FAILED due to unexpected error: {str(e)}")

# Test Case 8: Clicking 'Cloud Live Site' Row and Verifying Modal
def test_click_cloud_live_site_row():
    print("\nTest Case 8: Clicking 'Cloud Live Site' Row and Verifying Modal")

    try:
        ict_row = wait.until(EC.element_to_be_clickable((By.XPATH, "//tr[td[normalize-space()='Cloud Live Site']]")))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", ict_row)
        driver.execute_script("arguments[0].click();", ict_row)
        print("✅ 'Cloud Live Site' row clicked")
        time.sleep(5)
        itm_name_input = wait.until(EC.visibility_of_element_located((By.ID, "itm_name"))) #td[1]
        itm_cost_input = wait.until(EC.visibility_of_element_located((By.ID, "itm_cost"))) #td[2]
        itm_desc_input = wait.until(EC.visibility_of_element_located((By.ID, "itm_desc"))) #td[3]

        print("✅ Modal input field 'itm_name' appeared")
        return itm_name_input, itm_cost_input, itm_desc_input

    except Exception as e:
        print(f"❌ Exception in clicking 'Cloud Live Site' row: {str(e)}")

def test_ict_item(itm_name_input, itm_cost_input, itm_desc_input):
    print("\nTest Case 9: Comparing ICT Item Modal Values with Table Row")

    try:
        row = wait.until(EC.presence_of_element_located((
            By.XPATH, "//tr[td[normalize-space()='Cloud Live Site']]"
        )))

        # Table values
        table_item_name = row.find_element(By.XPATH, "./td[1]").text.strip()
        table_item_cost = row.find_element(By.XPATH, "./td[2]").text.strip().replace("₱", "").split("/")[0].strip()
        table_item_specs = row.find_element(By.XPATH, "./td[3]").text.strip()

        # Modal values
        modal_item_name = itm_name_input.get_attribute('value').strip()
        modal_item_cost = itm_cost_input.get_attribute('value').strip()
        modal_item_specs = itm_desc_input.get_attribute('value').strip()

        # Comparison
        name_match = modal_item_name == table_item_name
        cost_match = modal_item_cost in table_item_cost or table_item_cost in modal_item_cost
        specs_match = modal_item_specs.startswith(table_item_specs[:20])  # fuzzy match start

        
        assert name_match and cost_match and specs_match, (
            "❌ Test Case 9 Failed:\n" +
            ("" if name_match else "   - ITEM NAME mismatch\n") +
            ("" if cost_match else "   - COST mismatch\n") +
            ("" if specs_match else "   - SPECIFICATIONS mismatch")
        )
        print("✅ Test Case 9 Passed: Modal values match table row content")

    except AssertionError as ae:
        print(str(ae))
    except Exception as e:
        print(f"❌ Exception in Test Case 9: {str(e)}")


if __name__ == "__main__":
    main()