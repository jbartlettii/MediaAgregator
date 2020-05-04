import scrapy


class Treasury(scrapy.Spider):
    name = "Treasury"

    def start_requests(self):
        # Empty output file
        open("Treasury.json", 'w').close()
        # Only should empty before this spider runs
        urls = [
            'https://home.treasury.gov/news/press-releases'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def getFirstParagraph(self, response, title, link, date):
        self.log('\n \n')
        self.log(response.cb_kwargs)
        description = response.css('.field--name-field-news-body > p:nth-child(2) ::text').get()

        if description == "WASHINGTON":
            description = response.css('.field--name-field-news-body > p:nth-child(3) ::text').get()
        item = {
            'title': title,
            'link': link,
            "date": date,
            'description': description
        }
        return item

    def parse(self, response):
        for div in response.css('.content--2col__body > div'):
            # self.log(div.get())
            url1 = "https://home.treasury.gov" + div.css('h3[class = featured-stories__headline] a ::attr(href)').get()

            item = {
                'title': div.css('h3[class = featured-stories__headline] a ::text ').get(),
                'link': url1,
                'date': div.xpath('.//span[1]/time/text()').get(),
            }
            yield scrapy.Request(url1, self.getFirstParagraph, cb_kwargs=item)
            # TODO: Follow the links in href and grab the first paragrpah
            # yield item
        return
