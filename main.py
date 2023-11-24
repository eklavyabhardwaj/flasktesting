from flask import Flask, render_template, send_file
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

@app.route('/download_file')
def download_file():
    email_id = 'slaadmin'
    password = 'slaadmin@123'

    # Set up Chrome options for headless mode
    chrome_options = Options()
    #chrome_options.add_argument('--headless')
    #chrome_options.add_argument('--disable-gpu')  # May be required in headless mode
    chrome_options.add_argument('--window-size=1920x1080')  # Adjust the size as needed
    chrome_options.add_argument('--disable-software-rasterizer')  # Add this line

    # Specify the download directory as the program folder
    program_folder = os.path.dirname(os.path.abspath(__file__))
    download_dir = os.path.join(program_folder, 'downloads')
    chrome_options.add_argument(f'--download-path={download_dir}')

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

        time.sleep(3)

        # Navigate to the ISSUE_SLA report page
        quotation_report_url = 'https://erp.electrolabgroup.com/app/issue/view/report/Issue%20SLA%20T2023'
        driver.get(quotation_report_url)

        # Find the menu option and click on it to expand the menu
        menu_option = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH,
             '//*[@id="page-List/Issue/Report/Issue SLA T2023"]/div[1]/div/div/div[2]/div[2]/div[1]/button')))
        menu_option.click()

        # Wait for the menu to expand and show the dropdown options (you may need to adjust this)
        time.sleep(2)

        # Find the dropdown menu with the Export option and click on it
        export_option_dropdown = driver.find_element(By.XPATH,
                                                     '//*[@id="page-List/Issue/Report/Issue SLA T2023"]/div[1]/div/div/div[2]/div[2]/div[1]/ul/li[6]/a')
        export_option_dropdown.click()

        # Wait for the Export option to be visible in the dropdown menu (you may need to adjust this)
        time.sleep(2)

        # Find the "Export All" checkbox and click on it
        export_all_checkbox = driver.find_element(By.XPATH,
                                                  '//span[contains(@class, "label-area") and contains(text(), "Export All")]//preceding-sibling::span[@class="input-area"]//input[@type="checkbox"]')
        export_all_checkbox.click()

        # Find the Download button and click on it
        download_button = driver.find_element(By.XPATH, '//button[contains(text(), "Download")]')
        download_button.click()

        # Wait for the download to complete (you may need to adjust this)
        time.sleep(10)


        # Wait for the file to download (you may need to adjust the sleep time)
        time.sleep(5)

        # You can add further logic to verify the file is downloaded successfully
        # For example, you can check the presence of the downloaded file in a specific directory.

    finally:
        # Close the WebDriver
        driver.quit()

    # Assuming the file is downloaded to the current working directory with a specific name
    file_path = os.path.join(os.getcwd(), 'downloaded_file.txt')

    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(port = 8000, debug=True)
