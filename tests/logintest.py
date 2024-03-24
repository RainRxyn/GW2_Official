import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from tests.general_test_methods import fill_in_element_by_id, clear_all_tables, create_user, login_user


unittest.TestLoader.sortTestMethodsUsing = None

username = 'xandermoons'
email = 'xander@test.be'
password = '1234'


class LoginTest(unittest.TestCase):

    def setUp(self):

        self.driver = webdriver.Firefox()

    def test_website_opens(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000")
        self.assertIn("EXPENSE TRACKER", driver.title)

    def test_create_account(self):

        clear_all_tables()

        driver = self.driver

        create_user(driver, username, email, password)

        message = driver.find_element(By.ID, 'message').text.strip()
        self.assertEqual(message, "You are a registered user. Please login")

    def test_empty_username(self):

        clear_all_tables()

        driver = self.driver
        driver.get("http://127.0.0.1:5000/register")

        fill_in_element_by_id(driver, 'email', email)
        fill_in_element_by_id(driver, 'password', password)
        fill_in_element_by_id(driver, 'password2', password)
        driver.find_element(By.ID, 'submit').click()

        title = driver.find_element(By.TAG_NAME, value='h1').text.strip().lower()
        self.assertEqual(title, "register")

    def test_wrong_password(self):

        clear_all_tables()

        driver = self.driver
        driver.get("http://127.0.0.1:5000/register")

        fill_in_element_by_id(driver, 'username', username)
        fill_in_element_by_id(driver, 'email', email)
        fill_in_element_by_id(driver, 'password', password)
        fill_in_element_by_id(driver, 'password2', "4321")
        driver.find_element(By.ID, 'submit').click()

        message = driver.find_element(By.ID, 'message').text.strip()
        self.assertEqual(message, "Error: The passwords do not match")

    def test_login_after_registration(self):
        clear_all_tables()

        driver = self.driver

        create_user(driver, username, email, password)

        message = driver.find_element(By.ID, 'message').text.strip()
        self.assertEqual(message, "You are a registered user. Please login")

        login_user(driver, email, password)

        logout = driver.find_element(By.ID, 'logout').text.strip().lower()
        self.assertEqual(logout, "log out")

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
