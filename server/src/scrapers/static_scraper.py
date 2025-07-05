from bs4 import BeautifulSoup
from src.scrapers.base_scraper import BaseScraper
from src.utils.logger import get_logger

logger = get_logger(__name__)


class StaticScraper(BaseScraper):
    def __init__(self, proxies=None, max_retries=3, delay_range=(1, 3)):
        super().__init__(proxies, max_retries, delay_range)

    def scrape_jobs(self, url, job_selector, fields, headers=None):
        logger.info(f"Scraping static page: {url}")
        response = self.make_request(url, headers=headers)
        if not response or response.status_code != 200:
            logger.warning(f"Failed to fetch {url} with status code: {getattr(response, 'status_code', None)}")
            return []

        with open("static_debug.html", "w", encoding="utf-8") as f:
            f.write(response.text)

        soup = BeautifulSoup(response.content, "html.parser")
        job_elements = soup.select(job_selector)
        jobs = []

        logger.info(f"Found {len(job_elements)} jobs on page.")

        for idx, elem in enumerate(job_elements):
            job_data = {}
            for field_name, field in fields.items():
                if field_name == "company" and field == "span.listing-company-name":
                    target = elem.select_one(field)
                    company = None
                    if target:
                        for child in target.children:
                            if getattr(child, 'name', None) == 'br':
                                company = child.next_sibling
                                if company:
                                    company = company.strip()
                                break
                        if not company:
                            company = target.get_text(strip=True)
                    job_data[field_name] = company
                elif isinstance(field, dict) and field.get("type") == "multiple":
                    targets = elem.select(field["selector"])
                    texts = [t.get_text(strip=True) for t in targets]
                    job_data[field_name] = texts
                else:
                    target = elem.select_one(field)
                    job_data[field_name] = target.get_text(strip=True) if target else None

            if "employment_type" in job_data and isinstance(job_data["employment_type"], list):
                salary_text = next(
                    (t for t in job_data["employment_type"] if "$" in t),
                    None
                )
                job_data["salary"] = salary_text

            if job_data.get('company') and job_data.get('title'):
                company = job_data['company']
                title = job_data['title']
                if company.startswith(title):
                    job_data['company'] = company[len(title):].strip()

            jobs.append(job_data)
            logger.debug(f"[{idx + 1}] Job scraped: {job_data}")

        logger.info(f"Scraped {len(jobs)} job postings from: {url}")
        return jobs
