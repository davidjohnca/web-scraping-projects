import scrapy


class MySpiderSpider(scrapy.Spider):
    name = "my_spider"
    allowed_domains = ["zoopla.co.uk"]
    start_urls = ["https://www.zoopla.co.uk/for-sale/property/london/?q=London&results_sort=newest_listings&search_source=home"]

    def parse(self, response):
        
        for listing_url in response.css("._1lw0o5c2::attr(href)").extract():
            yield response.follow(listing_url, callback=self.parse_listing)

        next_page_url = response.css("._14bi3x31n._14bi3x3s a::attr(href)").extract_first()

        if next_page_url:
            yield response.follow(next_page_url, callback=self.parse)
    
    def parse_listing(self, response):
        yield {
            "title": response.css("._194zg6t7._18cwln11::text").extract_first(),
            "price": response.css("._194zg6t4._18cwln10::text").extract_first(),
            "location": response.css("._18cwln12._194zg6t8::text").extract_first(),
            "bedrooms": response.css("._14bi3x30::text").extract_first(),
        }
        