import pandas as pd
from src.utils.logger import get_logger

logger = get_logger(__name__)


def generate_basic_stats(jobs: list) -> dict:
    if not jobs:
        logger.warning("No jobs provided for statistics.")
        return {}

    cleaned_jobs = []
    for job in jobs:
        company = job.get('company') or ''
        title = job.get('title') or ''
        company_clean = company
        if (company and title) and (company.strip().lower().startswith(f"New{title.strip()}".lower()) or company.strip().lower().startswith(title.strip().lower())):
            company_clean = company[len(title):].strip()
        title_cap = title.title() if title else ''
        cleaned_job = job.copy()
        cleaned_job['company'] = company_clean
        cleaned_job['title'] = title_cap
        cleaned_jobs.append(cleaned_job)

    df = pd.DataFrame(cleaned_jobs)
    stats = {'top_titles': df['title'].value_counts().head(10).to_dict(),
             'top_companies': df['company'].value_counts().head(10).to_dict(),
             'jobs_by_location': df['location'].value_counts().head(10).to_dict()}

    numeric_salaries = (
        df['salary']
        .dropna()
        .apply(lambda s: extract_numeric_salary(s))
        .dropna()
    )
    if not numeric_salaries.empty:
        stats['average_salary'] = numeric_salaries.mean()
    else:
        stats['average_salary'] = None

    logger.info(f"Generated statistics: {stats}")
    return stats


def extract_numeric_salary(salary_str: str):
    if not salary_str:
        return None
    import re
    numbers = [float(s.replace(',', '')) for s in re.findall(r'\d[\d,]*', salary_str)]
    if not numbers:
        return None
    return sum(numbers) / len(numbers)
