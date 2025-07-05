import random
import time
import requests
from requests.exceptions import RequestException
from src.utils.logger import get_logger
from src.utils.helpers import random_delay

logger = get_logger(__name__)


class BaseScraper:
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "Mozilla/5.0 (X11; Linux x86_64)",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2)",
    ]

    def __init__(self, proxies=None, max_retries=3, delay_range=(1, 3)):
        self.session = requests.Session()
        self.proxies = proxies or []
        self.max_retries = max_retries
        self.delay_range = delay_range

    def get_random_user_agent(self):
        return random.choice(self.USER_AGENTS)

    def get_random_proxy(self):
        if not self.proxies:
            return None
        return random.choice(self.proxies)

    def make_request(self, url, headers=None, params=None, method='GET'):
        retries = 0
        while retries < self.max_retries:
            try:
                ua = self.get_random_user_agent()
                proxy = self.get_random_proxy()

                request_headers = headers or {}
                request_headers['User-Agent'] = ua

                logger.info(f"[Request] {url} | Attempt: {retries + 1}")
                response = self.session.request(
                    method=method,
                    url=url,
                    headers=request_headers,
                    params=params,
                    proxies={"http": proxy, "https": proxy} if proxy else None,
                    timeout=15
                )

                if response.status_code == 200:
                    random_delay(self.delay_range)
                    return response
                else:
                    logger.warning(f"Non-200 status: {response.status_code} | URL: {url}")
                    retries += 1
                    time.sleep(2 ** retries)  # exponential backoff
            except RequestException as e:
                logger.error(f"Request failed: {e}")
                retries += 1
                time.sleep(2 ** retries)
        logger.error(f"Failed to fetch URL after {self.max_retries} retries: {url}")
        return None
