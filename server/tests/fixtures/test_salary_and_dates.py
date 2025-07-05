import pytest
from src.analysis.statistics import extract_numeric_salary
from src.analysis.trends import parse_date


@pytest.fixture
def salary_fixture():
    return [
        "$70,000 - $80,000 per year",
        "USD 120000 annually",
        "€50k",
        None,
        "Not disclosed"
    ]


@pytest.fixture
def date_fixture():
    return [
        "today",
        "2 days ago",
        "April 10, 2025",
        "invalid date",
        None
    ]


def test_salary_parsing_with_fixture(salary_fixture):
    for salary_str in salary_fixture:
        result = extract_numeric_salary(salary_str)
        assert result is None or isinstance(result, (int, float))


def test_date_parsing_with_fixture(date_fixture):
    for date_str in date_fixture:
        parsed = parse_date(date_str) if date_str else None
        assert parsed is None or hasattr(parsed, "strftime")  # should return date or None
