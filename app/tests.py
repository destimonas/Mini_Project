from django.test import TestCase

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# class LoginTestCase(TestCase):
#     def setUp(self):
#         self.driver = webdriver.Chrome()  # Initialize Chrome WebDriver
#         self.driver.implicitly_wait(10)   # Implicit wait for elements

#     def tearDown(self):
#         self.driver.quit()  # Close the browser session after each test

#     def test_login(self):
#         self.driver.get('http://127.0.0.1:8000/signin/')

#         username_input = self.driver.find_element(By.NAME, 'username')
#         password_input = self.driver.find_element(By.NAME, 'password')
#         login_button = self.driver.find_element(By.ID, 'username')

#         username_input.send_keys('abi')
#         password_input.send_keys('Abi@1234')
#         login_button.click()

#ADDSLOT

# import time
# import logging
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import Select

# # Start the browser
# driver = webdriver.Chrome()

# # Open the login page
# driver.get('http://127.0.0.1:8000/addslot/')

# try:
#     # Provide your login credentials
#     # Locate the username input element by ID
#     username_input = driver.find_element(By.ID, 'username')
#     # Provide your username
#     username_input.send_keys('tijotitus')

#     # Locate the password input element by ID
#     password_input = driver.find_element(By.ID, 'password')
#     # Provide your password
#     password_input.send_keys('Tijo@123')

#     # Wait for the login button to be clickable
#     login_button = WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "btn-info")]'))
#     )
#     # Scroll to the login button to ensure it's in the viewport
#     driver.execute_script("arguments[0].scrollIntoView(true);", login_button)
#     # Click the login button
#     login_button.click()

#     # Wait for the trainerhome page to load
#     WebDriverWait(driver, 30).until(
#         EC.url_matches('http://127.0.0.1:8000/trainerhome/')
#     )

#     # Navigate to the addslot page
#     driver.get('http://127.0.0.1:8000/addslot/')

#     # Corrected the use of until method
#     show_slots_button_condition = EC.presence_of_element_located((By.ID, 'showSlotsFormButton')) and EC.element_to_be_clickable((By.ID, 'showSlotsFormButton'))
#     show_slots_button = WebDriverWait(driver, 30).until(show_slots_button_condition)

#     show_slots_button.click()

#     # Explicit wait for time options to be present
#     WebDriverWait(driver, 30).until(
#         EC.presence_of_all_elements_located((By.XPATH, '//input[@name="time"]'))
#     )

#     # Select 'morning' from the session dropdown
#     session_dropdown = Select(driver.find_element(By.ID, 'session'))
#     session_dropdown.select_by_value('morning')

#     # Assuming the first time option is selected
#     time_options = driver.find_elements(By.XPATH, '//input[@name="time"]')
#     time_options[0].click()

#     # Submit the form
#     submit_button = driver.find_element(By.XPATH, '//button[@class="btn-submit"]')
#     submit_button.click()

#     # Explicit wait for the success message to be visible
#     WebDriverWait(driver, 20).until(
#         EC.presence_of_element_located((By.ID, 'successMessage'))
#     )
   
# finally:
#     # Close the browser window
#     driver.quit()

#SPECIALIZATION


import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SpecializationPageTest(unittest.TestCase):

    def setUp(self):
        # Set up the Selenium WebDriver
        self.driver = webdriver.Chrome()
        # Navigate to the specialization page
        self.driver.get('http://127.0.0.1:8000/specialization/')

    def tearDown(self):
        # Close the browser when the test is done
        self.driver.quit()

    def test_add_specialization(self):
        # Wait for the "Add Specialization" button to be clickable
        add_specialization_button = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.ID, 'showFormButton'))
        )

        # Click the "Add Specialization" button
        add_specialization_button.click()

        # Wait for the specialization input to be clickable
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.ID, 'specialization'))
        ).send_keys('CrossFit')

        # Find the description input and fill it out
        description_input = self.driver.find_element(By.ID, 'description')
        description_input.send_keys('excercie')

        # Wait for the submit button to be present
        submit_button = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'btn-submit'))
        )
        submit_button.click()

        # Wait for the page to reload
        time.sleep(2)  # You can use WebDriverWait for a more robust solution

        # Assert that the new specialization appears in the table
        new_specialization_name = 'CrossFit'
        table_rows = self.driver.find_elements(By.XPATH, '//table/tbody/tr')
        last_row_data = table_rows[-1].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(last_row_data[1].text, new_specialization_name)

    def test_update_specialization(self):
        # Wait for the "Update" link to be present
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//table/tbody/tr[1]/td[4]/a'))
        ).click()

       

        # Update the specialization name
        specialization_input = self.driver.find_element(By.ID, 'specialization')
        specialization_input.clear()
        updated_specialization_name = 'Updated Specialization'
        specialization_input.send_keys(updated_specialization_name)

         # Find the submit button using a different method, e.g., by ID
        submit_button = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, 'submit'))
        )
        submit_button.click()

        # Wait for the page to reload
        time.sleep(2)  # You can use WebDriverWait for a more robust solution

        # Assert that the updated specialization name appears in the table
        table_rows = self.driver.find_elements(By.XPATH, '//table/tbody/tr')
        first_row_data = table_rows[0].find_elements(By.TAG_NAME, 'td')
        self.assertEqual(first_row_data[1].text, updated_specialization_name)

if __name__ == "__main__":
    unittest.main()

# import time
# import unittest
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException

# class UserTrainerPageTest(unittest.TestCase):

#     def setUp(self):

#         self.driver = webdriver.Chrome()
  
#         self.driver.get('http://127.0.0.1:8000/userhome/usertrainer/')  

#     def tearDown(self):
 
#         self.driver.quit()

#     def test_enroll_process(self):
#         try:
           
#             trainer_card = WebDriverWait(self.driver, 10).until(
#                 EC.presence_of_element_located((By.CLASS_NAME, 'card'))
#             )
#             trainer_card.click()

          
#             time_slot_checkbox = WebDriverWait(self.driver, 10).until(
#                 EC.element_to_be_clickable((By.CSS_SELECTOR, 'ul#timeSlots1 input[type="checkbox"]'))
#             )
#             time_slot_checkbox.click()

#             enroll_button = WebDriverWait(self.driver, 10).until(
#                 EC.element_to_be_clickable((By.ID, 'consultbtn'))
#             )
#             enroll_button.click()

      
#             starter_package_button = WebDriverWait(self.driver, 10).until(
#                 EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "12 Week Starter Package")]'))
#             )

          
#             self.driver.execute_script("arguments[0].scrollIntoView();", starter_package_button)

           
#             starter_package_button.click()

        
#             billing_modal = WebDriverWait(self.driver, 10).until(
#                 EC.presence_of_element_located((By.ID, 'billingModal1'))
#             )

           
#             make_payment_button = WebDriverWait(billing_modal, 10).until(
#                 EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Make Payment")]'))
#             )

#             self.driver.execute_script("arguments[0].scrollIntoView();", make_payment_button)

    
#             make_payment_button.click()

       
#             payment_option_modal = WebDriverWait(self.driver, 10).until(
#                 EC.presence_of_element_located((By.ID, 'paymentOptionModal1'))
#             )

          
#             netbanking_option = WebDriverWait(payment_option_modal, 10).until(
#                 EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Netbanking")]'))
#             )

        
#             self.driver.execute_script("arguments[0].scrollIntoView();", netbanking_option)

          
#             self.driver.execute_script("arguments[0].click();", netbanking_option)

         
        
#             razorpay_payment_modal = WebDriverWait(self.driver, 30).until(
#                 EC.presence_of_element_located((By.ID, 'razorpayPaymentModal1'))
#             )

#             razorpay_payment_form = WebDriverWait(razorpay_payment_modal, 10).until(
#                 EC.presence_of_element_located((By.ID, 'razorpay-form'))
#             )

         
#             try:
              
#                 close_button = WebDriverWait(razorpay_payment_modal, 10).until(
#                     EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Close")]'))
#                 )
#                 close_button.click()
#             except TimeoutException:
             
#                 self.driver.execute_script("arguments[0].style.display='none';", razorpay_payment_modal)

#             razorpay_success_modal = WebDriverWait(self.driver, 30).until(
#                 EC.visibility_of_element_located((By.ID, 'razorpaySuccessModal1'))
#             )


#             success_close_button = WebDriverWait(razorpay_success_modal, 10).until(
#                 EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Close")]'))
#             )
#             success_close_button.click()



#         except TimeoutException as e:
#             print(f"Timed out waiting for Razorpay payment modal: {e}")
#             raise

# if __name__ == "__main__":
#     unittest.main()

            