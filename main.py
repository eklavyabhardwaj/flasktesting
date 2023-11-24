from flask import Flask, render_template
from playwright.sync_api import sync_playwright

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index_with_download.html')

@app.route('/test_login')
def test_login():
    email_id = 'slaadmin'
    password = 'slaadmin@123'

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()

        # Navigate to the ERP login page
        page = context.new_page()
        page.goto('https://erp.electrolabgroup.com/login#login')

        # Enter login credentials
        email_input = page.wait_for_selector('//*[@id="login_email"]')
        email_input.type(email_id)

        password_input = page.wait_for_selector('//*[@id="login_password"]')
        password_input.type(password)

        # Find the login button and click it
        login_button = page.wait_for_selector(
            '//*[@id="page-login"]/div/main/div[2]/div/section[1]/div[1]/form/div[2]/button', timeout=10000)

        login_button.click()

        # Wait for the login process to complete (you may need to adjust this)
        page.wait_for_timeout(5000)

        # You can add further logic to verify that the login was successful.
        # For example, you can check if the user is redirected to the expected page.

        # Close the browser
        context.close()

    return "Login Test Completed"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
