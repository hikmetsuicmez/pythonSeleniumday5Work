from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
import pytest
from pathlib import Path
from datetime import date
from time import sleep


class Test_ExampleSauce:
    def setup_method(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.maximize_window()
        self.driver.get("https://www.saucedemo.com/")
        self.folderPath = str(date.today())
        Path(self.folderPath).mkdir(exist_ok=True)

    def teardown_method(self):
        self.driver.quit()

    def test_empty_login(self):
        self.waitForElementVisible((By.ID, 'login-button'))
        loginBtn = self.driver.find_element(By.ID, 'login-button')
        loginBtn.click()

        self.waitForElementVisible(
            (By.XPATH, '//*[@id="login_button_container"]/div/form/div[3]/h3'))

        errorMessage = self.driver.find_element(
            By.XPATH, '//*[@id="login_button_container"]/div/form/div[3]/h3')

        self.driver.save_screenshot(f"{self.folderPath}/test-empty-login.png")

        assert errorMessage.text == "Epic sadface: Username is required"

    @pytest.mark.parametrize("username", ["hikmet", "standard_user", "problem_user"])
    def test_empty_password_login(self, username):

        self.waitForElementVisible((By.ID, 'user-name'))
        usernameInput = self.driver.find_element(By.ID, 'user-name')
        usernameInput.send_keys(username)

        self.waitForElementVisible((By.ID, 'login-button'))
        loginBtn = self.driver.find_element(By.ID, 'login-button')
        loginBtn.click()

        errorMessage = self.driver.find_element(
            By.XPATH, '//*[@id="login_button_container"]/div/form/div[3]/h3')

        self.driver.save_screenshot(
            f"{self.folderPath}/test-empty-password-{username}-login.png")

        assert errorMessage.text == 'Epic sadface: Password is required'

    def test_invalid_login(self):
        self.waitForElementVisible((By.ID, 'user-name'))

        usernameInput = self.driver.find_element(By.ID, 'user-name')
        passwordInput = self.driver.find_element(By.ID, 'password')
        loginBtn = self.driver.find_element(By.ID, 'login-button')

        actions = ActionChains(self.driver)
        actions.send_keys_to_element(usernameInput, 'locked_out_user')
        actions.send_keys_to_element(passwordInput, 'secret_sauce')
        actions.send_keys_to_element(loginBtn, Keys.ENTER)
        actions.perform()

        errorMessage = self.driver.find_element(
            By.XPATH, '//*[@id="login_button_container"]/div/form/div[3]/h3')

        self.driver.save_screenshot(
            f"{self.folderPath}/test-invalid-login.png")

        assert errorMessage.text == 'Epic sadface: Sorry, this user has been locked out.'

    def test_icon_login(self):
        self.waitForElementVisible((By.ID, 'login-button'))
        loginBtn = self.driver.find_element(By.ID, 'login-button')
        loginBtn.click()

        errorBtn = self.driver.find_element(By.CLASS_NAME, 'error-button')
        errorBtn.click()

        errorIcon = len(self.driver.find_elements(By.CLASS_NAME, 'error_icon'))
        self.driver.save_screenshot(f"{self.folderPath}/test-icon-login.png")

        assert errorIcon == 0

    def test_success_login(self):
        self.waitForElementVisible((By.ID, 'user-name'))

        usernameInput = self.driver.find_element(By.ID, 'user-name')
        passwordInput = self.driver.find_element(By.ID, 'password')
        loginBtn = self.driver.find_element(By.ID, 'login-button')

        actions = ActionChains(self.driver)
        actions.send_keys_to_element(usernameInput, 'standard_user')
        actions.send_keys_to_element(passwordInput, 'secret_sauce')
        actions.send_keys_to_element(loginBtn, Keys.ENTER)
        actions.perform()

        self.waitForElementVisible((By.CLASS_NAME, 'inventory_list'))
        products = self.driver.find_elements(By.CLASS_NAME, 'inventory_item')

        self.driver.save_screenshot(
            f"{self.folderPath}/test-success-login.png")

        assert len(products) == 6

    @pytest.mark.parametrize("username, password", [("standard_user", "1"), ("locked_out_user", "61"), ("problem_user", "2"), ("performance_glitch_user", "sauce_secret")])
    def test_wrong_password_login(self, username, password):
        self.waitForElementVisible((By.ID, 'user-name'))

        usernameInput = self.driver.find_element(By.ID, 'user-name')
        passwordInput = self.driver.find_element(By.ID, 'password')
        loginBtn = self.driver.find_element(By.ID, 'login-button')

        actions = ActionChains(self.driver)
        actions.send_keys_to_element(usernameInput, username)
        actions.send_keys_to_element(passwordInput, password)
        actions.send_keys_to_element(loginBtn, Keys.ENTER)
        actions.perform()

        errorMessage = self.driver.find_element(
            By.XPATH, '//*[@id="login_button_container"]/div/form/div[3]/h3')

        self.driver.save_screenshot(
            f"{self.folderPath}/test-wrong-password-{username}-{password}-login.png")

        assert errorMessage.text == 'Epic sadface: Username and password do not match any user in this service'

    def test_add_to_cart(self):
        self.waitForElementVisible((By.ID, 'user-name'))

        usernameInput = self.driver.find_element(By.ID, 'user-name')
        passwordInput = self.driver.find_element(By.ID, 'password')
        loginBtn = self.driver.find_element(By.ID, 'login-button')

        actions = ActionChains(self.driver)
        actions.send_keys_to_element(usernameInput, 'standard_user')
        actions.send_keys_to_element(passwordInput, 'secret_sauce')
        actions.send_keys_to_element(loginBtn, Keys.ENTER)
        actions.perform()

        self.waitForElementVisible((By.CLASS_NAME, 'inventory_item'))

        productsNames = self.driver.find_elements(
            By.CLASS_NAME, 'inventory_item_name')

        productsNamesList = []
        for x in productsNames:
            name = x.text.replace(" ", "-").lower()
            productsNamesList.append(name)

        # for a in productsNamesList:
        #     print(a)

        products = self.driver.find_elements(By.CLASS_NAME, 'inventory_item')

        i = 0
        for product in products:
            self.waitForElementVisible((By.CLASS_NAME, 'btn_inventory'))
            addToCart = product.find_element(
                By.ID, f'add-to-cart-{productsNamesList[i]}')
            addToCart.click()
            i += 1

        shoppingCart = self.driver.find_element(
            By.ID, 'shopping_cart_container')

        self.driver.save_screenshot(f"{self.folderPath}/test-add-to-cart.png")

        assert shoppingCart.text == "6"

    def waitForElementVisible(self, locator, timeout=5):
        WebDriverWait(self.driver, timeout).until(
            ec.visibility_of_element_located(locator))
