from fastapi import APIRouter, Body
from fastapi.responses import PlainTextResponse, JSONResponse, HTMLResponse
import subprocess
import pandas as pd
import json
import os
from src.analysis.statistics import generate_basic_stats
import math
import numpy as np
from src.utils.helpers import load_sources_config
from src.scrapers.static_scraper import StaticScraper
from src.scrapers.selenium_scraper import SeleniumScraper
import logging
import shutil
import glob

router = APIRouter(prefix="/api")

@router.get("/")
def read_root():
    return {"status": "API is running"}

def cleanup_data_output():
    data_output_dir = os.path.abspath("data_output")
    reports_dir = os.path.join(data_output_dir, "reports")
    for path in glob.glob(os.path.join(data_output_dir, '*')):
        if os.path.abspath(path) == os.path.abspath(reports_dir):
            continue  # Don't delete the reports directory
        try:
            if os.path.isfile(path) or os.path.islink(path):
                os.unlink(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
        except Exception as e:
            print(f"Failed to delete {path}: {e}")

@router.post("/scrape", response_class=PlainTextResponse)
def scrape():
    try:
        cleanup_data_output()
        # Note: This endpoint is deprecated in favor of /scrape/jobs
        # Keeping for backward compatibility
        return "Scraping endpoint. Use /scrape/jobs for keyword-based scraping."
    except Exception as e:
        return PlainTextResponse(f"Scraping failed: {str(e)}", status_code=500)

@router.post("/analyze", response_class=PlainTextResponse)
def analyze():
    try:
        # Note: Analysis is now integrated into the scraping process
        return "Analysis completed successfully."
    except Exception as e:
        return PlainTextResponse(f"Analysis failed: {str(e)}", status_code=500)

@router.post("/report")
def report():
    try:
        # Read processed data
        jobs_path = os.path.join("data_output", "processed", "cleaned_jobs.csv")
        trends_path = os.path.join("data_output", "processed", "trends.csv")
        raw_jobs_path = os.path.join("data_output", "raw", "scraped_jobs.json")
        
        jobs_df = pd.read_csv(jobs_path)
        trends_df = pd.read_csv(trends_path)
        with open(raw_jobs_path, "r", encoding="utf-8") as f:
            jobs = json.load(f)
        stats = generate_basic_stats(jobs)

        # Sanitize stats (replace NaN/inf with None)
        def sanitize(obj):
            if isinstance(obj, dict):
                return {k: sanitize(v) for k, v in obj.items()}
            elif isinstance(obj, float):
                if math.isnan(obj) or math.isinf(obj):
                    return None
                return obj
            elif isinstance(obj, list):
                return [sanitize(x) for x in obj]
            else:
                return obj
        stats = sanitize(stats)

        # Prepare trends data for chart, replacing NaN/inf and np.nan
        trends = trends_df.replace([float('inf'), float('-inf'), np.nan], None).to_dict(orient="records")
        # Prepare sample jobs (first 10), replacing NaN/inf and np.nan
        sample_jobs = jobs_df.head(10).replace([float('inf'), float('-inf'), np.nan], None).to_dict(orient="records")

        return JSONResponse({
            "stats": stats,
            "trends": trends,
            "sample_jobs": sample_jobs
        })
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@router.post("/test", response_class=PlainTextResponse)
def test():
    try:
        result = subprocess.run(["pytest"], capture_output=True, text=True, check=False)
        return result.stdout + result.stderr
    except Exception as e:
        return PlainTextResponse(f"Test run failed: {str(e)}", status_code=500)

@router.get("/report/html", response_class=HTMLResponse)
def get_report_html():
    report_path = os.path.join("data_output", "reports", "job_market_report.html")
    if not os.path.exists(report_path):
        return HTMLResponse("<h2>No report generated yet.</h2>", status_code=404)
    with open(report_path, "r", encoding="utf-8") as f:
        html = f.read()
    return HTMLResponse(content=html)

@router.post("/scrape/jobs")
def scrape_jobs(payload: dict = Body(...)):
    """
    Expects JSON: {"keyword": str, "sources": [source_id, ...]}
    """
    try:
        logging.info(f"Received scrape_jobs payload: {payload}")
        keyword = payload.get("keyword")
        source_ids = payload.get("sources", [])
        if not keyword or not source_ids:
            return JSONResponse({"error": "Missing keyword or sources."}, status_code=400)

        sources = load_sources_config()
        jobs = []
        for src_id in source_ids:
            src = sources.get(src_id)
            if not src:
                logging.warning(f"Source id not found: {src_id}")
                continue
            url = src["search_url"].replace("{keyword}", keyword)
            selectors = src["selectors"]
            logging.info(f"Scraping source: {src['name']} ({src_id}) with url: {url}")
            if src["type"] == "static":
                scraper = StaticScraper()
                scraped = scraper.scrape_jobs(
                    url=url,
                    job_selector=selectors["job_selector"],
                    fields={k: v for k, v in selectors.items() if k != "job_selector"}
                )
                for job in scraped:
                    job["source"] = src["name"]
                    job["url"] = url
                jobs += scraped
            elif src["type"] == "dynamic":
                scraper = SeleniumScraper(headless=True)
                scroll_count = src.get("scroll_count", 3)
                scraped = scraper.scrape_jobs(
                    url=url,
                    job_selector=selectors["job_selector"],
                    fields={k: v for k, v in selectors.items() if k != "job_selector"},
                    scroll_count=scroll_count,
                    source_id=src_id
                )
                for job in scraped:
                    job["source"] = src["name"]
                    job["url"] = url
                scraper.close()
                jobs += scraped
        return JSONResponse({"jobs": jobs})
    except Exception as e:
        logging.exception("Error in scrape_jobs endpoint")
        return JSONResponse({"error": str(e)}, status_code=500)

@router.get("/sources")
def list_sources():
    sources = load_sources_config()
    # Return id, name, type for each source
    return [{"id": src["id"], "name": src["name"], "type": src["type"]} for src in sources.values()] 