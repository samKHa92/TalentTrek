import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from jinja2 import Environment, FileSystemLoader
from src.utils.logger import get_logger
import shutil
import glob

logger = get_logger(__name__)

REPORTS_DIR = "data_output/reports"


def generate_report(stats: dict, trends_df: pd.DataFrame, jobs_df: pd.DataFrame, report_name="job_market_report.html"):
    # Clean up old data first (except the report to be generated)
    report_path = os.path.join(REPORTS_DIR, report_name)
    report_abspath = os.path.abspath(report_path)
    data_output_dir = os.path.abspath(os.path.join(REPORTS_DIR, '..'))
    for path in glob.glob(os.path.join(data_output_dir, '*')):
        if os.path.abspath(path) == report_abspath:
            continue  # Don't delete the report
        try:
            if os.path.isfile(path) or os.path.islink(path):
                os.unlink(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
        except Exception as e:
            logger.error(f"Failed to delete {path}: {e}")
    # Explicitly remove scraped_jobs.json and cleaned_jobs.csv if they exist
    for f in [
        os.path.join(data_output_dir, 'raw', 'scraped_jobs.json'),
        os.path.join(data_output_dir, 'processed', 'cleaned_jobs.csv'),
        os.path.join(data_output_dir, 'processed', 'trends.csv'),
    ]:
        try:
            if os.path.exists(f):
                os.unlink(f)
        except Exception as e:
            logger.error(f"Failed to delete {f}: {e}")

    os.makedirs(REPORTS_DIR, exist_ok=True)
    charts = []

    if not trends_df.empty:
        plt.figure(figsize=(10, 6))
        sns.lineplot(x="date_posted_norm", y="job_count", data=trends_df)
        plt.title("Jobs Posted Over Time")
        plt.xlabel("Date")
        plt.ylabel("Number of Jobs")
        trend_chart_path = os.path.join(REPORTS_DIR, "trend_chart.png")
        plt.tight_layout()
        plt.savefig(trend_chart_path)
        plt.close()
        charts.append("trend_chart.png")
        logger.info(f"Saved trends chart: {trend_chart_path}")
    else:
        logger.warning("No trends data to generate trend chart.")

    csv_path = os.path.join(REPORTS_DIR, "jobs_data.csv")
    jobs_df.to_csv(csv_path, index=False)
    logger.info(f"Saved jobs data CSV: {csv_path}")

    env = Environment(loader=FileSystemLoader(searchpath="templates"))
    template = env.get_template("report_template.html")
    html_content = template.render(
        stats=stats,
        charts=charts,
        jobs_table=jobs_df.head(20).to_html(index=False, classes="table table-striped"),
    )
    report_path = os.path.join(REPORTS_DIR, report_name)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    logger.info(f"Generated HTML report: {report_path}")
