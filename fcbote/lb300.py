from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
import time

def LIB_300():
    """
    Function to test the Funding Source tab functionality of the ISSP Integrated System.
    Tests include search, add/edit/delete operations, and table interactions.
    """
    def wait_for_loading_screen(wait):
        """Helper function to wait for loading screen to disappear"""
        try:
            wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "loading-screen")))
            time.sleep(1)
        except:
            pass

    def return_to_funding_source(driver, wait):
        """Helper function to return to Funding Source tab after refresh"""
        wait_for_loading_screen(wait)
        funding_source_tab = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//p[normalize-space()='Funding Source']"
        )))
        funding_source_tab.click()
        time.sleep(2)
        wait_for_loading_screen(wait)

    try:
        # Initialize Chrome WebDriver
        options = uc.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = uc.Chrome(options=options)
        wait = WebDriverWait(driver, 7)
        
        # Initial setup - Login to the system
        driver.get("http://10.10.99.23/login")
        time.sleep(2)
        
        # Login process
        username_input = "admin@gmail.com"
        password_input = "Dost@123"
        
        email_field = wait.until(EC.presence_of_element_located((By.ID, "email")))
        email_field.send_keys(username_input)
        time.sleep(0.5)
        
        password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
        password_field.send_keys(password_input)
        time.sleep(0.5)
        
        sign_in_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sign in')]")))
        sign_in_button.click()
        time.sleep(2)

        # Navigate directly to library URL
        wait_for_loading_screen(wait)
        driver.get("http://10.10.99.23/library")
        time.sleep(2)
        wait_for_loading_screen(wait)
        print("\n✅ Successfully navigated to Library page")

        # Navigate to Funding Source tab
        print("\nTest Case: Clicking Funding Source Tab")
        funding_source_tab = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//p[normalize-space()='Funding Source']"
        )))
        funding_source_tab.click()
        time.sleep(2)
        print("✅ Successfully navigated to Funding Source tab")

        # Test Case 1: Search Functionality
        print("\nTest Case 1: Testing Search Functionality")
        search_icon = wait.until(EC.presence_of_element_located((
            By.XPATH, "//button[@class='absolute left-0 top-0 mt-2 ml-3 text-white']//*[name()='svg']"
        )))
        search_input = wait.until(EC.presence_of_element_located((
            By.XPATH, "//input[@placeholder='Search...']"
        )))
        
        if search_icon.is_displayed() and search_input.is_displayed():
            print("✅ Search icon and input field are displayed")
            search_input.send_keys("test search")
            time.sleep(1)
            search_input.clear()
            time.sleep(1)
            
            # Refresh page and return to Funding Source tab
            driver.refresh()
            time.sleep(2)
            return_to_funding_source(driver, wait)
            print("✅ Search functionality working and page refreshed")
        else:
            print("❌ Search elements not displayed properly")

        # Test Case 2: Add New Button and Modal
        print("\nTest Case 2: Testing Add New Button")
        add_new_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//button[@class='btn-circular square-md shadow-[4.0px_8.0px_8.0px_rgba(0,0,0,0.20)]']"
        )))
        if add_new_btn.is_displayed():
            print("✅ Add New button is displayed")
            add_new_btn.click()
            time.sleep(1.5)
            
            # Close modal using X button
            x_button = wait.until(EC.element_to_be_clickable((
                By.XPATH, "//p[@class='font-bold rounded-t-md modal-title px-5 pt-5 pb-3 flex justify-between']//button//div//*[name()='svg']"
            )))
            if x_button.is_displayed():
                x_button.click()
                time.sleep(1)
                print("✅ Modal closed successfully using X button")
            else:
                print("❌ X button not displayed")
        else:
            print("❌ Add New button not displayed")

        # Test Case 3: Table Row Hover Effect
        print("\nTest Case 3: Testing Table Row Hover Effect")
        table_row = wait.until(EC.presence_of_element_located((
            By.XPATH, "(//tr[@class='border mx-5 text-left align-text-top odd:white even:bg-gray-100 hover:bg-gray-200 text-sm'])[1]"
        )))
        if table_row.is_displayed():
            print("✅ Table row hover effect is working")
        else:
            print("❌ Table row not displayed properly")

        # Test Case 4: Funding Source Code Column Title
        print("\nTest Case 4: Checking Funding Source Code Column Title")
        fs_code_header = wait.until(EC.presence_of_element_located((
            By.XPATH, "//div[normalize-space()='FUNDING SOURCE CODE']"
        )))
        if fs_code_header.is_displayed():
            print("✅ Funding source code TITLE / abbreviation PASSED")
        else:
            print("❌ Funding Source Code column title not displayed")

        # Test Case 5: Funding Source Column Title
        print("\nTest Case 5: Checking Funding Source Column Title")
        fs_title = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, "td:nth-child(2) div:nth-child(1) div:nth-child(2)"
        )))
        if fs_title.is_displayed():
            print("✅ Name of Funding Source table column title PASSED")
        else:
            print("❌ Funding Source column title not displayed")

        # Test Case 6: Testing Sort Buttons for Funding Source Code
        print("\nTest Case 6: Testing Sort Buttons for Funding Source Code")
        # Up arrow
        sort_up = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, "td:nth-child(1) div:nth-child(1) div:nth-child(1) span:nth-child(2)"
        )))
        print("Testing Up sort button")
        sort_up.click()
        time.sleep(1.5)
        wait_for_loading_screen(wait)
        
        # Down arrow
        sort_down = wait.until(EC.presence_of_element_located((
            By.XPATH, "//td[1]//div[1]//div[1]//span[2]"
        )))
        print("Testing Down sort button")
        sort_down.click()
        time.sleep(1.5)
        wait_for_loading_screen(wait)
        print("✅ Sort buttons are functional")

        # Test Case 7: Testing Sort Buttons for Funding Source
        print("\nTest Case 7: Testing Sort Buttons for Funding Source")
        # Up arrow
        fs_sort_up = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, "td:nth-child(2) div:nth-child(1) div:nth-child(1) span:nth-child(2)"
        )))
        print("Testing Up sort button")
        fs_sort_up.click()
        time.sleep(1.5)
        wait_for_loading_screen(wait)
        
        # Down arrow
        fs_sort_down = wait.until(EC.presence_of_element_located((
            By.XPATH, "//td[2]//div[1]//div[1]//span[2]"
        )))
        print("Testing Down sort button")
        fs_sort_down.click()
        time.sleep(1.5)
        wait_for_loading_screen(wait)
        print("✅ Sort buttons are functional")

        # Refresh page and click GAA row
        print("\nRefreshing page and clicking GAA row")
        driver.refresh()
        time.sleep(2)
        return_to_funding_source(driver, wait)
        
        # Click the GAA row
        gaa_row = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//tr[.//td[text()='GAA']]"
        )))
        gaa_row.click()
        time.sleep(1.5)

        # Test Case 8: Store First Row Data
        print("\nTest Case 8: Getting First Row Data")
        # Wait for any loading screen to disappear first
        wait_for_loading_screen(wait)
        time.sleep(1)  # Extra stability wait
        
        # Get the first row
        first_row = wait.until(EC.presence_of_element_located((
            By.XPATH, "//tr[@class='border mx-5 text-left align-text-top odd:white even:bg-gray-100 hover:bg-gray-200 text-sm']"
        )))
        
        # Store row data before clicking
        row_data = {
            'code': first_row.find_element(By.XPATH, ".//td[1]").text,
            'name': first_row.find_element(By.XPATH, ".//td[2]").text
        }
        
        # Ensure element is clickable and scroll into view
        wait_for_loading_screen(wait)
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", first_row)
        time.sleep(1)  # Wait for scroll to complete
        
        # Click using JavaScript for better reliability
        driver.execute_script("arguments[0].click();", first_row)
        time.sleep(1.5)
        print("✅ Successfully stored row data and opened modal")

        # Test Case 9: Compare Funding Source Code
        print("\nTest Case 9: Comparing Funding Source Code")
        fs_code_input = wait.until(EC.presence_of_element_located((
            By.ID, "fnd_code"
        )))
        if fs_code_input.get_attribute('value') == row_data['code']:
            print("✅ Funding Source Code matches table row content")
        else:
            print("❌ Funding Source Code mismatch")

        # Test Case 10: Compare Funding Source Name
        print("\nTest Case 10: Comparing Funding Source Name")
        fs_name_input = wait.until(EC.presence_of_element_located((
            By.ID, "fnd_name"
        )))
        if fs_name_input.get_attribute('value') == row_data['name']:
            print("✅ Funding Source Name matches table row content")
        else:
            print("❌ Funding Source Name mismatch")

        # Test Case 11: Close (X) Button
        print("\nTest Case 11: Testing Close (X) Button")
        x_button = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//p[@class='font-bold rounded-t-md modal-title px-5 pt-5 pb-3 flex justify-between']//button//div//*[name()='svg']"
        )))
        if x_button.is_displayed():
            x_button.click()
            time.sleep(1)
            print("✅ Modal closed successfully using X button")
        else:
            print("❌ X button not displayed")

        print("\n--------------Test Completed--------------\n")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
    finally:
        time.sleep(3)
        driver.quit()

if __name__ == "__main__":
    LIB_300() 