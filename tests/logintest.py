from app import app, db
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class LoginTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get("http://127.0.0.1:5000")

    def fill_in_element_by_id(self, driver, element_id, text):
        element = driver.find_element(By.ID, element_id)
        element.clear()
        element.send_keys(text)

    def test_website_opens(self):
        driver = self.driver
        self.assertIn("EXPENSE TRACKER", driver.title)

    def test_create_account(self):
        username = 'xandermoons'
        email = 'xander@test.be'
        password = '1234'

        driver = self.driver
        driver.get("http://127.0.0.1:5000/register")

        self.fill_in_element_by_id(driver, 'username', username)
        self.fill_in_element_by_id(driver, 'email', email)
        self.fill_in_element_by_id(driver, 'password', password)
        self.fill_in_element_by_id(driver, 'password2', password)
        driver.find_element(By.CSS_SELECTOR, 'submit').click()

        title = driver.find_element(By.TAG_NAME, 'h1').text.strip()
        self.assertEqual(title, "Sign In")

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
