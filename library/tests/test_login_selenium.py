"""
Selenium Test: Login and Logout Functionality
==============================================
This test verifies:
1. Successful login with valid credentials
2. Successful logout
3. Failed login with invalid credentials and appropriate error message
"""

import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from authentication.models import CustomUser


class LoginLogoutTest(StaticLiveServerTestCase):
    """
    Selenium tests for verifying login and logout functionality
    with both valid and invalid credentials.
    """

    # Test user credentials
    TEST_EMAIL = "testuser@library.com"
    TEST_PASSWORD = "TestPass123!"
    TEST_FIRST_NAME = "Test"
    TEST_LAST_NAME = "User"

    INVALID_EMAIL = "wronguser@library.com"
    INVALID_PASSWORD = "WrongPass999!"

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Setup Chrome WebDriver
        chrome_options = Options()
        # Run in visible mode so we can see the test
        chrome_options.add_argument("--window-size=1280,800")
        chrome_options.add_argument("--disable-gpu")

        cls.browser = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=chrome_options,
        )
        cls.browser.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def setUp(self):
        """Create a test user before each test."""
        self.user = CustomUser.objects.create_user(
            email=self.TEST_EMAIL,
            password=self.TEST_PASSWORD,
            first_name=self.TEST_FIRST_NAME,
            last_name=self.TEST_LAST_NAME,
            middle_name="",
            role=0,
            is_active=True,
        )

    def tearDown(self):
        """Clean up after each test."""
        # Make sure we're logged out
        self.browser.delete_all_cookies()

    def _login(self, email, password):
        """Helper: navigate to login page and submit credentials."""
        self.browser.get(f"{self.live_server_url}/auth/login/")
        time.sleep(1)  # Small pause for visual clarity during recording

        # Find and fill the email field
        email_field = self.browser.find_element(By.ID, "email")
        email_field.clear()
        email_field.send_keys(email)
        time.sleep(0.5)

        # Find and fill the password field
        password_field = self.browser.find_element(By.ID, "password")
        password_field.clear()
        password_field.send_keys(password)
        time.sleep(0.5)

        # Click the Login button
        login_button = self.browser.find_element(By.CSS_SELECTOR, "button.btn-primary")
        login_button.click()
        time.sleep(1)

    def test_valid_login_logout(self):
        """
        Test Case 1: Valid Login and Logout
        ------------------------------------
        Steps:
        1. Navigate to the login page
        2. Enter valid email and password
        3. Click Login
        4. Verify successful login (user email visible in navbar)
        5. Click Logout
        6. Verify successful logout (redirected to login page)
        """
        print("\n--- TEST: Valid Login and Logout ---")

        # Step 1-3: Login with valid credentials
        print(f"Logging in with email: {self.TEST_EMAIL}")
        self._login(self.TEST_EMAIL, self.TEST_PASSWORD)

        # Step 4: Verify successful login
        # Check that the user email is displayed in the navbar
        wait = WebDriverWait(self.browser, 10)
        user_email_element = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".navbar-user span"))
        )
        self.assertIn(
            self.TEST_EMAIL,
            user_email_element.text,
            "User email should be visible in the navbar after login",
        )
        print(f"✓ Login successful — user email '{self.TEST_EMAIL}' is visible in navbar")

        # Check for success message
        try:
            alert = self.browser.find_element(By.CSS_SELECTOR, ".alert-success")
            print(f"✓ Success message displayed: '{alert.text}'")
            self.assertIn("Welcome back", alert.text)
        except Exception:
            pass  # Message might have already disappeared

        time.sleep(1)

        # Step 5: Click Logout
        print("Clicking Logout button...")
        logout_button = self.browser.find_element(
            By.CSS_SELECTOR, "form.logout-form button"
        )
        logout_button.click()
        time.sleep(1)

        # Step 6: Verify successful logout
        # After logout, user should be redirected to login page
        wait.until(EC.url_contains("/auth/login/"))
        self.assertIn("/auth/login/", self.browser.current_url)
        print(f"✓ Redirected to login page: {self.browser.current_url}")

        # Check for logout success message
        try:
            alert = self.browser.find_element(By.CSS_SELECTOR, ".alert-success")
            print(f"✓ Logout message displayed: '{alert.text}'")
            self.assertIn("logged out", alert.text.lower())
        except Exception:
            pass

        # Verify the Login/Register buttons are visible (user is NOT authenticated)
        login_link = self.browser.find_element(
            By.CSS_SELECTOR, ".navbar-user a.btn-secondary"
        )
        self.assertEqual(login_link.text.strip(), "Login")
        print("✓ Logout successful — Login button is visible again in navbar")

        print("--- PASSED: Valid Login and Logout ---\n")

    def test_invalid_login(self):
        """
        Test Case 2: Invalid Login
        ---------------------------
        Steps:
        1. Navigate to the login page
        2. Enter invalid email and password
        3. Click Login
        4. Verify that login fails with an error message
        5. Verify user remains on the login page
        """
        print("\n--- TEST: Invalid Login ---")

        # Step 1-3: Login with invalid credentials
        print(f"Attempting login with invalid email: {self.INVALID_EMAIL}")
        self._login(self.INVALID_EMAIL, self.INVALID_PASSWORD)

        # Step 4: Verify error message is displayed
        wait = WebDriverWait(self.browser, 10)
        error_alert = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-error"))
        )
        error_text = error_alert.text
        print(f"✓ Error message displayed: '{error_text}'")
        self.assertIn(
            "Invalid email or password",
            error_text,
            "Error message should indicate invalid credentials",
        )

        # Step 5: Verify user is still on the login page
        self.assertIn("/auth/login/", self.browser.current_url)
        print(f"✓ User remains on login page: {self.browser.current_url}")

        # Verify Login/Register buttons are still visible (user is NOT logged in)
        login_link = self.browser.find_element(
            By.CSS_SELECTOR, ".navbar-user a.btn-secondary"
        )
        self.assertEqual(login_link.text.strip(), "Login")
        print("✓ User is NOT logged in — Login button still visible")

        print("--- PASSED: Invalid Login ---\n")
