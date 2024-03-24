import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
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

    def test_add_expense(self):
        driver = self.driver
        driver.get('http://127.0.0.1:5000/add_expense')

        fill_in_element_by_id(driver, 'category', 'food')
        fill_in_element_by_id(driver, 'name', 'colruyt')
        fill_in_element_by_id(driver, 'amount', 66)
        fill_in_element_by_id(driver, 'date', '2024-03-22')
        driver.find_element(By.ID, 'submit').click()

        message = driver.find_element(By.ID, 'message').text.strip()
        self.assertEqual(message, "Expense added successfully!")

        driver.get('http://127.0.0.1:5000/show_expenses')

        time.sleep(1)

        name = driver.find_element(By.CSS_SELECTOR, 'td.name.data').text.strip()
        self.assertEqual(name, "colruyt")

        amount = driver.find_element(By.CSS_SELECTOR, 'td.amount.data').text.strip()
        self.assertEqual(amount, "€66.0")

        category = driver.find_element(By.CSS_SELECTOR, 'td.category.data').text.strip()
        self.assertEqual(category, "food")

        date = driver.find_element(By.CSS_SELECTOR, 'td.date.data').text.strip()
        self.assertEqual(date, "2024-03-22")

    def test_add_expense_without_amount(self):
        driver = self.driver
        driver.get('http://127.0.0.1:5000/add_expense')

        fill_in_element_by_id(driver, 'category', 'food')
        fill_in_element_by_id(driver, 'name', 'colruyt')
        fill_in_element_by_id(driver, 'date', '2024-03-22')
        driver.find_element(By.ID, 'submit').click()

        message = driver.find_element(By.ID, 'message').text.strip()
        self.assertEqual(message, "Error: Failed to add expense. Please try again.")

    def test_add_expense_with_negative_amount(self):
        driver = self.driver
        driver.get('http://127.0.0.1:5000/add_expense')

        fill_in_element_by_id(driver, 'category', 'food')
        fill_in_element_by_id(driver, 'name', 'colruyt')
        fill_in_element_by_id(driver, 'amount', -66)
        fill_in_element_by_id(driver, 'date', '2024-03-22')
        driver.find_element(By.ID, 'submit').click()

        message = driver.find_element(By.ID, 'message').text.strip()
        self.assertEqual(message, "Error: Failed to add expense. Please try again.")

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
