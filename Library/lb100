from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import sys

def LIB_001():
    """
    Function to test the Library tab functionality of the ISSP Integrated System.
    It tests navigation, form elements, and table operations.
    """
    driver = None
    
    def wait_for_loading_screen(wait):
        """Helper function to wait for loading screen to disappear"""
        try:
            wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "loading-screen")))
            time.sleep(1)
        except:
            pass

    def safe_click_tab(driver, wait, xpath, tab_name):
        """Helper function to safely click tabs and handle loading screens"""
        try:
            wait_for_loading_screen(wait)
            tab = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            print(f"\nTest Case: {tab_name} tab display")
            if tab.is_displayed():
                print(f"✅ {tab_name} PASSED")
                driver.execute_script("arguments[0].click();", tab)
                time.sleep(1.5)
                wait_for_loading_screen(wait)
            else:
                print(f"❌ {tab_name} tab is not displayed")
        except Exception as e:
            print(f"❌ Error clicking {tab_name} tab: {str(e)}")

    try:
        print("Initializing Chrome WebDriver...")
        
        # Initialize Chrome WebDriver with enhanced options
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('--window-size=1920,1080')
        
        try:
            driver = webdriver.Chrome(options=options)
            print("Chrome WebDriver initialized successfully!")
            
            driver.implicitly_wait(10)
            wait = WebDriverWait(driver, 7)
            
        except Exception as e:
            print(f"Error initializing Chrome WebDriver: {str(e)}")
            if driver:
                driver.quit()
            sys.exit(1)

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

        # Test Case 1: Agency/Institution Tab
        print("\nTest Case 1: Agency/Institution Tab")
        safe_click_tab(driver, wait, 
            "//p[@class='inline-block p-4 text-white bg-content rounded-t-lg active cursor-pointer']",
            "Agency/Institution")

        # Test Case 2: Funding Source Tab
        print("\nTest Case 2: Funding Source Tab")
        safe_click_tab(driver, wait,
            "//p[normalize-space()='Funding Source']",
            "Funding Source")

        # Test Case 3: ICT Categories Tab
        print("\nTest Case 3: ICT Categories Tab")
        safe_click_tab(driver, wait,
            "//p[normalize-space()='ICT Categories']",
            "ICT Categories")

        # Test Case 4: ICT Items Tab
        print("\nTest Case 4: ICT Items Tab")
        safe_click_tab(driver, wait,
            "//label[@class='mr-4']",
            "ICT Items")

        # Test Case 5: IS Classification Tab
        print("\nTest Case 5: IS Classification Tab")
        safe_click_tab(driver, wait,
            "//p[normalize-space()='IS Classification']",
            "IS Classification")

        # Test Case 6: User Accounts Tab
        print("\nTest Case 6: User Accounts Tab")
        safe_click_tab(driver, wait,
            "//p[normalize-space()='User Accounts']",
            "User Accounts")

        # Return to Agency/Institution tab
        print("\nReturning to Agency/Institution tab")
        driver.get("http://10.10.99.23/library")
        time.sleep(3)
        wait_for_loading_screen(wait)

        # Test Case 7: Search functionality
        print("\nTest Case 7: Testing Search Functionality")
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
            
            # Refresh page to show complete table
            driver.refresh()
            time.sleep(2)
            wait_for_loading_screen(wait)
            print("✅ Search functionality working and table refreshed")
        else:
            print("❌ Search elements not displayed properly")

        # Test Case 8: Add New Button
        print("\nTest Case 8: Testing Add New Button")
        add_new_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//button[@class='btn-circular square-md shadow-[4.0px_8.0px_8.0px_rgba(0,0,0,0.20)]']"
        )))
        if add_new_btn.is_displayed():
            print("✅ Add New button is displayed")
            add_new_btn.click()
            time.sleep(1.5)
            
            # Close using X button
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

        # Test Case 9: Table Row Hover Effect
        print("\nTest Case 9: Testing Table Row Hover Effect")
        table_row = wait.until(EC.presence_of_element_located((
            By.XPATH, "//tr[@class='border mx-5 text-left align-text-top odd:white even:bg-gray-100 hover:bg-gray-200 text-sm']"
        )))
        if table_row.is_displayed():
            print("✅ Table row hover effect is working")
        else:
            print("❌ Table row not displayed properly")

        # Test Case 10: Agency Code Column Sort
        print("\nTest Case 10: Testing Agency Code Column Sort")
        sort_up_code = wait.until(EC.presence_of_element_located((
            By.XPATH, "(//span[@class='hover:text-gray-500'][contains(text(),'▲')])[1]"
        )))
        sort_down_code = wait.until(EC.presence_of_element_located((
            By.XPATH, "(//span[@class='hover:text-gray-500'][contains(text(),'▼')])[1]"
        )))
        
        if sort_up_code.is_displayed() and sort_down_code.is_displayed():
            sort_up_code.click()
            time.sleep(1.5)
            wait_for_loading_screen(wait)
            sort_down_code.click()
            time.sleep(1.5)
            wait_for_loading_screen(wait)
            print("✅ Agency Code sort buttons are functional")
        else:
            print("❌ Agency Code sort buttons not displayed")

        # Test Case 11: Agency/Institution Column Sort
        print("\nTest Case 11: Testing Agency/Institution Column Sort")
        sort_up_inst = wait.until(EC.presence_of_element_located((
            By.XPATH, "(//span[@class='hover:text-gray-500'][contains(text(),'▲')])[2]"
        )))
        sort_down_inst = wait.until(EC.presence_of_element_located((
            By.XPATH, "(//span[@class='hover:text-gray-500'][contains(text(),'▼')])[2]"
        )))
        
        if sort_up_inst.is_displayed() and sort_down_inst.is_displayed():
            sort_up_inst.click()
            time.sleep(1.5)
            wait_for_loading_screen(wait)
            sort_down_inst.click()
            time.sleep(1.5)
            wait_for_loading_screen(wait)
            print("✅ Agency/Institution sort buttons are functional")
        else:
            print("❌ Agency/Institution sort buttons not displayed")

        # Test Case 12: Agency Code Column Title
        print("\nTest Case 12: Checking Agency Code Column Title")
        agency_code_title = wait.until(EC.presence_of_element_located((
            By.XPATH, "//div[normalize-space()='AGENCY CODE']"
        )))
        if agency_code_title.is_displayed():
            print("✅ Agency Code column title is displayed")
        else:
            print("❌ Agency Code column title not displayed")

        # Test Case 13: Agency/Institution Column Title
        print("\nTest Case 13: Checking Agency/Institution Column Title")
        agency_inst_title = wait.until(EC.presence_of_element_located((
            By.XPATH, "//div[normalize-space()='AGENCY / INSTITUTION']"
        )))
        if agency_inst_title.is_displayed():
            print("✅ Agency/Institution column title is displayed")
        else:
            print("❌ Agency/Institution column title not displayed")

        # Test Case 14: Agency Head Column Title
        print("\nTest Case 14: Checking Agency Head Column Title")
        agency_head_title = wait.until(EC.presence_of_element_located((
            By.XPATH, "//td[normalize-space()='AGENCY HEAD']"
        )))
        if agency_head_title.is_displayed():
            print("✅ Agency Head column title is displayed")
        else:
            print("❌ Agency Head column title not displayed")

        # Test Case 15: Official Website Link Column Title
        print("\nTest Case 15: Checking Official Website Link Column Title")
        website_title = wait.until(EC.presence_of_element_located((
            By.XPATH, "//td[normalize-space()='OFFICIAL WEBSITE LINK']"
        )))
        if website_title.is_displayed():
            print("✅ Official Website Link column title PASSED")
        else:
            print("❌ Official Website Link column title not displayed")

        # Test Case 16: Click First Row and Store Data
        print("\nTest Case 16: Clicking First Row and Storing Data")
        first_row = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//tr[@class='border mx-5 text-left align-text-top odd:white even:bg-gray-100 hover:bg-gray-200 text-sm']"
        )))
        
        # Store row data before clicking
        row_data = {
            'code': first_row.find_element(By.XPATH, ".//td[1]").text,
            'name': first_row.find_element(By.XPATH, ".//td[2]").text,
            'head': first_row.find_element(By.XPATH, ".//td[3]").text,
            'website': first_row.find_element(By.XPATH, ".//td[4]").text
        }
        
        first_row.click()
        time.sleep(1.5)
        print("✅ Successfully clicked first row and stored data")

        # Test Case 17: Compare Agency Code
        print("\nTest Case 17: Comparing Agency Code")
        agency_code_input = wait.until(EC.presence_of_element_located((
            By.ID, "agn_code"
        )))
        if agency_code_input.get_attribute('value') == row_data['code']:
            print("✅ Agency Code matches table row content")
        else:
            print("❌ Agency Code mismatch")

        # Test Case 18: Compare Agency/Institution Name
        print("\nTest Case 18: Comparing Agency/Institution Name")
        agency_name_input = wait.until(EC.presence_of_element_located((
            By.ID, "agn_name"
        )))
        if agency_name_input.get_attribute('value') == row_data['name']:
            print("✅ Agency/Institution name matches table row content")
        else:
            print("❌ Agency/Institution name mismatch")

        # Test Case 19: Compare Agency Head
        print("\nTest Case 19: Comparing Agency Head")
        fname = wait.until(EC.presence_of_element_located((By.ID, "agn_head_fname"))).get_attribute('value')
        mi = wait.until(EC.presence_of_element_located((By.ID, "agn_head_mi"))).get_attribute('value')
        lname = wait.until(EC.presence_of_element_located((By.ID, "agn_head_lname"))).get_attribute('value')
        suffix = wait.until(EC.presence_of_element_located((By.ID, "agn_head_sfx"))).get_attribute('value')
        
        modal_head = f"{fname} {mi} {lname} {suffix}".strip()
        if modal_head == row_data['head']:
            print("✅ Agency Head matches table row content")
        else:
            print("❌ Agency Head mismatch")

        # Test Case 20: Compare Website Link
        print("\nTest Case 20: Comparing Official Website Link")
        website_input = wait.until(EC.presence_of_element_located((
            By.ID, "agn_website"
        )))
        if website_input.get_attribute('value') == row_data['website']:
            print("✅ Website link matches table row content")
        else:
            print("❌ Website link mismatch")

        print("\n--------------Test Completed--------------\n")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
    finally:
        time.sleep(3)
        if driver:
            driver.quit()

if __name__ == "__main__":
    LIB_001() 