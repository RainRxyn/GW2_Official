from datetime import time

import psycopg2
from selenium.webdriver.common.by import By

from tests.testconfig import db_user, db_password, db_host, db_port


def set_data(query):
    """Inserts data into the database. This function is only used internally in the module"""

    try:
        connection = psycopg2.connect(
           dbname="app.db",
           user=db_user,
           password=db_password,
           host=db_host,
           port=db_port
        )
        cursor = connection.cursor()
        cursor.execute(query)

        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to database", error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("database connection is closed")


def clear_data(table: str):
    """Clears the given table from the postgres db"""

    query = 'DELETE FROM {}'.format(table)
    set_data(query)


def fill_in_element_by_id(driver, element_id, text):
    element = driver.find_element(By.ID, element_id)
    element.clear()
    element.send_keys(text)


def clear_all_tables():
    clear_data('expenses')
    clear_data('incomes')
    clear_data('public."user"')


def create_user(driver, username, email, password):

    driver.get("http://127.0.0.1:5000/register")

    fill_in_element_by_id(driver, 'username', username)
    fill_in_element_by_id(driver, 'email', email)
    fill_in_element_by_id(driver, 'password', password)
    fill_in_element_by_id(driver, 'password2', password)
    driver.find_element(By.ID, 'submit').click()


def login_user(driver, email, password):
    driver.get("http://127.0.0.1:5000/login")

    fill_in_element_by_id(driver, 'email', email)
    fill_in_element_by_id(driver, 'password', password)
    driver.find_element(By.ID, 'submit').click()
