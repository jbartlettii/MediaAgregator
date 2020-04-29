import scrapy
from scrapy.spiders import XMLFeedSpider


class FDIC(scrapy.Spider):
    name = "FDIC"

    def start_requests(self):
        # Empty output file
        open("FDIC.csv", 'w').close()
        # Only should empty before this spider runs

        urls = [
            'https://www.fdic.gov/bank/individual/failed/banklist.html'
        ]
        # This collects the failed banklist from the FDIC
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for tr in response.css('tr'):
            self.log(tr.get())
            item = {
                'Bank Name': tr.css('[class = institution] ::text').get(),
                'City': tr.css('[class = city] ::text').get(),
                'State': tr.css('[class = state] ::text').get(),
                'Cert': tr.xpath("td[4]/text()").get(),
                'Acquiring Institution': tr.xpath('td[5]/text()').get(),
                'Closing Date': tr.xpath('td[6]/text()').get()

            }
            yield item

        return
