from flask import Flask, render_template
from splinter import Browser
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index_with_download.html')

@app.route('/test_login')
def test_login():
    email_id = 'slaadmin'
    password = 'slaadmin@123'

    # Set up Splinter with Chrome browser
    with Browser('chrome') as browser:
        # Navigate to the ERP login page
        browser.visit('https://erp.electrolabgroup.com/login#login')

        # Enter login credentials
        browser.find_by_xpath('//*[@id="login_email"]').fill(email_id)
        browser.find_by_xpath('//*[@id="login_password"]').fill(password)

        # Find the login button and click it
        browser.find_by_xpath('//*[@id="page-login"]/div/main/div[2]/div/section[1]/div[1]/form/div[2]/button').click()

        # Wait for the login process to complete (you may need to adjust this)
        time.sleep(5)

        # You can add further logic to verify that the login was successful.
        # For example, you can check if the user is redirected to the expected page.

    return "Login Test Completed"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
