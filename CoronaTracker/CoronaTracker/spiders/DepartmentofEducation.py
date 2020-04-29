import scrapy
from scrapy.spiders import XMLFeedSpider


class DepartmentofEducation(XMLFeedSpider):
    name = "DepartmentofEducation"

    def start_requests(self):
        # Empty output file
        open("DepartmentofEducation.json", 'w').close()
        # Only should empty before this spider runs
        urls = [
            'https://www.ed.gov/news/press-releases/feed'

        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    itertag = 'item'

    def parse_node(self, response, node):
        self.logger.info('Hi, this is a <%s> node!: %s', self.itertag, ''.join(node.extract()))

        item = {'title': node.xpath('title/text()', ).get(),
                'link': node.xpath('link/text()').get(),
                'description': node.xpath('description/text()').get(),
                'pubDate': node.xpath('pubDate/text()').get()}

        return item
