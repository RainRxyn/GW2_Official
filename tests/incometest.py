import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from tests.general_test_methods import fill_in_element_by_id, clear_all_tables, create_user, login_user
import time

unittest.TestLoader.sortTestMethodsUsing = None

username = 'xandermoons'
email = 'xander@test.be'
password = '1234'


class ExpenseTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()

        clear_all_tables()

        create_user(self.driver, username, email, password)
        login_user(self.driver, email, password)

    def test_add_income(self):
        driver = self.driver
        driver.get('http://127.0.0.1:5000/add_income')

        fill_in_element_by_id(driver, 'name', 'salary')
        fill_in_element_by_id(driver, 'amount', 2350)
        fill_in_element_by_id(driver, 'date', '2024-03-30')
        select = Select(driver.find_element(By.ID, 'frequency'))
        select.select_by_value('Monthly')
        driver.find_element(By.ID, 'submit').click()

        message = driver.find_element(By.ID, 'message').text.strip()
        self.assertEqual(message, "Income has been successfully added")

        driver.get('http://127.0.0.1:5000/income')

        time.sleep(1)

        name = driver.find_element(By.CSS_SELECTOR, 'td.name.data').text.strip()
        self.assertEqual(name, "salary")

        amount = driver.find_element(By.CSS_SELECTOR, 'td.amount.data').text.strip()
        self.assertEqual(amount, "2350.0")

        date = driver.find_element(By.CSS_SELECTOR, 'td.date.data').text.strip()
        self.assertEqual(date, "2024-03-30")

        frequency = driver.find_element(By.CSS_SELECTOR, 'td.frequency.data').text.strip()
        self.assertEqual(frequency, "Monthly")

    def test_add_income_without_amount(self):
        driver = self.driver
        driver.get('http://127.0.0.1:5000/add_income')

        fill_in_element_by_id(driver, 'name', 'salary')
        fill_in_element_by_id(driver, 'date', '2024-03-30')
        select = Select(driver.find_element(By.ID, 'frequency'))
        select.select_by_value('Monthly')
        driver.find_element(By.ID, 'submit').click()

        time.sleep(2)

        title = driver.find_element(By.TAG_NAME, 'h1').text.strip().lower()
        self.assertEqual(title, "add income")

    def test_add_income_with_negative_amount(self):
        driver = self.driver
        driver.get('http://127.0.0.1:5000/add_income')

        fill_in_element_by_id(driver, 'name', 'salary')
        fill_in_element_by_id(driver, 'amount', -2350)
        fill_in_element_by_id(driver, 'date', '2024-03-30')
        select = Select(driver.find_element(By.ID, 'frequency'))
        select.select_by_value('Monthly')
        driver.find_element(By.ID, 'submit').click()

        time.sleep(2)

        title = driver.find_element(By.TAG_NAME, 'h1').text.strip().lower()
        self.assertEqual(title, "add income")

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
