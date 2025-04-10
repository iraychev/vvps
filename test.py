import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class RegistrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize the WebDriver
        cls.driver = webdriver.Chrome() 
        cls.driver.implicitly_wait(5)
        cls.url = "http://127.0.0.1:5500/register.html"

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        self.driver.get(self.url)

    def fill_form(self, firstName="Petar", lastName="Petrov", email="petar_petrov@abv.bg",
                  username="petko", password="12345678@A", confirmPassword="12345678@A",
                  phone="0888888888", terms=True):
        driver = self.driver
        driver.find_element(By.ID, "firstName").clear()
        driver.find_element(By.ID, "firstName").send_keys(firstName)
        driver.find_element(By.ID, "lastName").clear()
        driver.find_element(By.ID, "lastName").send_keys(lastName)
        driver.find_element(By.ID, "email").clear()
        driver.find_element(By.ID, "email").send_keys(email)
        driver.find_element(By.ID, "username").clear()
        driver.find_element(By.ID, "username").send_keys(username)
        driver.find_element(By.ID, "password").clear()
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.ID, "confirmPassword").clear()
        driver.find_element(By.ID, "confirmPassword").send_keys(confirmPassword)
        driver.find_element(By.ID, "phone").clear()
        driver.find_element(By.ID, "phone").send_keys(phone)
        checkbox = driver.find_element(By.ID, "terms")
        if checkbox.is_selected() != terms:
            checkbox.click()

    def submit_form(self):
        self.driver.find_element(By.XPATH, "//input[@type='submit']").click()
        time.sleep(1)  # Pause to simulate waiting for form processing

    def get_message(self):
        return self.driver.find_element(By.ID, "message").text

    def test_valid_registration(self):
        """Test valid registration."""
        self.fill_form()
        self.submit_form()
        self.assertEqual(self.get_message(), "Registration successful")

    def test_missing_email(self):
        """Test registration with missing email."""
        self.fill_form(email="")
        self.submit_form()
        email_field = self.driver.find_element(By.ID, "email")
        self.assertEqual(email_field.get_attribute("value"), "")

    def test_invalid_email_format(self):
        """Test registration with invalid email format."""
        self.fill_form(email="invalidemail")
        self.submit_form()
        email_field = self.driver.find_element(By.ID, "email")
        self.assertEqual(email_field.get_attribute("value"), "invalidemail")

    def test_password_mismatch(self):
        """Test registration with mismatched passwords."""
        self.fill_form(confirmPassword="Opagreshka1")
        self.submit_form()
        self.assertEqual(self.get_message(), "Passwords do not match.")

    def test_short_password(self):
        """Test registration with a too short password."""
        self.fill_form(password="123", confirmPassword="123")
        self.submit_form()
        self.assertEqual(self.get_message(), "Password must be at least 8 characters long, contain a number and an uppercase letter.")

    def test_terms_not_checked(self):
        """Test registration without checking terms and conditions."""
        self.fill_form(terms=False)
        self.submit_form()
        checkbox = self.driver.find_element(By.ID, "terms")
        self.assertFalse(checkbox.is_selected())

    def test_special_characters_in_name(self):
        """Test registration with special characters in the first name."""
        self.fill_form(firstName="Pet@r")
        self.submit_form()
        self.assertEqual(self.get_message(), "Invalid characters in first name.")

    def test_excessively_long_input(self):
        """Test registration with excessively long username."""
        long_username = "abcdefghijklmnopqrstuwxyzabcde"
        self.fill_form(username=long_username)
        self.submit_form()
        self.assertEqual(self.driver.find_element(By.ID, "username").get_attribute("value"), long_username)

    def test_duplicate_username(self):
        """Test registration with duplicate username."""
        self.fill_form(username="petarigracha")
        self.submit_form()
        self.assertEqual(self.get_message(), "Username already exists.")

    def test_invalid_phone_format(self):
        """Test registration with invalid phone format."""
        self.fill_form(phone="ABCDEF")
        self.submit_form()
        self.assertEqual(self.get_message(), "Please enter a valid phone number.")

if __name__ == "__main__":
    unittest.main()
