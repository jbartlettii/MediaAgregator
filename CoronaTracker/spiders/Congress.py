import scrapy


class Congress(scrapy.Spider):
    name = "Congress"

    def start_requests(self):
        # Empty output file
        open("Congress.csv", 'w').close()
        # Only should empty before this spider runs
        urls = [
            'https://www.congress.gov/quick-search/legislation?wordsPhrases=&wordVariants=on&congresses%5B%5D=all'
            '&legislationNumbers=&legislativeAction=&sponsor=on&representative=&senator=&searchResultViewType=compact'
            '&KWICView=false&pageSort=dateOfIntroduction%3Adesc '
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for li in response.css('[class = compact]'):
            self.log(li.get())
            item = {
                'title': li.css('span[class = result-heading] a ::text ').get(),
                'link': li.css('span[class = result-heading] a ::attr(href)').get(),
                'summary': li.css('span.result-title.bottom-padding ::text').get(),
                'sponsor': li.css('span.result-item a ::text').get(),
                'date': li.xpath('//span[3]/span/text()').get(),
                'committee': li.xpath('span[4]/span/text()').get(),
                'latestAction': li.xpath('span[5]/span/text()').get()

            }
            yield item

        return
