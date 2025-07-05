import pytest
from src.data.processors import clean_job_posting, deduplicate_jobs
from src.analysis.statistics import generate_basic_stats
from src.analysis.trends import generate_time_trends


@pytest.fixture
def empty_and_partial_jobs_fixture():
    return [
        {},
        {"title": "", "company": None, "location": "", "description": None},
        {"title": "QA Engineer"},
    ]


def test_cleaning_with_empty_and_partial_jobs(empty_and_partial_jobs_fixture):
    cleaned = [clean_job_posting(job) for job in empty_and_partial_jobs_fixture]
    assert len(cleaned) == 3
    for job in cleaned:
        assert "title" in job
        assert isinstance(job["title"], str)


def test_deduplication_with_empty_and_partial_jobs(empty_and_partial_jobs_fixture):
    cleaned = [clean_job_posting(job) for job in empty_and_partial_jobs_fixture]
    unique = deduplicate_jobs(cleaned)
    assert isinstance(unique, list)
    assert len(unique) >= 1


def test_analysis_with_empty_and_partial_jobs(empty_and_partial_jobs_fixture):
    cleaned = [clean_job_posting(job) for job in empty_and_partial_jobs_fixture]
    stats = generate_basic_stats(cleaned)
    assert isinstance(stats, dict)
    trends_df = generate_time_trends(cleaned)
    assert isinstance(trends_df, object)
