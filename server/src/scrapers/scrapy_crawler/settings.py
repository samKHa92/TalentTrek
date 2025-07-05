BOT_NAME = "scrapy_crawler"

SPIDER_MODULES = ["src.scrapers.scrapy_crawler.spiders"]
NEWSPIDER_MODULE = "src.scrapers.scrapy_crawler.spiders"

ROBOTSTXT_OBEY = True
DOWNLOAD_DELAY = 2

ITEM_PIPELINES = {"src.scrapers.scrapy_crawler.pipelines.JobPipeline": 300}

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
