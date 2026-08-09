import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = os.getenv(
    "E2E_BASE_URL",
    "http://127.0.0.1:8000",
)

USERNAME = os.getenv("E2E_USERNAME")
PASSWORD = os.getenv("E2E_PASSWORD")


def test_user_login_and_property_workflow():
    assert USERNAME, "E2E_USERNAME is not configured."
    assert PASSWORD, "E2E_PASSWORD is not configured."

    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    try:
        driver.get(f"{BASE_URL}/accounts/login/")

        username_input = wait.until(
            EC.presence_of_element_located(
                (By.NAME, "username")
            )
        )
        password_input = driver.find_element(
            By.NAME,
            "password",
        )

        username_input.send_keys(USERNAME)
        password_input.send_keys(PASSWORD)

        driver.find_element(
            By.CSS_SELECTOR,
            "button[type='submit']",
        ).click()

        wait.until(
            lambda d: "login" not in d.current_url.lower()
        )

        assert "Smart Property Maintenance" in driver.page_source

        driver.get(f"{BASE_URL}/properties/")

        wait.until(
            EC.presence_of_element_located(
                (By.TAG_NAME, "body")
            )
        )

        assert "Demo Property" in driver.page_source

    finally:
        driver.quit()