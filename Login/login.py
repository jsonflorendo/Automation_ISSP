from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("http://10.10.99.23/login")
  
# Login function
def login():

    try: 
            
        username_input = "admin@gmail.com"
        password_input = "Dost@123"

        time.sleep(10)
        driver.find_element(By.ID,"username").send_keys(username_input)

        time.sleep(10)
        driver.find_element(By.ID,"password").send_keys(password_input)

        time.sleep(10)
        driver.find_element(By.XPATH, "//button[contains(text(), 'Sign in')]").click()
        print("Clicked Sign-in.")

    except Exception as e:
    
        print("Error", str(e))