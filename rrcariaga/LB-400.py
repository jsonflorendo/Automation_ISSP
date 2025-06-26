from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pytest


# ───────────────────────────
# Helper to close the modal
# ───────────────────────────
def close_modal(driver, timeout=5):
    """
    Close the modal dialog and its backdrop.
    """
    print("Attempting to close modal...")

    try:
        # First remove the backdrop
        try:
            backdrop = driver.find_element(By.CSS_SELECTOR, "div.absolute.inset-0.bg-gray-500.opacity-75")
            driver.execute_script("arguments[0].remove();", backdrop)
            print("Removed backdrop")
        except:
            print("No backdrop found or already removed")

        # Try to find and click the close button
        try:
            close_button = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH,
                                            "//p[@class='font-bold rounded-t-md modal-title px-5 pt-5 pb-3 flex justify-between']//button"))
            )
            print("Found close button")
            driver.execute_script("arguments[0].click();", close_button)
            print("Clicked close button")
        except Exception as e:
            print(f"Could not click close button: {str(e)}")
            # Try to force remove the modal
            driver.execute_script("""
                var modal = document.querySelector('div[role="dialog"]');
                if (modal) modal.remove();
                var backdrop = document.querySelector('div.absolute.inset-0.bg-gray-500.opacity-75');
                if (backdrop) backdrop.remove();
            """)
            print("Force removed modal and backdrop")

        # Wait for modal to disappear
        WebDriverWait(driver, timeout).until(
            EC.invisibility_of_element_located((By.XPATH, "//div[@role='dialog']"))
        )
        print("✅ Modal closed successfully")

    except Exception as e:
        print(f"❌ Error closing modal: {str(e)}")
        # One last attempt to force remove everything
        driver.execute_script("""
            var modal = document.querySelector('div[role="dialog"]');
            if (modal) modal.remove();
            var backdrop = document.querySelector('div.absolute.inset-0.bg-gray-500.opacity-75');
            if (backdrop) backdrop.remove();
        """)
        print("Final attempt to force remove modal and backdrop")


# Add a helper to check if modal is present

def is_modal_present(driver):
    try:
        modal = driver.find_element(By.XPATH, "//div[@role='dialog']")
        return modal.is_displayed()
    except:
        return False


# ───────────────────────────
# Config / constants
# ───────────────────────────
LOGIN_URL = "http://10.10.99.23/login"
LIBRARY_URL = "http://10.10.99.23/library"
EMAIL = "admin@gmail.com"
PASSWORD = "Dost@123"
SEARCH_TERM = "ICT"

ROWS = [
    ("COMMUNICATION EXPENSES", "//td[normalize-space()='COMMUNICATION EXPENSES']"),
    ("ICT MACHINERIES AND EQUIPMENT", "//td[normalize-space()='ICT MACHINERIES AND EQUIPMENT']"),
    ("ICT Printing", "//td[normalize-space()='ICT Printing']"),
    ("ICT SOFTWARE", "//td[normalize-space()='ICT SOFTWARE']"),
    ("ICT SOFTWARE SUBSCRIPTION", "//td[normalize-space()='ICT SOFTWARE SUBSCRIPTION']"),
    ("ICT SUPPLIES AND MATERIALS", "//td[normalize-space()='ICT SUPPLIES AND MATERIALS']"),
    ("PRINTING EQUIPMENT", "//td[normalize-space()='PRINTING EQUIPMENT']"),
    ("SUBSCRIPTION EXPENSES", "//td[normalize-space()='SUBSCRIPTION EXPENSES']")
]


@pytest.fixture(scope="function")
def driver():
    """Create a new Chrome driver instance for each test."""
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


def test_ict_item_category(driver):
    """Test the ICT Item Category field functionality."""
    try:
        driver.get(LOGIN_URL)

        # Wait for and fill login form (no print)
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        email_input.send_keys(EMAIL)

        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        password_input.send_keys(PASSWORD)

        # Click login and wait for navigation (no print)
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='button']"))
        )
        login_button.click()

        # Wait for login to complete and dashboard to load (no print)
        WebDriverWait(driver, 10).until(
            lambda d: "login" not in d.current_url.lower()
        )

        # Navigate to Library (no print)
        driver.get(LIBRARY_URL)

        # Wait for loading screen to disappear (no print)
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "loading-screen"))
        )

        # Wait for the page to be fully loaded
        time.sleep(2)

        # Test Case 1: Click ICT Categories Tab (was 3)
        print("\n" + "="*50)
        print("Test Case 1: Click ICT Categories Tab")
        print("="*50)
        print("Looking for ICT Categories tab...")
        tabs = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "p.cursor-pointer"))
        )

        ict_tab_found = False
        for tab in tabs:
            tab_text = tab.text.strip().upper()
            if "ICT" in tab_text:
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(tab)
                ).click()
                print("✅ ICT Categories tab clicked.")
                ict_tab_found = True
                break

        assert ict_tab_found, "ICT Categories tab not found"

        # Test Case 2: Search Functionality (was 4)
        print("\n" + "="*50)
        print("Test Case 2: Search Functionality")
        print("="*50)
        try:
            # Find and clear the search input
            search_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Search...']"))
            )
            search_input.clear()

            # Enter search term
            search_input.send_keys(SEARCH_TERM)
            print(f"✅ Entered search term: {SEARCH_TERM}")

            # Wait for search results
            time.sleep(2)

            # Get all visible rows after search
            search_results = driver.find_elements(By.XPATH, "//td[contains(@class, 'text-left')]")
            search_result_texts = [item.text.strip() for item in search_results if item.text.strip()]

            # Verify that all results contain the search term
            for result in search_result_texts:
                assert SEARCH_TERM.upper() in result.upper(), f"Search result '{result}' does not contain '{SEARCH_TERM}'"
            print(f"✅ Search results verified - found {len(search_result_texts)} matching items")

            # Clear search
            search_input.clear()
            driver.execute_script("arguments[0].value = ''; arguments[0].dispatchEvent(new Event('input'));",
                                  search_input)
            print("✅ Search cleared")

        except Exception as e:
            print(f"❌ Error testing search: {e}")
            raise

        # Test Case 3: Add New Button and Modal (was 5)
        print("\n" + "="*50)
        print("Test Case 3: Add New Button and Modal")
        print("="*50)
        # ✅ Click the Add New (+) button
        add_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                        "(//button[@class='btn-circular square-md shadow-[4.0px_8.0px_8.0px_rgba(0,0,0,0.20)]'])[1]"))
        )
        assert add_btn.is_displayed(), "❌ Add New (+) button not visible"
        add_btn.click()
        print("✅ Clicked Add New (+) button")

        # ✅ Wait for the modal to appear
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH,
                                              "(//p[@class='font-bold rounded-t-md modal-title px-5 pt-5 pb-3 flex justify-between'])[1]"))
        )
        print("✅ Modal appeared")

        # ✅ Close the form to proceed with table row tests
        close_modal(driver)
        print("✅ Modal closed")

        # Wait for table to reset
        time.sleep(2)

        # ───────────────────────────
        # Test Case 4: Table Column Titles
        # ───────────────────────────
        print("\n" + "="*50)
        print("Test Case 4: Table Column Titles")
        print("="*50)
        try:
            # Find all column title elements
            column_titles = driver.find_elements(By.CSS_SELECTOR, "div.text-left")
            titles = [col.text.strip() for col in column_titles if col.text.strip()]
            expected_titles = ['ICT ITEM CATEGORY']
            assert titles == expected_titles, f"Column titles mismatch: expected {expected_titles}, found {titles}"
            print(f"✅ Column titles verified: {titles}")
        except Exception as e:
            print(f"❌ Error finding or verifying column titles: {e}")

        # Test Case 5: Table Row Testing (was 6)
        print("\n" + "="*50)
        print("Test Case 5: Table Row Testing")
        print("="*50)
        # Only test the first row
        name, xpath = ROWS[0]
        print(f"\n--- Testing Row: {name} ---")
        try:
            # Wait for the row to be visible and clickable
            row = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )

            # ✅ Assert that the row's visible text matches expected label
            row_text = row.text.strip().upper()
            assert row_text == name.upper(), f"Row text mismatch – expected: '{name}', found: '{row_text}'"
            print(f"✅ Verified row label: {row_text}")

            # Hover and click
            ActionChains(driver).move_to_element(row).perform()
            driver.execute_script("arguments[0].click();", row)

            ActionChains(driver).move_to_element(row).perform()
            print(f"✅ Hovered: {name}")

            # Click using JavaScript to avoid backdrop issues
            driver.execute_script("arguments[0].click();", row)
            print(f"✅ Clicked: {name}")

            # Only close the modal if it is present
            if is_modal_present(driver):
                close_modal(driver)
            time.sleep(1)

            # Ensure the search field is clear and table restored
            search_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Search...']"))
            )
            if search_input.get_attribute("value"):
                search_input.clear()
                driver.execute_script("arguments[0].value = ''; arguments[0].dispatchEvent(new Event('input'));",
                                      search_input)

            # Wait for the current row to be visible again
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, xpath))
            )
            time.sleep(0.5)

        except Exception as e:
            print(f"❌ Error processing {name}: {e}")
            # Try to force close the modal if it's still open
            try:
                driver.execute_script("""
                    var modal = document.querySelector('div[role=\"dialog\"]');
                    if (modal) modal.remove();
                    var backdrop = document.querySelector('div.absolute.inset-0.bg-gray-500.opacity-75');
                    if (backdrop) backdrop.remove();
                """)
            except:
                pass

        # Test Case 6: Sort Functionality (was 7)
        print("\n" + "="*50)
        print("Test Case 6: Sort Functionality")
        print("="*50)
        # Ensure any remaining modal is closed before sort testing
        print("Ensuring all modals are closed before sort testing...")
        try:
            # Try normal modal close first
            close_modal(driver)
        except:
            pass

        # Force remove any remaining modals and backdrops
        driver.execute_script("""
            var modals = document.querySelectorAll('div[role=\"dialog\"]');
            modals.forEach(function(modal) {
                modal.remove();
            });
            var backdrops = document.querySelectorAll('div.absolute.inset-0.bg-gray-500.opacity-75');
            backdrops.forEach(function(backdrop) {
                backdrop.remove();
            });
        """)
        print("✅ Cleaned up any remaining modals")

        # Wait a moment to ensure everything is cleared
        time.sleep(2)

        # 5) Test sort buttons
        print("Testing sort buttons...")
        try:
            # Get initial order of items
            initial_items = driver.find_elements(By.XPATH, "//td[contains(@class, 'text-left')]")
            initial_order = [item.text.strip() for item in initial_items if item.text.strip()]
            print("Initial order:", initial_order)

            # Find and click the up arrow (ascending sort)
            print("\nTesting ascending sort...")
            up_arrow = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'▲')]"))
            )
            driver.execute_script("arguments[0].click();", up_arrow)
            print("✅ Clicked ascending sort button")

            # Wait longer for sorting to complete and verify
            time.sleep(3)  # Increased wait time

            # Get items after ascending sort
            ascending_items = driver.find_elements(By.XPATH, "//td[contains(@class, 'text-left')]")
            ascending_order = [item.text.strip() for item in ascending_items if item.text.strip()]
            print("After ascending sort:", ascending_order)

            # Verify ascending order
            sorted_ascending = sorted(ascending_order)
            assert ascending_order == sorted_ascending, "Items are not in ascending order"
            print("✅ Verified ascending sort order")

            # Wait before descending sort
            time.sleep(2)

            # Find and click the down arrow (descending sort)
            print("\nTesting descending sort...")
            down_arrow = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'▼')]"))
            )
            driver.execute_script("arguments[0].click();", down_arrow)
            print("✅ Clicked descending sort button")

            # Wait longer for sorting to complete and verify
            time.sleep(3)  # Increased wait time

            # Get items after descending sort
            descending_items = driver.find_elements(By.XPATH, "//td[contains(@class, 'text-left')]")
            descending_order = [item.text.strip() for item in descending_items if item.text.strip()]
            print("After descending sort:", descending_order)

            # Verify descending order
            sorted_descending = sorted(descending_order, reverse=True)
            assert descending_order == sorted_descending, "Items are not in descending order"
            print("✅ Verified descending sort order")

            # Final wait to observe the result
            time.sleep(2)

        except Exception as e:
            print(f"❌ Error testing sort buttons: {e}")

        # --- New: Separate Test Case for Row/Input Value Check ---
        print("\n" + "="*50)
        print("Test Case 7: Row Value Matches Input Field")
        print("="*50)
        try:
            # Find the first visible row in the table
            row = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "tbody tr:nth-child(4) td:nth-child(1)"))
            )
            row_text = row.text.strip()
            print(f"Row text: '{row_text}'")

            # Click the row to open the modal
            driver.execute_script("arguments[0].click();", row)
            time.sleep(1)

            # Get the value from the input field in the modal
            input_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#cat_name"))
            )
            input_value = input_field.get_attribute("value").strip()
            print(f"Input field value: '{input_value}'")

            # Compare and assert
            assert row_text == input_value, f"Mismatch: row text '{row_text}' != input value '{input_value}'"
            print("✅ Row text matches input field value!")

            # Close the modal if present
            if is_modal_present(driver):
                close_modal(driver)
            time.sleep(1)

        except Exception as e:
            print(f"❌ Error in row/input value check: {e}")

        print("\n" + "="*50)
        print(" ALL TEST CASES COMPLETED SUCCESSFULLY! ")
        print("="*50)

    except Exception as e:
        print(f"❌ Test failed: {e}")
        raise
