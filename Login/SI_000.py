from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def SI_000(driver):
    """
    Function to test the login page of the ISSP Integrated System.
    It checks for banners, logos, labels, input fields, links, and error messages.
    """
    try:

        wait = WebDriverWait(driver, 10)

        time.sleep(3)
        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[-1])

        username_input = "admin@gmail.com"
        password_input = "Dost@123"


        # Test Case 1: Check for "REPUBLIC OF THE PHILIPPINES"
        time.sleep(1)
        header_1 = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'header_t1')))
        banner = header_1.text.strip()

        print(f"\nTest Case 1 : View system banner : System display correct banner, REPUBLIC OF THE PHILIPPINES")

        if banner == "REPUBLIC OF THE PHILIPPINES":
            print(f"✅ Passed : {banner}")
        elif banner == "":
            print(f"❌ Banner not found")
        else:
            print(f"❌ Incorrect banner display : {banner}")


        # Test Case 2: Check for "DEPARTMENT OF SCIENCE AND TECHNOLOGY"
        time.sleep(1)
        header_2 = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'header_t2')))
        banner = header_2.text.strip()

        print(f"\nTest Case 2 : View system banner : System display correct banner, DEPARTMENT OF SCIENCE AND TECHNOLOGY")

        if banner == "DEPARTMENT OF SCIENCE AND TECHNOLOGY":
            print(f"✅ Passed : {banner}")
        elif banner == "":
            print(f"❌ Banner not found")
        else:
            print(f"❌ Incorrect banner display : {banner}")


        # Test Case 3: Check for the presence of the DOST Logo
        time.sleep(1)
        logo_img = wait.until(EC.presence_of_element_located((By.XPATH, "//img[contains(@src, 'dost_logo.png')]")))
        logo_img.is_displayed()

        print(f"\nTest Case 3 : View agency logo : System display correct logo, DOST Logo")

        if logo_img.is_displayed():
            print(f"✅ Passed")
        else:
            print(f"❌ DOST Logo not found")


        # Test Case 4: Check for the presence of the Bagong Pilipinas Logo
        time.sleep(1)
        logo_img = wait.until(EC.presence_of_element_located((By.XPATH, "//img[contains(@src, 'bagong_pilipinas.png')]")))
        logo_img.is_displayed()

        print(f"\nTest Case 4 : View Bagong Pilipinas Logo : System display correct logo, Bagong Pilipinas Logo")

        if logo_img.is_displayed():
            print(f"✅ Passed")
        else:
            print(f"❌ Bagong Pilipinas Logo not found")


        # Test Case 5: Check for system name 'ISSP Integrated System'
        time.sleep(1)
        system_name = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'sys_title')))
        system_name = system_name.text.strip()

        print(f"\nTest Case 5 : View system name : System display correct system name, ISSP Integrated System")

        if system_name == "ISSP Integrated System":
            print(f"✅ Passed : {system_name}")
        elif system_name == "":
            print(f"❌ System name not found")
        else:
            print(f"❌ Incorrect system name display : {system_name}")


        # Test Case 6: Check for login form name
        time.sleep(1)
        login_form = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'login-lbl')))
        login_form = login_form.text.strip()

        print(f"\nTest Case 6 : View login form name : Sysem display correct login form name, Sign In")

        if login_form == "Sign In":
            print(f"✅ Passed : {login_form}")
        elif login_form == "":
            print(f"❌ Login form name not found")
        else:
            print(f"❌ Incorrect login form name display : {login_form}")


        # Test Case 7: Check for label name 'Email Address'
        time.sleep(1)
        lbl_email_address = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[1]/div[1]/div[3]/form/div[2]/label/span')))
        lbl_email_address = lbl_email_address.text.strip()

        print(f"\nTest Case 7 : View label name : System display correct label name, Email Address")

        if lbl_email_address == "Email Address":
            print(f"✅ Passed : {lbl_email_address}")
        elif lbl_email_address == "":
            print(f"❌ Label name not found")
        else:
            print(f"❌ Incorrect Label name display : {lbl_email_address}")


        # Test Case 8: Check for label name 'Password'
        time.sleep(1)
        lbl_password = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[1]/div[1]/div[3]/form/div[3]/label/span')))
        lbl_password = lbl_password.text.strip()

        print(f"\nTest Case 8 : View label name : System display correct label name, Password")

        if lbl_password == "Password":
            print(f"✅ Passed : {lbl_password}")
        elif lbl_password == "":
            print(f"❌ Label name not found")
        else:
            print(f"❌ Incorrect Label name display : {lbl_password}")


        # Test Case 9: Check for label name 'Remember me'
        time.sleep(1)
        lbl_remember_me = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[1]/div[1]/div[3]/form/div[4]/div/label/span[2]')))
        lbl_remember_me = lbl_remember_me.text.strip()

        print(f"\nTest Case 9 : View label name : System display correct label name, Remember me")

        if lbl_remember_me == "Remember me":
            print(f"✅ Passed : {lbl_remember_me}")
        elif lbl_remember_me == "":
            print(f"❌ Label name not found")
        else:
            print(f"❌ Incorrect Label name display : {lbl_remember_me}")


        # Test Case 10: Check for label name 'Forgot Password?'
        time.sleep(1)
        lbl_forgot_password = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[1]/div[1]/div[3]/form/div[4]/div/div/a')))
        lbl_forgot_password = lbl_forgot_password.text.strip()

        print(f"\nTest Case 10 : View label name : System display correct label name, Forgot Password?")

        if lbl_forgot_password == "Forgot Password?":
            print(f"✅ Passed : {lbl_forgot_password}")
        elif lbl_forgot_password == "":
            print(f"❌ Label name not found")
        else:
            print(f"❌ Incorrect Label name display : {lbl_forgot_password}")


        # Test Case 11: Check for button label name 'Sign in'
        time.sleep(1)
        btn_lbl_sign_in = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[1]/div[1]/div[3]/form/div[5]/button')))
        btn_lbl_sign_in = btn_lbl_sign_in.text.strip()

        print(f"\nTest Case 11 : View label name : System display correct label name, Sign in")

        if btn_lbl_sign_in == "Sign in":
            print(f"✅ Passed : {btn_lbl_sign_in}")
        elif btn_lbl_sign_in == "":
            print(f"❌ Button label name not found")
        else:
            print(f"❌ Incorrect Button label name display : {btn_lbl_sign_in}")


        # Test Case 12: Check for the presence of the DX Logo
        time.sleep(1)
        logo_img = wait.until(EC.presence_of_element_located((By.XPATH, "//img[contains(@src, 'dost_dx.png')]")))
        logo_img.is_displayed()

        print(f"\nTest Case 12 : View DX Logo : System display correct DX Logo")

        if logo_img.is_displayed():
            print(f"✅ Passed")
        else:
            print(f"❌ DX Logo not found")


        # Test Case 13: Check for the presence of the Copyright Statement
        time.sleep(1)
        copyright_statement = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[1]/div[2]/p')))
        copyright_statement = copyright_statement.text.strip()

        print(f"\nTest Case 13 : View Copyright Statment : System display correct Copyright Statement")

        if copyright_statement == "Copyright 2024 DOST. All rights reserved.":
            print(f"✅ Passed : {copyright_statement}")
        elif copyright_statement == "":
            print(f"❌ Copyright Statement not found")
        else:
            print(f"❌ Incorrect Copyright Statement display : {copyright_statement}")


        # Test Case 14: Email Input maximum length of 255 (char)
        time.sleep(1)
        email_address_input_length = "a" * 256

        email_address_field = wait.until(EC.presence_of_element_located((By.ID, "email")))
        email_address_field.send_keys(email_address_input_length)
        character_counter = len(email_address_field.get_attribute("value"))

        print(f"\nTest Case 14 : Email Address Input maximum length of 255 (char)")

        if character_counter <= 255:
            print(f"✅ Passed : {character_counter}")
        else:
            print(f"❌ Character limit must be 255 characters and below")


        # Test Case 15: Password Input maximum length of 50 (char)
        time.sleep(1)
        password_input_length = "a" * 51

        password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
        password_field.send_keys(password_input_length)
        character_counter = len(password_field.get_attribute("value"))

        print(f"\nTest Case 15 : Password Input maximum length of 50 (char)")

        if character_counter <= 50:
            print(f"✅ Passed : {character_counter}")
        else:
            print(f"❌ Character limit must be 50 characters and below")


        # Test Case 16: Invalid input email format, display error message : Please input a valid email address.
        driver.get("http://10.10.99.23/login")

        invalid_email_format = "Sed ut perspiciatis"

        time.sleep(1)
        email_address_field = wait.until(EC.presence_of_element_located((By.ID, "email")))
        email_address_field.send_keys(invalid_email_format)
        password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
        password_field.click()

        time.sleep(1)
        invalid_email_address_error_message = wait.until(EC.presence_of_element_located((By.ID, 'error_email')))
        message_text = invalid_email_address_error_message.text.strip()

        print(f"\nTest Case 16 : Input invalid email format and click Sign In: System display error message, Please input a valid email address.")

        if message_text == "Please input a valid email address.":
            print(f"✅ Passed : {message_text}")
        elif message_text == "":
            print(f"❌ Invalid Email Address error message not found")
        else:
            print(f"❌ Incorrect error message : {message_text}")


        # Test Case 17: Display Email Address error message.
        driver.get("http://10.10.99.23/login")

        time.sleep(1)
        sign_in_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[1]/div[1]/div[3]/form/div[5]/button')))
        sign_in_button.click()

        time.sleep(1)
        email_address_error_message = wait.until(EC.presence_of_element_located((By.ID, 'error_email')))
        message_text = email_address_error_message.text.strip()

        print(f"\nTest Case 17 : Input email address = empty : System display Email Address error message.")

        if message_text == "This field is required.":
            print(f"✅ Passed : {message_text}")
        elif message_text == "":
            print(f"❌ Email Address error message not found")
        else:
            print(f"❌ Incorrect error message : {message_text}")


        # Test Case 18: Display Password error message.
        time.sleep(1)
        password_error_message = wait.until(EC.presence_of_element_located((By.ID, 'error_pwd')))
        message_text = password_error_message.text.strip()

        print(f"\nTest Case 18 : Input password = empty and click Sign In: System display Password error message.")

        if message_text == "This field is required.":
            print(f"✅ Passed : {message_text}")
        elif message_text == "":
            print(f"❌ Password error message not found")
        else:
            print(f"❌ Incorrect error message : {message_text}")


        # Test Case 19: Invalid credentials error message.
        invalid_password_input = "Dost1234"

        time.sleep(1)
        email_address_field = wait.until(EC.presence_of_element_located((By.ID, "email")))
        email_address_field.send_keys(username_input)

        time.sleep(1)
        password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
        password_field.send_keys(invalid_password_input)

        time.sleep(1)
        sign_in_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[1]/div[1]/div[3]/form/div[5]/button')))
        sign_in_button.click()

        time.sleep(5)
        invalid_credentials_error_message = wait.until(EC.presence_of_element_located((By.ID, 'error_pwd')))
        message_text = invalid_credentials_error_message.text.strip()

        time.sleep(1)
        print(f"\nTest Case 19 : Input invalide credentials and click Sign In: System display Invalid credentials error message.")

        if message_text == "Invalid Email Address / Password.":
            print(f"✅ Passed : {message_text}")
        elif message_text == "":
            print(f"❌ Invalid credentials error message not found")
        else:
            print(f"❌ Incorrect error message : {message_text}")


        # Test Case 20: Eye icon toggle ON, display password characters.
        time.sleep(1)
        password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
        password_field.clear()
        password_field.send_keys(password_input)
        password_showed = password_field.get_attribute("value")

        time.sleep(1)
        eye_icon_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[1]/div[1]/div[3]/form/div[3]/div[1]/span[2]')))
        eye_icon_button.click()

        print(f"\nTest Case 20 : Click Eye icon toggle ON : System display password characters.")

        if password_showed == password_input:
            print(f"✅ Passed : {password_showed}")
        else:
            print(f"❌ Eye icon show/hide password is not functioning properly")


        # Test Case 21: Eye icon toggle OFF, hide password characters.
        time.sleep(1)
        eye_icon_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[1]/div[1]/div[3]/form/div[3]/div[1]/span[2]')))
        eye_icon_button.click()

        password_showed = password_field.get_attribute("value")

        print(f"\nTest Case 21 : Click Eye icon toggle OFF: System, hide password characters.")

        if password_showed == password_input:
            print(f"✅ Passed : {password_showed}")
        else:
            print(f"❌ Eye icon show/hide password is not functioning properly")


        # Test Case 22: Click Forgot Password link, redirects to the Forgot Password page.
        time.sleep(1)
        forgot_password_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Forgot Password?")))
        forgot_password_link.click()

        time.sleep(5)
        forgot_password_form_name = wait.until(EC.presence_of_element_located((By.XPATH, "//p[@class='mt-4 login-lbl']")))
        forgot_password_form_name = forgot_password_form_name.text.strip()

        print(f"\nTest Case 22 : Click Forgot Password link : System redirects to the Forgot Password page.")

        if forgot_password_form_name == "Forgot Password?":
            print(f"✅ Passed")
        else:
            print(f"❌ Forgot Password link did not redirect to the Forgot Password page")

        time.sleep(1)
        driver.get("http://10.10.99.23/login")


        # Test Case 23: Input credentials and click Sign In, redirects to the Dashboard page.
        time.sleep(1)
        email_address_field = wait.until(EC.presence_of_element_located((By.ID, "email")))
        email_address_field.send_keys(username_input)

        time.sleep(1)
        password_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
        password_field.send_keys(password_input)

        time.sleep(1)
        sign_in_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sign in')]")))
        sign_in_button.click()

        time.sleep(10)
        dashboard_name = wait.until(EC.presence_of_element_located((By.XPATH, "//p[@class='page-title']")))
        dashboard_name = dashboard_name.text.strip()

        print(f"\nTest Case 23 : Input valid credentials and click Sign In : System redirects to the Dashboard page.")

        if dashboard_name == "Dashboard":
            print(f"✅ Passed")
        else:
            print(f"❌ Login process did not redirect to the Dashboard page")

        print(f"\n--------------Test Completed--------------\n")

    except ElementNotInteractableException as e:

        print(f"Element not interactable: {e}")

    finally:

        # ✅ Close browser
        time.sleep(3)
        driver.quit()