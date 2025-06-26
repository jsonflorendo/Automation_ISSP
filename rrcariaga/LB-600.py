from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

# Config
LOGIN_URL = 'http://10.10.99.23/login'
LIBRARY_URL = 'http://10.10.99.23/library'
EMAIL = 'admin@gmail.com'
PASSWORD = 'Dost@123'
SEARCH_TERM = '@bicol-u.edu.ph'

# Set up the webdriver (using Chrome in this example)
driver = webdriver.Chrome()
driver.maximize_window()

try:
    driver.get(LOGIN_URL)

    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#email'))
    )
    email_input.clear()
    email_input.send_keys(EMAIL)

    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#password'))
    )
    password_input.clear()
    password_input.send_keys(PASSWORD)

    sign_in_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='button']"))
    )
    sign_in_button.click()

    WebDriverWait(driver, 10).until(EC.url_changes(LOGIN_URL))
    driver.get(LIBRARY_URL)

    print("\n" + "="*50)
    print("Test Case 1: Click User Accounts Tab")
    print("="*50)
    print("Clicking User Accounts tab...")

    # Wait for loading overlay to disappear if present
    try:
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, ".loading-screen"))
        )
        print("Loading screen is gone.")
    except Exception:
        print("No loading screen detected or it disappeared quickly.")

    user_accounts_tab = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//p[normalize-space()='User Accounts']"))
    )
    user_accounts_tab.click()
    time.sleep(1)

    print("\n" + "="*50)
    print("Test Case 2: Search Functionality")
    print("="*50)
    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Search...']"))
    )
    search_input.clear()
    search_input.send_keys(SEARCH_TERM)
    search_input.send_keys(Keys.RETURN)
    print(f"Searched for: {SEARCH_TERM}")
    time.sleep(2)

    print("Checking if any table row contains the search term...")
    found = False
    try:
        # Try to find a table cell containing the search term
        cell = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, f"//td[contains(text(), '{SEARCH_TERM}')]") )
        )
        print(f"✅ Found a row with '{SEARCH_TERM}': {cell.text}")
        found = True
    except Exception as e:
        print(f"❌ No row found with '{SEARCH_TERM}'.")

    # Clear the search field after search test
    print("\nClearing the search field...")
    search_input = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Search...']"))
    )
    search_input.clear()
    search_input.send_keys(Keys.RETURN)
    time.sleep(1)
    print("Search field cleared.")

    print("\n" + "="*50)
    print("Test Case 3: Add New Modal - Component Visibility")
    print("="*50)
    # Click the Add New button
    add_new_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class='btn-circular square-md shadow-[4.0px_8.0px_8.0px_rgba(0,0,0,0.20)]']"))
    )
    add_new_button.click()
    print("Clicked Add New button.")
    time.sleep(1)

    # Check if modal is displayed
    modal_displayed = False
    modal_selectors = [
        (By.CSS_SELECTOR, "div[role='dialog']"),
        (By.CSS_SELECTOR, "div.bg-white[role]"),
        (By.CSS_SELECTOR, "div.bg-white"),
        (By.XPATH, "//div[contains(@class, 'modal') or contains(@class, 'Modal')]")
    ]
    for m_by, m_selector in modal_selectors:
        try:
            modal = WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((m_by, m_selector))
            )
            modal_displayed = True
            break
        except Exception:
            continue
    if modal_displayed:
        print("✅ Modal is visible after clicking Add New.")
    else:
        print("❌ Modal did not appear after clicking Add New.")

    # Close the Add New modal before proceeding
    closed = False
    try:
        # Try to click Cancel button
        cancel_btn = driver.find_element(By.XPATH, "//button[normalize-space()='Cancel']")
        driver.execute_script("arguments[0].click();", cancel_btn)
        print("🛑 Closed Add New modal using Cancel button.")
        closed = True
    except Exception:
        try:
            # Try to click a close (X) button if present
            close_btn = driver.find_element(By.XPATH, "//button[contains(@class, 'btn-close') or contains(@aria-label, 'Close')]")
            driver.execute_script("arguments[0].click();", close_btn)
            print("🛑 Closed Add New modal using Close (X) button.")
            closed = True
        except Exception:
            # Fallback: Remove modal by JS
            driver.execute_script("var modal = document.querySelector('div[role=\\'dialog\\']'); if (modal) modal.remove();")
            print("🛑 Force removed Add New modal via JS.")
            closed = True
    if not closed:
        print("⚠️ Could not close Add New modal.")
    time.sleep(1)

    # Ensure search field is clear after closing modal
    try:
        search_input = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Search...']"))
        )
        search_input.clear()
        driver.execute_script("arguments[0].value = ''; arguments[0].dispatchEvent(new Event('input'));", search_input)
        print("🧹 Cleared the search field after closing modal.")
        time.sleep(1)
    except Exception:
        print("⚠️ Could not clear search field after closing modal.")
        time.sleep(1)

    print("\n" + "="*50)
    print("Test Case 4: Table Column Titles")
    print("="*50)
    column_checks = [
        {
            "label": "Column 1",
            "selectors": [
                (By.CSS_SELECTOR, "td:nth-child(1) div:nth-child(1) div:nth-child(1)"),
                (By.XPATH, "//div[normalize-space()='NAME']"),
                (By.XPATH, "(//div[normalize-space()='NAME'])[1]")
            ],
            "expected": "NAME"
        },
        {
            "label": "Column 2",
            "selectors": [
                (By.CSS_SELECTOR, "div[id='app'] thead[class='border bg-container z-10 sticky top-[-1px]'] td:nth-child(1)"),
                (By.XPATH, "//td[normalize-space()='AGENCY / OFFICE']"),
                (By.XPATH, "(//td[normalize-space()='AGENCY / OFFICE'])[1]")
            ],
            "expected": "AGENCY / OFFICE"
        },
        {
            "label": "Column 3",
            "selectors": [
                (By.CSS_SELECTOR, "td:nth-child(1) div:nth-child(1) div:nth-child(1)"),
                (By.XPATH, "//div[normalize-space()='ACCESS LEVEL']"),
                (By.XPATH, "(//div[normalize-space()='ACCESS LEVEL'])[1]")
            ],
            "expected": "ACCESS LEVEL"
        },
        {
            "label": "Column 4",
            "selectors": [
                (By.CSS_SELECTOR, "div[id='app'] thead[class='border bg-container z-10 sticky top-[-1px]'] td:nth-child(1)"),
                (By.XPATH, "//td[normalize-space()='EMAIL']"),
                (By.XPATH, "(//td[normalize-space()='EMAIL'])[1]")
            ],
            "expected": "EMAIL"
        }
    ]
    for col in column_checks:
        found = False
        for by, selector in col["selectors"]:
            try:
                el = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((by, selector)))
                text = el.text.strip().replace("\n", "")
                if col["expected"] in text:
                    print(f"✅ {col['label']} title matches: '{text}'")
                    found = True
                    break
            except Exception:
                continue
        if not found:
            print(f"❌ {col['label']} title not found or does not match '{col['expected']}'")

    print("\n" + "="*50)
    print("Test Case 5: Table Row Interaction & Modal Display")
    print("="*50)
    try:
        # Hover over the first row
        first_row = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "tbody tr:nth-child(1)"))
        )
        ActionChains(driver).move_to_element(first_row).perform()
        print("🖱️ Hovered over Row 1.")
        time.sleep(1)
        # Click to open modal
        driver.execute_script("arguments[0].click();", first_row)
        print("🖱️ Clicked Row 1.")
        time.sleep(2)
        # Check if modal is displayed
        modal_displayed = False
        modal_selectors = [
            (By.CSS_SELECTOR, "div[role='dialog']"),
            (By.CSS_SELECTOR, "div.bg-white[role]"),
            (By.CSS_SELECTOR, "div.bg-white"),
            (By.XPATH, "//div[contains(@class, 'modal') or contains(@class, 'Modal')]")
        ]
        for m_by, m_selector in modal_selectors:
            try:
                modal = WebDriverWait(driver, 3).until(
                    EC.visibility_of_element_located((m_by, m_selector))
                )
                modal_displayed = True
                break
            except Exception:
                continue
        if modal_displayed:
            print("✅ Modal displayed for Row 1.")
        else:
            print("❌ Modal not displayed for Row 1 after click.")
        # Try to close modal using Cancel or Close (X) button or JS
        closed = False
        try:
            cancel_btn = driver.find_element(By.XPATH, "//button[normalize-space()='Cancel']")
            driver.execute_script("arguments[0].click();", cancel_btn)
            print("🛑 Closed modal using Cancel button.")
            closed = True
        except Exception:
            try:
                close_btn = driver.find_element(By.XPATH, "//button[contains(@class, 'btn-close') or contains(@aria-label, 'Close')]")
                driver.execute_script("arguments[0].click();", close_btn)
                print("🛑 Closed modal using Close (X) button.")
                closed = True
            except Exception:
                driver.execute_script("var modal = document.querySelector('div[role=\\'dialog\\']'); if (modal) modal.remove();")
                print("🛑 Force removed modal via JS.")
                closed = True
        if not closed:
            print("⚠️ Could not close modal.")
        time.sleep(1)
    except Exception:
        print("❌ Row 1 could not be interacted with or modal not shown.")

    print("\n" + "="*50)
    print("Test Case 6: Sort Functionality by Name")
    print("="*50)
    # Only check data rows, not header
    data_rows = driver.find_elements(By.XPATH, "//tbody/tr/td[1]")
    data_order = [item.text.strip() for item in data_rows if item.text.strip()]
    print("Data order before sort:", data_order)
    time.sleep(1)

    # Descending sort (down arrow) FIRST
    down_arrow_selectors = [
        (By.CSS_SELECTOR, "td:nth-child(1) div:nth-child(1) div:nth-child(1) span:nth-child(2)"),
        (By.XPATH, "//td[1]//div[1]//div[1]//span[2]"),
        (By.XPATH, "(//span[@class='hover:text-gray-500'][contains(text(),'▼')])[1]")
    ]
    down_arrow_clicked = False
    for by, selector in down_arrow_selectors:
        try:
            down_arrow = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((by, selector)))
            driver.execute_script("arguments[0].click();", down_arrow)
            print("✅ Clicked descending sort (down arrow) button.")
            down_arrow_clicked = True
            time.sleep(1)
            break
        except Exception:
            continue
    if not down_arrow_clicked:
        print("❌ Could not find or click descending sort (down arrow) button.")
    time.sleep(3)
    descending_rows = driver.find_elements(By.XPATH, "//tbody/tr/td[1]")
    descending_order = [item.text.strip() for item in descending_rows if item.text.strip()]
    print("Data order after descending sort:", descending_order)
    if descending_order == sorted(descending_order, key=lambda x: x.lower(), reverse=True):
        print("✅ Verified descending sort order.")
    else:
        print("❌ Items are not in descending order.")
    time.sleep(1)

    # Ascending sort (up arrow) SECOND
    up_arrow_selectors = [
        (By.CSS_SELECTOR, "td:nth-child(1) div:nth-child(1) div:nth-child(1) span:nth-child(2)"),
        (By.XPATH, "//td[1]//div[1]//div[1]//span[2]"),
        (By.XPATH, "(//span[@class='hover:text-gray-500'][contains(text(),'▲')])[1]")
    ]
    up_arrow_clicked = False
    for by, selector in up_arrow_selectors:
        try:
            up_arrow = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((by, selector)))
            driver.execute_script("arguments[0].click();", up_arrow)
            print("✅ Clicked ascending sort (up arrow) button.")
            up_arrow_clicked = True
            time.sleep(1)
            break
        except Exception:
            continue
    if not up_arrow_clicked:
        print("❌ Could not find or click ascending sort (up arrow) button.")
    time.sleep(3)
    ascending_rows = driver.find_elements(By.XPATH, "//tbody/tr/td[1]")
    ascending_order = [item.text.strip() for item in ascending_rows if item.text.strip()]
    print("Data order after ascending sort:", ascending_order)
    if ascending_order == sorted(ascending_order, key=lambda x: x.lower()):
        print("✅ Verified ascending sort order.")
    else:
        print("❌ Items are not in ascending order.")
    time.sleep(1)

    print("\n" + "="*50)
    print("Test Case 7: Sort Functionality by Access Level")
    print("="*50)
    # Only check access level data rows, not header
    access_level_rows = driver.find_elements(By.XPATH, "//tbody/tr/td[3]")
    access_level_order = [item.text.strip() for item in access_level_rows if item.text.strip()]
    print("Access level order before sort:", access_level_order)
    time.sleep(1)

    # Descending sort (down arrow) FIRST
    down_arrow_selectors = [
        (By.CSS_SELECTOR, "td:nth-child(1) div:nth-child(1) div:nth-child(1) span:nth-child(2)"),
        (By.XPATH, "//td[1]//div[1]//div[1]//span[2]"),
        (By.XPATH, "(//span[@class='hover:text-gray-500'][contains(text(),'▼')])[2]")
    ]
    down_arrow_clicked = False
    for by, selector in down_arrow_selectors:
        try:
            down_arrow = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((by, selector)))
            driver.execute_script("arguments[0].click();", down_arrow)
            print("✅ Clicked descending sort (down arrow) button for Access Level.")
            down_arrow_clicked = True
            time.sleep(1)
            break
        except Exception:
            continue
    if not down_arrow_clicked:
        print("❌ Could not find or click descending sort (down arrow) button for Access Level.")
    time.sleep(3)
    descending_access_level_rows = driver.find_elements(By.XPATH, "//tbody/tr/td[3]")
    descending_access_level_order = [item.text.strip() for item in descending_access_level_rows if item.text.strip()]
    print("Access level order after descending sort:", descending_access_level_order)
    if descending_access_level_order == sorted(descending_access_level_order, key=lambda x: x.lower(), reverse=True):
        print("✅ Verified descending sort order for Access Level.")
    else:
        print("❌ Access Level items are not in descending order.")
    time.sleep(1)

    # Ascending sort (up arrow) SECOND
    up_arrow_selectors = [
        (By.CSS_SELECTOR, "td:nth-child(1) div:nth-child(1) div:nth-child(1) span:nth-child(2)"),
        (By.XPATH, "//td[1]//div[1]//div[1]//span[2]"),
        (By.XPATH, "(//span[@class='hover:text-gray-500'][contains(text(),'▲')])[2]")
    ]
    up_arrow_clicked = False
    for by, selector in up_arrow_selectors:
        try:
            up_arrow = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((by, selector)))
            driver.execute_script("arguments[0].click();", up_arrow)
            print("✅ Clicked ascending sort (up arrow) button for Access Level.")
            up_arrow_clicked = True
            time.sleep(1)
            break
        except Exception:
            continue
    if not up_arrow_clicked:
        print("❌ Could not find or click ascending sort (up arrow) button for Access Level.")
    time.sleep(3)
    ascending_access_level_rows = driver.find_elements(By.XPATH, "//tbody/tr/td[3]")
    ascending_access_level_order = [item.text.strip() for item in ascending_access_level_rows if item.text.strip()]
    print("Access level order after ascending sort:", ascending_access_level_order)
    if ascending_access_level_order == sorted(ascending_access_level_order, key=lambda x: x.lower()):
        print("✅ Verified ascending sort order for Access Level.")
    else:
        print("❌ Access Level items are not in ascending order.")
    time.sleep(1)

    print("\n" + "="*50)
    print("Test Case 8: Table Row Value Matches Modal Input")
    print("="*50)
    # Click the first row to open modal
    try:
        first_row = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "tbody tr:nth-child(1)"))
        )
        driver.execute_script("arguments[0].click();", first_row)
        print("Clicked first row to open modal.")
        time.sleep(2)

        # Check Name column
        try:
            table_name = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "tbody tr:nth-child(1) td:nth-child(1)"))
            ).text.strip()
            print(f"Table Name: '{table_name}'")
            modal_first_name = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "#usr_fname"))
            ).get_attribute("value").strip()
            modal_middle_name = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "#usr_mname"))
            ).get_attribute("value").strip()
            modal_surname = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "#usr_lname"))
            ).get_attribute("value").strip()
            modal_suffix = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "#usr_sfx"))
            ).get_attribute("value").strip()
            modal_full_name = f"{modal_surname}, {modal_first_name} {modal_middle_name} {modal_suffix}".strip()
            print(f"Modal Name: '{modal_full_name}'")
            if table_name == modal_full_name:
                print("✅ Name matches between table and modal input.")
            else:
                print("❌ Name does not match between table and modal input.")
        except Exception as e:
            print(f"❌ Error checking Name: {e}")

        # Check Agency/Office column
        try:
            table_agency = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "tbody tr:nth-child(1) td:nth-child(2)"))
            ).text.strip()
            print(f"Table Agency: '{table_agency}'")
            modal_agency = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='search']"))
            ).get_attribute("value").strip()
            print(f"Modal Agency: '{modal_agency}'")
            if table_agency == modal_agency:
                print("✅ Agency matches between table and modal input.")
            else:
                print("❌ Agency does not match between table and modal input.")
        except Exception as e:
            print(f"❌ Error checking Agency: {e}")

        # Check Access Level column
        try:
            table_access_level = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "tbody tr:nth-child(1) td:nth-child(3)"))
            ).text.strip()
            print(f"Table Access Level: '{table_access_level}'")
            # Get the selected option text using JavaScript
            access_level_select = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "#usr_level"))
            )
            modal_access_level = driver.execute_script("return arguments[0].options[arguments[0].selectedIndex].text;", access_level_select).strip()
            print(f"Modal Access Level: '{modal_access_level}'")
            if table_access_level == modal_access_level:
                print("✅ Access Level matches between table and modal input.")
            else:
                print("❌ Access Level does not match between table and modal input.")
        except Exception as e:
            print(f"❌ Error checking Access Level: {e}")

        # Check Email column
        try:
            table_email = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "tbody tr:nth-child(1) td:nth-child(4)"))
            ).text.strip()
            print(f"Table Email: '{table_email}'")
            modal_email = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "#usr_email"))
            ).get_attribute("value").strip()
            print(f"Modal Email: '{modal_email}'")
            if table_email == modal_email:
                print("✅ Email matches between table and modal input.")
            else:
                print("❌ Email does not match between table and modal input.")
        except Exception as e:
            print(f"❌ Error checking Email: {e}")

        # Close modal
        try:
            cancel_btn = driver.find_element(By.XPATH, "//button[normalize-space()='Cancel']")
            driver.execute_script("arguments[0].click();", cancel_btn)
            print("🛑 Closed modal using Cancel button.")
        except Exception:
            try:
                close_btn = driver.find_element(By.XPATH, "//button[contains(@class, 'btn-close') or contains(@aria-label, 'Close')]")
                driver.execute_script("arguments[0].click();", close_btn)
                print("🛑 Closed modal using Close (X) button.")
            except Exception:
                driver.execute_script("var modal = document.querySelector('div[role=\\'dialog\\']'); if (modal) modal.remove();")
                print("🛑 Force removed modal via JS.")
        time.sleep(1)
    except Exception as e:
        print(f"❌ Error in Table Row Value Matches Modal Input: {e}")

    print("\n" + "="*50)
    print("Test completed.")
    print("="*50)
    time.sleep(2)

finally:
    driver.quit()
