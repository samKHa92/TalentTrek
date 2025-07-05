import pytest
from src.data.processors import clean_job_posting, deduplicate_jobs
from src.analysis.statistics import generate_basic_stats
from src.analysis.trends import generate_time_trends


@pytest.fixture
def messy_jobs_fixture():
    return [
        {
            "title": "  PYTHON  DEVELOPER!!!  ",
            "company": "  Test Co ",
            "location": " Remote ",
            "salary": None,
            "date_posted": "today",
            "description": " A messy job posting. ",
            "url": " http://example.com/job1 "
        },
        {
            "title": "python developer",
            "company": "Test Co",
            "location": "Remote",
            "salary": "",
            "date_posted": "today",
            "description": " Another messy job posting.",
            "url": "http://example.com/job1"
        }
    ]


def test_cleaning_and_deduplication_with_fixture(messy_jobs_fixture):
    cleaned = [clean_job_posting(job) for job in messy_jobs_fixture]
    assert cleaned[0]["title"] == "python developer"
    assert cleaned[0]["company"] == "Test Co"
    assert cleaned[0]["url"] == "http://example.com/job1"

    unique = deduplicate_jobs(cleaned)
    assert len(unique) == 1  # Should deduplicate identical title+company+location


def test_analysis_with_fixture(messy_jobs_fixture):
    cleaned = [clean_job_posting(job) for job in messy_jobs_fixture]
    unique = deduplicate_jobs(cleaned)

    stats = generate_basic_stats(unique)
    assert "top_titles" in stats
    assert stats["top_titles"].get("python developer") == 1

    trends_df = generate_time_trends(unique)
    assert not trends_df.empty
