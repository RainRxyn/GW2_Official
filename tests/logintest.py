import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from tests.general_test_methods import clear_data


unittest.TestLoader.sortTestMethodsUsing = None


def fill_in_element_by_id(driver, element_id, text):

    element = driver.find_element(By.ID, element_id)
    element.clear()
    element.send_keys(text)


class LoginTest(unittest.TestCase):

    def setUp(self):

        self.driver = webdriver.Firefox()

    def test_website_opens(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000")
        self.assertIn("EXPENSE TRACKER", driver.title)

    def test_create_account(self):

        clear_data()

        username = 'xandermoons'
        email = 'xander@test.be'
        password = '1234'

        driver = self.driver
        driver.get("http://127.0.0.1:5000/register")

        fill_in_element_by_id(driver, 'username', username)
        fill_in_element_by_id(driver, 'email', email)
        fill_in_element_by_id(driver, 'password', password)
        fill_in_element_by_id(driver, 'password2', password)
        driver.find_element(By.ID, 'submit').click()

        message = driver.find_element(By.CLASS_NAME, 'message').text.strip()
        print(message)
        self.assertEqual(message, "You are a registered user. Please login")

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
