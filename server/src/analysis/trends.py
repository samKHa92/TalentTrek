import pandas as pd
from datetime import datetime
from src.utils.logger import get_logger

logger = get_logger(__name__)


def generate_time_trends(jobs: list) -> pd.DataFrame:
    if not jobs:
        logger.warning("No jobs provided for trend analysis.")
        return pd.DataFrame()

    df = pd.DataFrame(jobs)
    if 'date_posted' not in df.columns:
        logger.warning("No date_posted field found in data.")
        return pd.DataFrame()

    df['date_posted_norm'] = df['date_posted'].apply(parse_date)
    df = df.dropna(subset=['date_posted_norm'])

    if df.empty:
        logger.warning("No valid dates found after parsing.")
        return pd.DataFrame()

    trend = df.groupby('date_posted_norm').size().reset_index(name='job_count')
    trend = trend.sort_values(by='date_posted_norm')
    logger.info(f"Generated time trends:\n{trend}")
    return trend


def parse_date(date_str: str):
    try:
        date_str = date_str.strip().lower()
        today = datetime.now().date()
        if date_str in ["today"]:
            return today
        elif "day" in date_str:
            days_ago = int(date_str.split()[0])
            return today - pd.Timedelta(days=days_ago)
        elif "hour" in date_str:
            return today
        else:
            return pd.to_datetime(date_str, errors='coerce').date()
    except Exception as e:
        logger.debug(f"Failed to parse date '{date_str}': {e}")
        return None
