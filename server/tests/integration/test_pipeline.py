import os
import pandas as pd

from src.data.processors import clean_job_posting, deduplicate_jobs
from src.analysis.statistics import generate_basic_stats
from src.analysis.trends import generate_time_trends
from src.analysis.reports import generate_report


def test_full_pipeline(tmp_path):
    raw_jobs = [
        {
            "title": "Python Developer",
            "company": "Company A",
            "location": "Remote",
            "salary": "$80,000",
            "date_posted": "1 day ago",
            "description": "Job description.",
            "url": "http://example.com/job1"
        },
        {
            "title": "Python Developer",
            "company": "Company A",
            "location": "Remote",
            "salary": "$80,000",
            "date_posted": "1 day ago",
            "description": "Job description.",
            "url": "http://example.com/job1"
        },
        {
            "title": "Data Engineer",
            "company": "Company B",
            "location": "NYC",
            "salary": "$100,000",
            "date_posted": "2 days ago",
            "description": "Job description.",
            "url": "http://example.com/job2"
        }
    ]

    cleaned = [clean_job_posting(job) for job in raw_jobs]
    unique = deduplicate_jobs(cleaned)

    assert len(unique) == 2

    stats = generate_basic_stats(unique)
    trends_df = generate_time_trends(unique)

    assert isinstance(stats, dict)
    assert not trends_df.empty

    jobs_df = pd.DataFrame(unique)

    os.makedirs(tmp_path / "reports", exist_ok=True)
    generate_report(stats, trends_df, jobs_df, report_name="test_report.html")

    report_file = tmp_path / "reports" / "test_report.html"
    assert report_file.exists() or os.path.isfile(report_file)
