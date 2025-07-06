import requests
import json
from src.scrapers.base_scraper import BaseScraper
from src.utils.logger import get_logger
from src.utils.linkedin_auth import linkedin_auth

logger = get_logger(__name__)


class APIScraper(BaseScraper):
    def __init__(self, proxies=None, max_retries=3, delay_range=(1, 3)):
        super().__init__(proxies, max_retries, delay_range)

    def scrape_jobs(self, api_url, data_mapping, headers=None, source_id=None):
        """
        Scrape jobs from API endpoints that return JSON data.
        
        Args:
            api_url (str): The API URL to fetch data from
            data_mapping (dict): Mapping of job fields to API response fields
            headers (dict): Optional headers for the request
            source_id (str): Source identifier for special handling
            
        Returns:
            list: List of job dictionaries
        """
        logger.info(f"Scraping API: {api_url}")
        
        # Handle LinkedIn authentication
        if source_id == "linkedin_api" and "linkedin.com" in api_url:
            auth_headers = linkedin_auth.get_auth_headers()
            if auth_headers:
                if headers is None:
                    headers = {}
                headers.update(auth_headers)
                logger.info("LinkedIn authentication headers added")
                logger.debug(f"Headers being sent: {headers}")
            else:
                logger.error("Failed to get LinkedIn authentication headers")
                return []
        
        try:
            response = self.make_request(api_url, headers=headers)
            if not response or response.status_code != 200:
                logger.warning(f"Failed to fetch {api_url} with status code: {getattr(response, 'status_code', None)}")
                return []

            # Parse JSON response
            data = response.json()
            
            # Handle different API response structures
            if isinstance(data, list):
                jobs_data = data
            elif isinstance(data, dict) and 'jobs' in data:
                jobs_data = data['jobs']
            elif isinstance(data, dict) and 'results' in data:
                jobs_data = data['results']
            else:
                logger.warning(f"Unexpected API response structure: {type(data)}")
                return []

            jobs = []
            logger.info(f"Found {len(jobs_data)} jobs from API.")

            for idx, job_item in enumerate(jobs_data):
                job_data = {}
                
                # Map API fields to our standard job fields
                for field_name, api_field in data_mapping.items():
                    if api_field in job_item:
                        job_data[field_name] = job_item[api_field]
                    else:
                        job_data[field_name] = None

                # Add source information
                job_data['source'] = 'API'
                
                # Only add jobs that have at least a title
                if job_data.get('title'):
                    jobs.append(job_data)
                    logger.debug(f"[{idx + 1}] Job scraped: {job_data.get('title', 'No title')}")

            logger.info(f"Scraped {len(jobs)} job postings from API: {api_url}")
            return jobs

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response from {api_url}: {e}")
            return []
        except Exception as e:
            logger.error(f"Error scraping API {api_url}: {e}")
            return [] 