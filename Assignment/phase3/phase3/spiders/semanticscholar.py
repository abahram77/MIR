import scrapy
from json import dumps


class SemanticScholarSpider(scrapy.Spider):
    name = 'semanticscholar'

    TITLE = "//h1[@data-selenium-selector='paper-detail-title']/text()" #DONE
    DATE = "//span[@data-selenium-selector='paper-year']/span/span/text()" #DONE
    CITATIONS = "//div[@data-selenium-selector='citation']/div/h2/a/@href" #DONE
    AUTHORS = "//span[@data-selenium-selector='paper-meta-subhead']/span/span/a/span/span/text()" #DONE
    MORE_AUTHORS = "//span[@data-selenium-selector='paper-meta-subhead']/span/span/span/span[@class='more-authors-label']" #DONE
    ABSTRACT = "//meta[@name='description']/@content" #DONE
    MAXIMUM = 2000 #DONE


    def __init__(self):
        self.start_urls = [
            'https://www.semanticscholar.org/paper/The-Lottery-Ticket-Hypothesis%3A-Training-Pruned-Frankle-Carbin/f90720ed12e045ac84beb94c27271d6fb8ad48cf',
            'https://www.semanticscholar.org/paper/Attention-is-All-you-Need-Vaswani-Shazeer/204e3073870fae3d05bcbc2f6a8e263d9b72e776',
            'https://www.semanticscholar.org/paper/BERT%3A-Pre-training-of-Deep-Bidirectional-for-Devlin-Chang/df2b0e26d0599ce3e70df8a9da02e51594e0e992'   
        ]
        self.crawled = set()

    def start_requests(self):
        urls = self.start_urls
        self.crawled.update(url for url in urls)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        url = response.url
        data = dict()
        id = url.split('/')[-1]
        domain = url.split('/')[2]
        data['id'] = id
        data['title'] = response.xpath(self.TITLE).get()
        data['date'] = response.xpath(self.DATE).get()
        data['citations'] = response.xpath(self.CITATIONS).getall()
        data['authors'] = response.xpath(self.AUTHORS).getall()
        data['abstract'] = response.xpath(self.ABSTRACT).get()
        with open('./data/{}.json'.format(id), 'w') as f:
            f.write(dumps(data))
        counter = 0
        for citation in data['citations']:
            if len(self.crawled) <= self.MAXIMUM:
                print('citation', citation)
                url_to_crawl = citation
                if counter < 10:
                    if url_to_crawl not in self.crawled:
                        counter += 1
                        self.crawled.add(url_to_crawl)
                        yield response.follow(url_to_crawl, callback=self.parse)

                    else:
                        continue
                else:
                    return

            else:
                return
        return


