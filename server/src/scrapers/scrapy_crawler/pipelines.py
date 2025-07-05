import logging


class JobPipeline:
    @staticmethod
    def process_item(item, spider):
        logging.info(f"Job scraped: {item['title']} at {item['company']}")
        return item
