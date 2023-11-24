from flask import Flask, render_template
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index_with_download.html')

@app.route('/test_login')
def test_login():
    email_id = 'slaadmin'
    password = 'slaadmin@123'

    # Set up Chrome options for headless mode
    chrome_options = Options()
    #chrome_options.add_argument('--headless')
    #chrome_options.add_argument('--disable-gpu')  # May be required in headless mode
    chrome_options.add_argument('--window-size=1920x1080')  # Adjust the size as needed
    chrome_options.add_argument('--disable-software-rasterizer')  # Add this line

    # Initialize the Selenium WebDriver with Chrome options
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Navigate to the ERP login page
        driver.get('https://erp.electrolabgroup.com/login#login')

        # Enter login credentials
        email_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="login_email"]')))
        email_input.send_keys(email_id)

        password_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="login_password"]')))
        password_input.send_keys(password)

        # Find the login button and click it
        login_button = driver.find_element(By.XPATH,
                                           '//*[@id="page-login"]/div/main/div[2]/div/section[1]/div[1]/form/div[2]/button')
        login_button.click()

        # Wait for the login process to complete (you may need to adjust this)
        time.sleep(5)

        # You can add further logic to verify that the login was successful.
        # For example, you can check if the user is redirected to the expected page.

    finally:
        # Close the WebDriver
        driver.quit()

    return "Login Test Completed"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
