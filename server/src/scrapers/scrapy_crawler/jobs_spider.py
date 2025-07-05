import scrapy
from src.scrapers.scrapy_crawler.items import JobPostingItem


class JobsSpider(scrapy.Spider):
    name = "jobs"
    allowed_domains = ["indeed.com"]
    start_urls = [
        "https://www.indeed.com/jobs?q=python&l="
    ]

    def parse(self, response):
        job_cards = response.css("div.job_seen_beacon")
        for card in job_cards:
            item = JobPostingItem()
            item['title'] = card.css("h2.jobTitle span::text").get()
            item['company'] = card.css("span.companyName::text").get()
            item['location'] = card.css("div.companyLocation::text").get()
            item['salary'] = card.css("div.salary-snippet span::text").get()
            item['date_posted'] = card.css("span.date::text").get()
            item['description'] = card.css("div.job-snippet").xpath("string()").get()
            item['url'] = response.url
            yield item

        # Pagination
        next_page = response.css("a[aria-label='Next']::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
