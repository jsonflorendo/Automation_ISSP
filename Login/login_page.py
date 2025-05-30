from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import time

driver = webdriver.Chrome()
driver.maximize_window ()

wait = WebDriverWait(driver, 15)

time.sleep(3)
if len(driver.window_handles) > 1:
    driver.switch_to.window(driver.window_handles[-1])

driver.get("http://10.10.99.23/login")

time.sleep(1)

emailInput = "admin@gmail.com"
passwordInput = "Dost@123"

print(f"\n--- TEST CASES FOR HEADER UI ---")
# Test Case 1.1: Check for "REPUBLIC OF THE PHILIPPINES"
try:
    time.sleep(1)
    header_1 = driver.find_element(By.XPATH, "//p[normalize-space()='REPUBLIC OF THE PHILIPPINES']")
    assert header_1.text.strip() == "REPUBLIC OF THE PHILIPPINES", "Header 1 text mismatch"
    print("✅ Test Case 1.1: 'REPUBLIC OF THE PHILIPPINES' text found and matched")
except NoSuchElementException:
    print("❌ Test Case 1.1 Failed: 'REPUBLIC OF THE PHILIPPINES' element not found")
except AssertionError as e:
    print(f"❌ Test Case 1.1 Failed: {e}")

# Test Case 1.2: Check for "DEPARTMENT OF SCIENCE AND TECHNOLOGY"
try:
    time.sleep(1)
    header_2 = driver.find_element(By.XPATH, "//p[normalize-space()='DEPARTMENT OF SCIENCE AND TECHNOLOGY']")
    assert header_2.text.strip() == "DEPARTMENT OF SCIENCE AND TECHNOLOGY", "Header 2 text mismatch"
    print("✅ Test Case 1.2: 'DEPARTMENT OF SCIENCE AND TECHNOLOGY' text found and matched")
except NoSuchElementException:
    print("❌ Test Case 1.2 Failed: 'DEPARTMENT OF SCIENCE AND TECHNOLOGY' element not found")
except AssertionError as e:
    print(f"❌ Test Case 1.2 Failed: {e}")

# Test Case 1.3: Check for the presence of the DOST Image
try:
    time.sleep(1)
    logo_image = driver.find_element(By.XPATH, "//img[contains(@src, 'dost_logo.png')]")
    assert logo_image.is_displayed(), "DOST Logo image is not visible"
    print("✅ Test Case 1.3: Logo image 'dost_logo.png' found and visible")
except NoSuchElementException:
    print("❌ Test Case 1.3 Failed: Logo image 'dost_logo.png' not found")
except AssertionError as e:
    print(f"❌ Test Case 1.3 Failed: {e}")

# Test Case 1.4: Check for the presence of the Bagong Pilipinas Image
try:
    time.sleep(1)
    logo_image = driver.find_element(By.XPATH, "//img[contains(@src, 'bagong_pilipinas.png')]")
    assert logo_image.is_displayed(), "Logo image is not visible"
    print("✅ Test Case 1.4: Logo image 'bagong_pilipinas.png' found and visible")
except NoSuchElementException:
    print("❌ Test Case 1.4 Failed: Logo image 'dost_logo.png' not found")
except AssertionError as e:
    print(f"❌ Test Case 1.4 Failed: {e}")

print(f"\n--- TEST CASE FOR SYSTEM NAME ---")
# Test Case 2: Check for system name 'ISSP Integrated System'
try:
    time.sleep(1)
    system_name = driver.find_element(By.XPATH, "//p[@class='sys_title' and normalize-space()='ISSP Integrated System']")
    assert system_name.text.strip() == "ISSP Integrated System", "System name text mismatch"
    print("✅ Test Case 2: System name 'ISSP Integrated System' found and matched")
except NoSuchElementException:
    print("❌ Test Case 2 Failed: System name element not found")
except AssertionError as e:
    print(f"❌ Test Case 2 Failed: {e}")

print(f"\n--- TEST CASE FOR SIGIN FORM MODAL ---")
# Test Case 3: Check for Sign-In modal form existence
try:
    time.sleep(1)
    sign_in_modal = driver.find_element(By.XPATH, "//div[contains(@class, 'bg-white') and contains(@class, 'rounded-login-content')]//form")
    assert sign_in_modal is not None, "Sign-In form not found inside modal container"
    print("✅ Test Case 3: Sign-In modal form found successfully")
except NoSuchElementException:
    print("❌ Test Case 3 Failed: Sign-In modal form not found")
except AssertionError as e:
    print(f"❌ Test Case 3 Failed: {e}")


# Test Case 3: Check for 'Sign-In' text
try:
    time.sleep(1)
    sign_in_text = driver.find_element(By.XPATH, "//p[@class='mt-4 login-lbl' and normalize-space()='Sign In']")
    assert sign_in_text.text.strip() == "Sign In", "'Sign In' text mismatch"
    print("✅ Test Case 3: Modal Title 'Sign In' found and matched")
except NoSuchElementException:
    print("❌ Test Case 3 Failed:  Modal Title 'Sign In' not found")
except AssertionError as e:
    print(f"❌ Test Case 3 Failed: {e}")


print(f"\n--- TEST CASES FOR EMAIL ---")
# Test Case 3.1.1: Email Input maximum length of 255 (char)
email_local_part = "a" * 245
valid_email = email_local_part + "@gmail.com"

try:
    driver.find_element(By.ID, "email").clear()
    driver.find_element(By.ID, "password").clear()

    time.sleep(1)
    driver.find_element(By.ID, "email").send_keys(valid_email)
    time.sleep(1)
    driver.find_element(By.ID, "password").send_keys("SomePwd123")
    time.sleep(1)
   
    error_element = driver.find_element(By.ID, "error_email")
    error_msg = error_element.text.strip()
    assert error_msg == ""
    print("✅ Test Case 3.1.1 PASS: No error message for max-length email.")
except AssertionError as ae:
    print(f"❌ Test Case 3.1.1 FAIL: {ae}")
except Exception as e:
    print(f"❌ Test Case 3.1.1 ERROR: Unexpected issue during email max length test: {e}")


# Test Case 3.1.2: Out-of-bound: Email Input maximum length of 256 
email_local_part = "a" * 246
long_email = email_local_part + "@gmail.com"

try:
    driver.find_element(By.ID, "email").clear()
    driver.find_element(By.ID, "password").clear()

    time.sleep(1)
    driver.find_element(By.ID, "email").send_keys(long_email)
    time.sleep(1)
    actual_email = driver.find_element(By.ID, "email").get_attribute("value")
    assert actual_email != long_email  # truncated
    print("✅ Test Case 3.1.2 PASS: Email input exceeded maxlength (out-of-bound) and was truncated correctly.")
except AssertionError:
    print("❌ Test Case 3.1.2 FAIL: Email input was not truncated; maxlength not enforced.")
except Exception as e:
    print(f"❌ Test Case 3.1.2 ERROR: Unexpected issue: {e}")

# Test Case 3.1.3: Invalid format
invalid_email_format = "Sed ut perspiciatis unde omnis iste natus error si"
try:
    driver.find_element(By.ID, "email").clear()
    driver.find_element(By.ID, "password").clear()

    time.sleep(5)
    email_field = driver.find_element(By.ID, "email")
    email_field.click()
    email_field.send_keys(Keys.CONTROL + "a")  
    email_field.send_keys(Keys.DELETE)
    email_field.send_keys(emailInput)
    email_field.send_keys(invalid_email_format)
    time.sleep(1)
    field = driver.find_element(By.ID, "password")
    field.click()
    field.send_keys(Keys.CONTROL + "a")  
    field.send_keys(Keys.DELETE)
    field.send_keys(passwordInput)

    wait = WebDriverWait(driver, 5)
    error_element = wait.until(
        EC.visibility_of_element_located((By.ID, "error_email"))
    )
    error_msg = error_element.text.strip()
    assert error_msg == "Please input a valid email address."
    print("✅ Test Case 3.1.3 PASS: Email input has invalid format and triggered correct validation message.")
except AssertionError:
    print("❌ Test Case 3.1.3 FAIL: Incorrect or missing validation message for invalid email format.")
except Exception as e:
    print(f"❌ Test Case 3.1.3 ERROR: Unexpected issue: {e}")

# Test Case 3.1.4: Empty email
try:
    email_input = driver.find_element(By.ID, "email")
    password_input = driver.find_element(By.ID, "password")

    email_input.clear()
    password_input.clear()
    time.sleep(5)
    field = driver.find_element(By.ID, "password")
    field.click()
    field.send_keys(Keys.CONTROL + "a")  
    field.send_keys(Keys.DELETE)
    field.send_keys(passwordInput)

    time.sleep(1)

    driver.find_element(By.XPATH, "//button[contains(text(), 'Sign in')]").click()
    wait = WebDriverWait(driver, 5)
    error_email_element = wait.until(
        EC.visibility_of_element_located((By.ID, "error_email"))
    )

    error_email_msg = error_email_element.text.strip()
    assert error_email_msg == "Please input a valid email address."
    print("✅ Test Case 3.1.4 PASS: Email empty fields triggered correct validation messages.")
    time.sleep(5)
except AssertionError:
    print("❌ Test Case 3.1.4 FAIL: Incorrect or missing validation message for empty email fields.")

except Exception as e:
    print(f"❌ Test Case 3.1.4 ERROR: Unexpected issue: {e}")


print(f"\n--- TEST CASES FOR PASSWORD ---")

# Test Case 3.2.1: Password Max Length = 50
valid_password = "P" * 50
try:
    driver.find_element(By.ID, "email").clear()
    driver.find_element(By.ID, "password").clear()

    driver.find_element(By.ID, "email").send_keys("admin@gmail.com")
    driver.find_element(By.ID, "password").send_keys(valid_password)

    error_msg = driver.find_element(By.ID, "error_pwd").text.strip()
    assert error_msg == "", f"Unexpected password error: {error_msg}"
    print("✅ Test Case 3.2.1 PASS: No error message for max-length password.")
except AssertionError as ae:
    print(f"❌ Test Case 3.2.1 FAIL:FAIL: {ae}")
except Exception as e:
    print(f"❌ Test Case 3.2.1 FAIL: ERROR: Unexpected issue during password max length test: {e}")

# Test Case 3.2.2: Out-of-bound: Password Max Length = 51
long_pw = "a" * 51

try:
    driver.find_element(By.ID, "email").clear()
    driver.find_element(By.ID, "password").clear()

    time.sleep(1)
    driver.find_element(By.ID, "email").send_keys(emailInput)
    driver.find_element(By.ID, "email").send_keys(long_pw)

    time.sleep(1)
    # Retrieve the actual value inside the email field after sending keys
    actual_pw = driver.find_element(By.ID, "password").get_attribute("value")
    assert actual_email != long_pw  # truncated

    print("✅ Test Case 3.2.2 PASS: Password input exceeded maxlength (out-of-bound) and was truncated correctly.")
except AssertionError:
    print("❌ Test Case 3.2.2 FAIL: Password input was not truncated; maxlength not enforced.")
except Exception as e:
    print(f"❌ Test Case 3.2.2 ERROR: Unexpected issue: {e}")

# Test Case 3.2.3: Empty Password
#empty_str = ""
try:
    driver.find_element(By.ID, "email").clear()
    driver.find_element(By.ID, "password").clear()

    time.sleep(1)
    email_field = driver.find_element(By.ID, "email")
    email_field.click()
    email_field.send_keys(Keys.CONTROL + "a")  
    email_field.send_keys(Keys.DELETE)
    email_field.send_keys(emailInput)
    
    
    pass_field = driver.find_element(By.ID, "password")
    pass_field.click()
    pass_field.send_keys(Keys.CONTROL + "a")  
    pass_field.send_keys(Keys.DELETE)
    time.sleep(1)
    
    driver.find_element(By.XPATH, "//button[contains(text(), 'Sign in')]").click()
    time.sleep(1) 
    
    wait = WebDriverWait(driver, 5)
    error_pw_element = wait.until(
        EC.visibility_of_element_located((By.ID, "error_pwd"))
    )

    error_pw_msg = error_pw_element.text.strip()
    assert error_pw_msg == "This field is required."
    print("✅ Test Case 3.2.3 PASS: Password empty fields triggered correct validation messages.")
    time.sleep(5)
except AssertionError:
    print("❌ Test Case 3.2.3 FAIL: Incorrect or missing validation message for empty password fields.")
except Exception as e:
    print(f"❌ Test Case 3.2.3 ERROR: Unexpected issue: {e}")


print(f"\n--- TEST CASES FOR EMAIL & PASSWORD ---")

# Test Case 3.2.4: Invalid Email Address / Password combination.
invalid_password = "P" * 50
try:
    driver.find_element(By.ID, "email").clear()
    driver.find_element(By.ID, "password").clear()
    time.sleep(2)
    email_field = driver.find_element(By.ID, "email")
    email_field.click()
    email_field.send_keys(Keys.CONTROL + "a")  
    email_field.send_keys(Keys.DELETE)
    email_field.send_keys("admin@gmail.com")
    time.sleep(1)

    pass_field = driver.find_element(By.ID, "password")
    pass_field.click()
    pass_field.send_keys(Keys.CONTROL + "a")  
    pass_field.send_keys(Keys.DELETE)
    pass_field.send_keys(invalid_password)
    time.sleep(1)

    driver.find_element(By.XPATH, "//button[contains(text(), 'Sign in')]").click()
    time.sleep(1) 

    wait = WebDriverWait(driver, 5)
    error_password_element = wait.until(
        EC.visibility_of_element_located((By.ID, "error_pwd"))
    )
    error_password_msg = error_password_element.text.strip()
    assert error_password_msg == "Invalid Email Address / Password."

    print("✅ Test Case 3.2.4 PASS: Invalid Email Address / Password credential triggered correct validation message.")
    time.sleep(5)
except AssertionError as ae:
    print(f"❌ Test Case 3.2.4 FAIL: {ae}")

except Exception as e:
    print(f"❌ Test Case 3.2.4 ERROR: Unexpected issue during credential validation: {e}")

# Test Case 3.2.5: Empty Email Address / Password.
#empty_str = ""
try:
    driver.find_element(By.ID, "email").clear()
    driver.find_element(By.ID, "password").clear()
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Sign in')]").click()
    time.sleep(1) 
    
    wait = WebDriverWait(driver, 5)
    error_password_element = wait.until(
        EC.visibility_of_element_located((By.ID, "error_pwd"))
    )

    error_password_msg = error_password_element.text.strip()
    assert error_password_msg == "Invalid Email Address / Password."
    print("✅ Test Case 3.2.5 PASS: Both email and password empty fields triggered correct validation messages.")
    time.sleep(5)
except AssertionError:
    print("❌ Test Case 3.2.5 FAIL: Incorrect or missing validation message for empty fields.")

except Exception as e:
    print(f"❌ Test Case 3.2.5 ERROR: Unexpected issue: {e}")


print(f"\n--- TEST CASE FOR FORGOT PASSWORD ---")
# Test Case 5: Forgot Password
try:
    # Clear email and password fields
    driver.find_element(By.ID, "email").clear()
    driver.find_element(By.ID, "password").clear()

    email_field = driver.find_element(By.ID, "email")
    email_field.click()
    email_field.send_keys(Keys.CONTROL + "a")
    email_field.send_keys(Keys.DELETE)

    password_field = driver.find_element(By.ID, "password")
    password_field.click()
    password_field.send_keys(Keys.CONTROL + "a")
    password_field.send_keys(Keys.DELETE)

    # Click 'Forgot Password?' link
    time.sleep(1)
    forgot_password_link = driver.find_element(By.LINK_TEXT, "Forgot Password?")
    forgot_password_link.click()
    print("Clicked 'Forgot Password?' link.")

    WebDriverWait(driver, 10).until(EC.url_to_be("http://10.10.99.23/forgot-password"))
    print("Redirected to Forgot Password Page.")

    forgetPassword_text_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//p[@class='mt-4 login-lbl']"))
    )
    FP_text = forgetPassword_text_element.text.strip()
    assert FP_text == "Forgot Password?"

    print("✅ Test Case 5 PASS: Redirected to Forgot Password Page successfully.")

    # Click "Back to Sign In page" link
    back_to_login_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Back to Sign In page"))
    )
    back_to_login_link.click()
    WebDriverWait(driver, 10).until(EC.url_to_be("http://10.10.99.23/login"))

    print("Redirected back to Login Page.")

except AssertionError:
    print("❌ Test Case 5 FAIL: Expected 'Forgot Password?' heading not found.")

except Exception as e:
    print(f"❌ Test Case 5 ERROR: Unexpected issue: {e}")

print(f"\n--- TEST CASE FOR SIGN-IN BUTTON ---")
# Test Case 6: Valid format and correct credential 
try:
    time.sleep(10)
    driver.find_element(By.ID, "email").clear()
    driver.find_element(By.ID, "password").clear()

    print("\nemailInput: ", emailInput)
    print("passwordInput: ", passwordInput)

    time.sleep(1)
    email_field = driver.find_element(By.ID, "email")
    email_field.click()
    email_field.send_keys(Keys.CONTROL + "a")
    email_field.send_keys(Keys.DELETE)
    email_field.send_keys(emailInput)

    time.sleep(1)
    
    field = driver.find_element(By.ID, "password")
    field.click()
    field.send_keys(Keys.CONTROL + "a")  
    field.send_keys(Keys.DELETE)
    field.send_keys(passwordInput)

    time.sleep(1) 
    driver.find_element(By.XPATH, "//button[contains(text(), 'Sign in')]").click()
    print("Clicked Sign-in.")
    time.sleep(10)  

    # Wait for the dashboard page to load
    WebDriverWait(driver, 10).until(EC.url_to_be("http://10.10.99.23/dashboard"))
    print("Login succeeded. Reached dashboard.\n")
    
    dashboard_text_element = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//p[@class='page-title']"))
    )
    dashboard_text = dashboard_text_element.text.strip()
    assert dashboard_text == "Dashboard"
    
    print("✅ Test Case 6 PASS: Valid and correct credential. Redirected to Dashboard successfully.")
    
    
    # Step 1: Click the user menu
    user_menu = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'cursor-pointer') and .//span[contains(text(),'Hello')]]"))
    )
    user_menu.click()
    print("Clicked User Menu.")
    time.sleep(10)  # Short delay to let dropdown render

    # Step 2: Click the Logout button
    logout_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//li[contains(text(), 'Log Out')]"))
    )
    logout_button.click()
    print("Clicked Log Out once.")
    time.sleep(25)
    user_menu = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'cursor-pointer') and .//span[contains(text(),'Hello')]]"))
    )
    user_menu.click()
    print("Clicked User Menu.")
    time.sleep(1)
    logout_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//li[contains(text(), 'Log Out')]"))
    )
    logout_button.click()
    print("Clicked Log Out twice.")
    
    print("Redirected back to login page.")
    driver.delete_all_cookies()
    time.sleep(15)
except AssertionError:
    print("❌ Test Case 6 FAIL: Expected 'Dashboard' but got something else.")

except Exception as e:
    print(f"❌ Test Case 6 ERROR: Unexpected issue: {e}")

print(f"\n--- TEST CASES FOR PASSWORD VISIBILITY ---")
# Test Case 3.2.1.1:Toggling password visibility ON
try:
    driver.find_element(By.ID, "password").clear()
    time.sleep(1)

    # Type password
    field = driver.find_element(By.ID, "password")
    field.click()
    field.send_keys(Keys.CONTROL + "a")
    field.send_keys(Keys.DELETE)
    field.send_keys(passwordInput)

    time.sleep(1)

    value_before = field.get_attribute("value")
    eyeIcon = driver.find_element(By.CSS_SELECTOR, ".svg-inline--fa.fa-eye")
    eyeIcon.click()

    time.sleep(1)

    value_after = field.get_attribute("value")

    if value_before == value_after and len(value_after) == len(passwordInput):
        print("✅ Test Case 3.2.1.1 PASS: Password visibility ON.")
    else:
        print("❌ Test Case 3.2.1.1 FAIL: Password mismatch after visibility toggle.")
except Exception as e:
    print(f"❌ Test Case 3.2.1.1 FAIL: Eye icon toggle ON failed. Error: {e}")


# Test Case 3.2.1.2:Toggling password visibility OFF
try:
    time.sleep(1)

    field = driver.find_element(By.ID, "password")
    value_before = field.get_attribute("value")

    eyeIcon = driver.find_element(By.CSS_SELECTOR, ".svg-inline--fa.fa-eye-slash")
    eyeIcon.click()
    time.sleep(1)

    value_after = field.get_attribute("value")

    if value_before == value_after and len(value_after) == len(passwordInput):
        print("✅ Test Case 3.2.1.2 PASS: Password visibility OFF.")
    else:
        print("❌ Test Case 3.2.1.2 FAIL: Password changed or cleared after toggle OFF.")
except Exception as e:
    print(f"❌ Test Case 3.2.1.2 FAIL: Eye icon toggle OFF failed. Error: {e}")

print(f"\n--- TEST CASES FOR DX LOGO ---")
# Test Case 7 Check for DX Logo
try:
    time.sleep(1)
    logo_image = driver.find_element(By.XPATH, "//img[contains(@src, 'dost_dx.png')]")
    assert logo_image.is_displayed(), "DOST DX Logo image is not visible"
    print("✅ Test Case 7: Logo image 'dost_dx.png' found and visible")
except NoSuchElementException:
    print("❌ Test Case 7 Failed: Logo image 'dost_dx.png' not found")
except AssertionError as e:
    print(f"❌ Test Case 7 Failed: {e}")

print(f"\n--- TEST CASES FOR COPYRIGHT STATEMENT ---")
# Test Case 8 Check for Copyright Statement
try:
    time.sleep(1)
    cs_name = driver.find_element(By.XPATH, "//div[contains(@class, 'note-footer')]//p[normalize-space()='Copyright 2024 DOST. All rights reserved.']")
    assert cs_name.text.strip() == "Copyright 2024 DOST. All rights reserved.", "Copyright Statement text mismatch"
    print("✅ Test Case 8: System name 'Copyright Statement' found and matched")
except NoSuchElementException:
    print("❌ Test Case 8 Failed: Copyright Statement element not found")
except AssertionError as e:
    print(f"❌ Test Case 8 Failed: {e}")



print("--- Tests complete ---")
driver.quit()