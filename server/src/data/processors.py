import re
from src.utils.logger import get_logger

logger = get_logger(__name__)


def normalize_title(title: str) -> str:
    if not title:
        return ""
    title = title.strip().lower()
    title = re.sub(r'[^\w\s]', '', title)
    return title


def clean_job_posting(job: dict) -> dict:
    cleaned = {'title': normalize_title(job.get('title')),
               'company': job.get('company', '').strip() if job.get('company') else None,
               'location': job.get('location', '').strip() if job.get('location') else None,
               'salary': job.get('salary', '').strip() if job.get('salary') else None,
               'date_posted': job.get('date_posted', '').strip() if job.get('date_posted') else None,
               'description': job.get('description', '').strip() if job.get('description') else None,
               'url': job.get('url', '').strip() if job.get('url') else None}
    logger.debug(f"Cleaned job: {cleaned}")
    return cleaned


def deduplicate_jobs(jobs: list) -> list:
    seen = set()
    unique_jobs = []
    for job in jobs:
        key = (job['title'], job['company'], job['location'])
        if key not in seen:
            seen.add(key)
            unique_jobs.append(job)
    logger.info(f"Deduplicated jobs: {len(jobs)} -> {len(unique_jobs)}")
    return unique_jobs
