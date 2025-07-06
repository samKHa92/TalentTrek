from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import os
from dotenv import load_dotenv

from src.scrapers.base_scraper import BaseScraper
from src.utils.logger import get_logger
from src.utils.helpers import random_delay

logger = get_logger(__name__)


class SeleniumScraper(BaseScraper):
    def __init__(self, headless=True, proxies=None, max_retries=3, delay_range=(1, 3)):
        load_dotenv()
        super().__init__(proxies, max_retries, delay_range)
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-images")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        # Use webdriver-manager to install and set up the right chromedriver
        try:
            chromedriver_dir = os.path.dirname(ChromeDriverManager().install())
            logger.info(f"ChromeDriver directory: {chromedriver_dir}")
            chromedriver_path = os.path.join(chromedriver_dir, "chromedriver")
            
            if not os.path.exists(chromedriver_path):
                logger.error(f"ChromeDriver binary not found at: {chromedriver_path}")
                raise FileNotFoundError(f"ChromeDriver not found at {chromedriver_path}")
            
            logger.info(f"Using ChromeDriver: {chromedriver_path}")
            try:
                os.chmod(chromedriver_path, 0o755)
            except Exception as e:
                logger.warning(f"Could not set executable permissions: {e}")
            
            self.driver = webdriver.Chrome(
                service=Service(chromedriver_path),
                options=chrome_options
            )
        except Exception as e:
            logger.error(f"Failed to initialize Chrome driver: {e}")
            # Fallback: try without specifying the path
            try:
                self.driver = webdriver.Chrome(options=chrome_options)
                logger.info("Chrome driver initialized with fallback method")
            except Exception as fallback_error:
                logger.error(f"Fallback Chrome driver initialization also failed: {fallback_error}")
                raise

    def login_linkedin(self):
        email = os.environ.get('LINKEDIN_EMAIL')
        password = os.environ.get('LINKEDIN_PASSWORD')
        if not email or not password:
            print("LinkedIn credentials not set in environment variables.")
            return False
        print("Logging in to LinkedIn...")
        self.driver.get("https://www.linkedin.com/login")
        try:
            self.driver.find_element("id", "username").send_keys(email)
            self.driver.find_element("id", "password").send_keys(password)
            self.driver.find_element("xpath", "//button[@type='submit']").click()
            time.sleep(5)  # Wait for login to complete
            print("LinkedIn login attempted.")
            return True
        except Exception as e:
            print("LinkedIn login failed:", e)
            return False

    def scrape_jobs(self, url, job_selector, fields, scroll_count=3, source_id=None):
        # If scraping LinkedIn, perform login first
        if source_id == 'linkedin':
            self.login_linkedin()
        logger.info(f"Opening dynamic page: {url}")
        try:
            self.driver.get(url)
            time.sleep(3)  # wait for initial content

            if source_id == 'linkedin':
                max_attempts = 15
                attempts = 0
                last_height = self.driver.execute_script("return document.body.scrollHeight")
                while attempts < max_attempts:
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)
                    new_height = self.driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        attempts += 1
                    else:
                        attempts = 0
                        last_height = new_height
                logger.debug(f"Dynamic scroll for LinkedIn completed after {max_attempts} attempts or no new content.")
            else:
                for i in range(scroll_count):
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    random_delay(self.delay_range)
                    logger.debug(f"Scrolled page {i + 1}/{scroll_count} times.")

            page_source = self.driver.page_source

            soup = BeautifulSoup(page_source, "html.parser")
            job_elements = soup.select(job_selector)
            jobs = []

            logger.info(f"Found {len(job_elements)} jobs on dynamic page.")

            for idx, elem in enumerate(job_elements):
                job_data = {}
                for field_name, selector in fields.items():
                    target = elem.select_one(selector)
                    # Special handling for LinkedIn job title to avoid duplicate text
                    if field_name == "title" and selector == ".artdeco-entity-lockup__title a":
                        if target:
                            span = target.find("span", attrs={"aria-hidden": "true"})
                            job_data[field_name] = span.get_text(strip=True) if span else target.get_text(strip=True)
                        else:
                            job_data[field_name] = None
                    else:
                        job_data[field_name] = target.get_text(strip=True) if target else None
                # Remove title from start of company if present
                if job_data.get('company') and job_data.get('title'):
                    company = job_data['company']
                    title = job_data['title']
                    if company.startswith(title):
                        job_data['company'] = company[len(title):].strip()
                jobs.append(job_data)
                logger.debug(f"[{idx + 1}] Job scraped: {job_data}")

            logger.info(f"Scraped {len(jobs)} job postings from dynamic page: {url}")
            return jobs

        except WebDriverException as e:
            logger.error(f"Selenium error: {e}")
            return []

    def close(self):
        logger.info("Closing Selenium WebDriver.")
        self.driver.quit()
