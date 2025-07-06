from fastapi import APIRouter, Body
from fastapi.responses import PlainTextResponse, JSONResponse
import subprocess
import json
import os
from src.utils.helpers import load_sources_config
from src.scrapers.static_scraper import StaticScraper
from src.scrapers.selenium_scraper import SeleniumScraper
from src.scrapers.api_scraper import APIScraper
import logging

router = APIRouter(prefix="/api")

@router.get("/")
def read_root():
    return {"status": "API is running"}

@router.post("/test", response_class=PlainTextResponse)
def test():
    try:
        result = subprocess.run(["pytest"], capture_output=True, text=True, check=False)
        return result.stdout + result.stderr
    except Exception as e:
        return PlainTextResponse(f"Test run failed: {str(e)}", status_code=500)

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
            
            logging.info(f"Scraping source: {src['name']} ({src_id})")
            
            if src["type"] == "static":
                url = src["search_url"].replace("{keyword}", keyword)
                selectors = src["selectors"]
                logging.info(f"Static scraping URL: {url}")
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
                url = src["search_url"].replace("{keyword}", keyword)
                selectors = src["selectors"]
                logging.info(f"Dynamic scraping URL: {url}")
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
            elif src["type"] == "api":
                api_url = src["api_url"].replace("{keyword}", keyword)
                data_mapping = src["data_mapping"]
                logging.info(f"API scraping URL: {api_url}")
                scraper = APIScraper()
                scraped = scraper.scrape_jobs(
                    api_url=api_url,
                    data_mapping=data_mapping,
                    source_id=src_id
                )
                for job in scraped:
                    job["source"] = src["name"]
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

@router.get("/linkedin/auth-url")
def get_linkedin_auth_url():
    """Get LinkedIn OAuth authorization URL for manual setup."""
    from src.utils.linkedin_auth import linkedin_auth
    
    auth_url = linkedin_auth.get_authorization_url()
    if auth_url:
        return JSONResponse({
            "auth_url": auth_url,
            "instructions": [
                "1. Copy the authorization URL and open it in your browser",
                "2. Complete the LinkedIn authorization",
                "3. Copy the authorization code from the redirect URL",
                "4. Use the /linkedin/exchange-code endpoint to get your access token"
            ]
        })
    else:
        return JSONResponse({"error": "LinkedIn credentials not configured"}, status_code=400)

@router.post("/linkedin/exchange-code")
def exchange_linkedin_code(payload: dict = Body(...)):
    """Exchange LinkedIn authorization code for access token."""
    from src.utils.linkedin_auth import linkedin_auth
    
    auth_code = payload.get("auth_code")
    if not auth_code:
        return JSONResponse({"error": "Authorization code required"}, status_code=400)
    
    token = linkedin_auth._exchange_code_for_token(auth_code)
    if token:
        return JSONResponse({
            "access_token": token,
            "message": "Token generated successfully. Set LINKEDIN_ACCESS_TOKEN environment variable and restart the application."
        })
    else:
        return JSONResponse({"error": "Failed to exchange code for token"}, status_code=400) 