from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException
import time

  
# Login function
def login(driver):

    try:

        wait = WebDriverWait(driver, 10)
            
        username_input = "admin@gmail.com"
        password_input = "Dost@123"

        time.sleep(1)
        username_field = wait.until(EC.presence_of_element_located((By.ID,"username")))
        username_field.send_keys(username_input)

        time.sleep(1)
        password_field = wait.until(EC.presence_of_element_located((By.ID,"password")))
        password_field.send_keys(password_input)

        time.sleep(1)
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sign in')]")))
        login_button.click()

    except ElementNotInteractableException as e:

        print(f"Element not interactable: {e}")