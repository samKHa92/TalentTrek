import scrapy


class JobPostingItem(scrapy.Item):
    title = scrapy.Field()
    company = scrapy.Field()
    location = scrapy.Field()
    salary = scrapy.Field()
    date_posted = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
