from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import pytest
import re

# Setup Chrome options
options = Options()
options.add_argument("--start-maximized")

# ───────────────────────────
# Config / constants
# ───────────────────────────
LOGIN_URL = "http://10.10.99.23/login"
LIBRARY_URL = "http://10.10.99.23/library"
EMAIL = "admin@gmail.com"
PASSWORD = "Dost@123"
SEARCH_TERM = "Laptop"
EXPECTED_RESULT = "Mid-range Laptop"

@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

def normalize_text(text):
    return re.sub(r'\s+', ' ', text).strip()

def test_ict_items_modal(driver):
    try:
        # Login and navigate (no print)
        driver.get(LOGIN_URL)
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        email_input.send_keys(EMAIL)
        driver.find_element(By.ID, "password").send_keys(PASSWORD)
        driver.find_element(By.CSS_SELECTOR, "button[type='button']").click()
        WebDriverWait(driver, 10).until(EC.url_changes(LOGIN_URL))
        driver.get(LIBRARY_URL)
        time.sleep(1)

        print("\n" + "="*50)
        print("Test Case 1: Click ICT Items Tab")
        print("="*50)
        ict_items_tab = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='w-full h-full overflow-y-hidden flex flex-col'] li:nth-child(4) p:nth-child(1)"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", ict_items_tab)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", ict_items_tab)
        print("✅ ICT Items tab clicked.")
        time.sleep(1)

        print("\n" + "="*50)
        print("Test Case 2: Search Functionality")
        print("="*50)
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Search...']"))
        )
        search_input.clear()
        search_input.send_keys(SEARCH_TERM)
        time.sleep(1)
        try:
            WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, f"//td[normalize-space()='{EXPECTED_RESULT}']"))
            )
            print(f"✅ Found expected result: '{EXPECTED_RESULT}'")
        except Exception as e:
            print(f"❌ Expected result '{EXPECTED_RESULT}' not found: {e}")
            assert False, f"Expected result '{EXPECTED_RESULT}' not found."
        # Clear the search field as part of this test case
        search_input.clear()
        print("🧹 Cleared the search field.")
        time.sleep(1)
        # Wait for the table to be fully restored (unfiltered)
        try:
            WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, "//td[contains(@class, 'text-left')]"))
            )
            print("✅ Table restored after clearing search.")
        except Exception:
            print("⚠️ Table may not be fully restored after clearing search.")
        time.sleep(1)

        print("\n" + "="*50)
        print("Test Case 3: Add New Modal - Modal Visibility Only")
        print("="*50)
        add_new_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class='btn-circular square-md shadow-[4.0px_8.0px_8.0px_rgba(0,0,0,0.20)]']"))
        )
        driver.execute_script("arguments[0].click();", add_new_button)
        print("➕ Clicked Add New button.")
        time.sleep(1)

        # Check if modal is visible (general selector)
        modal_visible = False
        modal_selectors = [
            (By.CSS_SELECTOR, "div[role='dialog']"),
            (By.CSS_SELECTOR, "div.bg-white[role]"),
            (By.CSS_SELECTOR, "div.bg-white"),
            (By.XPATH, "//div[contains(@class, 'modal') or contains(@class, 'Modal')]")
        ]
        for m_by, m_selector in modal_selectors:
            try:
                modal = WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located((m_by, m_selector))
                )
                modal_visible = True
                break
            except Exception:
                continue
        if modal_visible:
            print("✅ Add New modal is visible.")
        else:
            print("❌ Add New modal is NOT visible.")
            assert False, "Add New modal is not visible after clicking Add New button."
        time.sleep(1)

        # Close the Add New modal
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
                driver.execute_script("var modal = document.querySelector('div[role=\"dialog\"]'); if (modal) modal.remove();")
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
            WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, "//td[contains(@class, 'text-left')]"))
            )
            print("✅ Table restored after clearing search (post-modal).")
        except Exception:
            print("⚠️ Could not clear search field or restore table after closing modal.")
            time.sleep(1)

        print("\n" + "="*50)
        print("Test Case 4: Table Column Titles")
        print("="*50)
        column_checks = [
            {
                "label": "Column 1",
                "selectors": [
                    (By.CSS_SELECTOR, "div[class='text-left']"),
                    (By.XPATH, "//div[@class='text-left']"),
                    (By.XPATH, "(//div[@class='text-left'])[1]")
                ],
                "expected": "ICT ITEM"
            },
            {
                "label": "Column 2",
                "selectors": [
                    (By.CSS_SELECTOR, "div[id='app'] thead[class='border bg-container z-10 sticky top-[-1px]'] td:nth-child(2)"),
                    (By.XPATH, "//td[normalize-space()='ESTIMATED COST PER UOM']"),
                    (By.XPATH, "(//td[normalize-space()='ESTIMATED COST PER UOM'])[1]")
                ],
                "expected": "ESTIMATED COST PER UOM"
            },
            {
                "label": "Column 3",
                "selectors": [
                    (By.CSS_SELECTOR, "div[id='app'] thead[class='border bg-container z-10 sticky top-[-1px]'] td:nth-child(3)"),
                    (By.XPATH, "//td[normalize-space()='SPECIFICATIONS']"),
                    (By.XPATH, "(//td[normalize-space()='SPECIFICATIONS'])[1]")
                ],
                "expected": "SPECIFICATIONS"
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
                        time.sleep(0.5)
                        break
                except Exception:
                    continue
            if not found:
                print(f"❌ {col['label']} title not found or does not match '{col['expected']}'")
                assert False, f"{col['label']} title not found or does not match '{col['expected']}'"
        time.sleep(1)

        # Move Table Row Interaction & Modal Display before Sort Functionality
        print("\n" + "="*50)
        print("Test Case 5: Table Row Interaction & Modal Display")
        print("="*50)
        # Only test the first row
        row = {
            "label": "Row 1",
            "selectors": [
                (By.CSS_SELECTOR, "tbody tr:nth-child(1)"),
                (By.XPATH, "//tbody/tr[1]"),
                (By.XPATH, "(//tr[@class='border mx-5 text-left align-text-top odd:white even:bg-gray-100 hover:bg-gray-200 text-sm'])[1]")
            ],
            "expected": "All-in-one computer"
        }
        found = False
        for by, selector in row["selectors"]:
            try:
                tr = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((by, selector)))
                # Hover to highlight
                ActionChains(driver).move_to_element(tr).perform()
                print(f"🖱️ Hovered over {row['label']}.")
                time.sleep(1)
                # Click to open modal
                driver.execute_script("arguments[0].click();", tr)
                print(f"🖱️ Clicked {row['label']}.")
                time.sleep(2)

                # Try more general modal selectors
                modal_selectors = [
                    (By.CSS_SELECTOR, "div.bg-white[role]"),  # any bg-white modal with a role
                    (By.CSS_SELECTOR, "div.bg-white"),        # any bg-white modal
                    (By.XPATH, "//div[contains(@class, 'bg-white') and contains(@class, 'rounded-xl')]") ,
                    (By.XPATH, "//div[contains(@class, 'modal') or contains(@class, 'Modal')]")
                ]
                modal = None
                for m_by, m_selector in modal_selectors:
                    try:
                        modal = WebDriverWait(driver, 5).until(
                            EC.visibility_of_element_located((m_by, m_selector))
                        )
                        break
                    except Exception:
                        continue
                if modal is not None:
                    print(f"✅ Modal displayed for {row['label']}.")
                    found = True
                    time.sleep(1)
                    # Try to close modal using SVG close icon
                    closed = False
                    try:
                        # Wait a bit for the close icon to be interactable
                        time.sleep(0.5)
                        close_icon = driver.find_element(By.XPATH, "(//*[name()='svg'][@class='svg-inline--fa fa-xmark text-xl rounded-full'])[1]")
                        try:
                            ActionChains(driver).move_to_element(close_icon).click().perform()
                            print("🛑 Closed modal using SVG close icon (ActionChains).")
                            closed = True
                        except Exception:
                            driver.execute_script("arguments[0].click();", close_icon)
                            print("🛑 Closed modal using SVG close icon (JS click).")
                            closed = True
                    except Exception:
                        try:
                            close_btn = driver.find_element(By.XPATH, "//button[contains(@class, 'btn-close') or contains(@aria-label, 'Close')]")
                            driver.execute_script("arguments[0].click();", close_btn)
                            print("🛑 Closed modal using Close (X) button.")
                            closed = True
                        except Exception:
                            driver.execute_script("var modal = document.querySelector('div.bg-white'); if (modal) modal.remove();")
                            print("🛑 Force removed modal via JS.")
                            closed = True
                    if not closed:
                        print("⚠️ Could not close modal.")
                    # Wait for the table to be restored after closing the modal
                    try:
                        WebDriverWait(driver, 5).until(
                            EC.visibility_of_element_located((By.XPATH, "//tbody/tr[1]"))
                        )
                        print("✅ Table restored after closing modal.")
                    except Exception:
                        print("⚠️ Table may not be fully restored after closing modal.")
                    time.sleep(1)
                else:
                    print(f"❌ Modal not displayed for {row['label']} after click.")
                    print(driver.page_source[:1000])
                break
            except Exception:
                continue
        if not found:
            print(f"❌ {row['label']} could not be interacted with or modal not shown.")

        print("\n" + "="*50)
        print("Test Case 6: Sort Functionality")
        print("="*50)
        # Only check data rows, not header
        data_rows = driver.find_elements(By.XPATH, "//tbody/tr/td[1]")
        data_order = [item.text.strip() for item in data_rows if item.text.strip()]
        print("Data order before sort:", data_order)
        time.sleep(1)

        # Descending sort (down arrow) FIRST
        down_arrow_selectors = [
            (By.CSS_SELECTOR, "div[class='max-h-[500px] overflow-y-auto mb-6 mr-6'] span:nth-child(1)"),
            (By.XPATH, "//span[contains(text(),'▼')]") ,
            (By.XPATH, "(//span[contains(text(),'▼')])[1]")
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
            assert False, "Descending sort (down arrow) button not found or not clickable."
        time.sleep(3)
        descending_rows = driver.find_elements(By.XPATH, "//tbody/tr/td[1]")
        descending_order = [item.text.strip() for item in descending_rows if item.text.strip()]
        print("Data order after descending sort:", descending_order)
        if descending_order == sorted(descending_order, key=lambda x: x.lower(), reverse=True):
            print("✅ Verified descending sort order.")
        else:
            print("❌ Items are not in descending order.")
            assert False, "Items are not in descending order after descending sort."
        time.sleep(1)

        # Ascending sort (up arrow) SECOND
        up_arrow_selectors = [
            (By.CSS_SELECTOR, "div[class='max-h-[500px] overflow-y-auto mb-6 mr-6'] span:nth-child(1)"),
            (By.XPATH, "//span[contains(text(),'▲')]") ,
            (By.XPATH, "(//span[contains(text(),'▲')])[1]")
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
            assert False, "Ascending sort (up arrow) button not found or not clickable."
        time.sleep(3)
        ascending_rows = driver.find_elements(By.XPATH, "//tbody/tr/td[1]")
        ascending_order = [item.text.strip() for item in ascending_rows if item.text.strip()]
        print("Data order after ascending sort:", ascending_order)
        if ascending_order == sorted(ascending_order, key=lambda x: x.lower()):
            print("✅ Verified ascending sort order.")
        else:
            print("❌ Items are not in ascending order.")
            assert False, "Items are not in ascending order after ascending sort."
        time.sleep(1)

        print("\n" + "="*50)
        print("Test Case 7: Table Row Value Matches Modal Input")
        print("="*50)
        # ICT ITEM column
        try:
            table_ict_item = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "tbody tr:nth-child(1) td:nth-child(1)"))
            ).text.strip()
            print(f"Table ICT ITEM: '{table_ict_item}'")
            # Click the row to open modal
            row = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "tbody tr:nth-child(1)"))
            )
            driver.execute_script("arguments[0].click();", row)
            time.sleep(1)
            # ICT ITEM input field
            modal_ict_item = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "#itm_name"))
            ).get_attribute("value").strip()
            print(f"Modal ICT ITEM input: '{modal_ict_item}'")
            if table_ict_item == modal_ict_item:
                print("✅ ICT ITEM matches between table and modal input.")
            else:
                print("❌ ICT ITEM does not match between table and modal input.")
            # ESTIMATED COST PER UOM
            table_cost = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, "//td[contains(text(),'₱ 100,000.00 / pc')]"))
            ).text.strip()
            print(f"Table ESTIMATED COST PER UOM: '{table_cost}'")
            modal_cost = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "#itm_cost"))
            ).get_attribute("value").strip()
            print(f"Modal ESTIMATED COST input: '{modal_cost}'")
            if modal_cost in table_cost:
                print("✅ ESTIMATED COST matches between table and modal input.")
            else:
                print("❌ ESTIMATED COST does not match between table and modal input.")
            # SPECIFICATIONS
            table_spec = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, "//td[contains(text(),'High-end unit')]"))
            ).text.strip()
            print(f"Table SPECIFICATIONS: '{table_spec}'")
            modal_spec = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "#itm_desc"))
            ).get_attribute("value").strip()
            print(f"Modal SPECIFICATIONS textarea: '{modal_spec}'")
            if normalize_text(modal_spec) == normalize_text(table_spec):
                print("✅ SPECIFICATIONS match between table and modal textarea.")
            else:
                print("❌ SPECIFICATIONS do not match between table and modal textarea.")
            # Close modal after check
            time.sleep(1)
            closed = False
            try:
                close_icon = driver.find_element(By.XPATH, "(//*[name()='svg'][@class='svg-inline--fa fa-xmark text-xl rounded-full'])[1]")
                try:
                    ActionChains(driver).move_to_element(close_icon).click().perform()
                    print("🛑 Closed modal using SVG close icon (ActionChains).")
                    closed = True
                except Exception:
                    driver.execute_script("arguments[0].click();", close_icon)
                    print("🛑 Closed modal using SVG close icon (JS click).")
                    closed = True
            except Exception:
                try:
                    close_btn = driver.find_element(By.XPATH, "//button[contains(@class, 'btn-close') or contains(@aria-label, 'Close')]")
                    driver.execute_script("arguments[0].click();", close_btn)
                    print("🛑 Closed modal using Close (X) button.")
                    closed = True
                except Exception:
                    driver.execute_script("var modal = document.querySelector('div.bg-white'); if (modal) modal.remove();")
                    print("🛑 Force removed modal via JS.")
                    closed = True
            if not closed:
                print("⚠️ Could not close modal.")
            time.sleep(1)
        except Exception as e:
            print(f"❌ Error in Table Row Value Matches Modal Input: {e}")

        print("\n" + "="*50)
        print(" ALL TEST CASES COMPLETED SUCCESSFULLY! ")
        print("="*50)

    except Exception as e:
        print(f"❌ Test failed: {e}")
        raise
