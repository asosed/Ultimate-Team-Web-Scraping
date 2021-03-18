import scrapy 
from ultimate_team.items import UtItem

class FutwizSpider(scrapy.Spider):
    name = 'futwiz'
    start_urls = ['https://www.futwiz.com/en/fifa21/players']

    def parse(self, response):
        """
        Scrapy creates scrapy.http.Request objects for each URL in the
        start_urls attribute of the Spider, and assings them the parse method
        of the spider as their callback function
        """
        # Link to the player page
        players = response.xpath('//div[@id="cardview"]//a/@href').getall()
        for player in players:
            yield response.follow(player, callback=self.parse_player) #follow the link and register the parse_player callback to handle the data extraction

        # Link to next page
        next_page = response.xpath('//div[@class="pagination"]//a[contains(text(), "Next")]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)


    def parse_player(self, response):
        item = UtItem()

        item['url'] = response.url
        item['name'] = response.xpath('//div[@class="playerprofile-head"]//h1/text()').get()
        item['nation'] = response.xpath('//div[@class="playerprofile-head"]//a[contains(@href, "nation")]/text()').get()
        item['club'] = response.xpath('//div[@class="playerprofile-head"]//a[contains(@href, "club")]/text()').get()
        item['league'] = response.xpath('//div[@class="playerprofile-head"]//a[contains(@href, "league")]/text()').get()
        item['position'] = response.xpath('//div[contains(@class, "card-21-position")]/text()').get()
        item['global_rate'] = response.xpath('//div[contains(@class, "card-21-rating")]/text()').get()


        # Physical stats
        physical_stats = {}

        physical_stats_labels = response.xpath('//div[@class="playerprofile-db"]/p[2]/text()').getall()
        for label in physical_stats_labels:
            physical_stats[f'{label}'] = response.xpath(f"""//div[contains(@class, "playerprofile-info")]
                                                            //p[contains(text(), "{label}")]
                                                            /parent::*/p/text()""") \
                                                            .get()

        item['physical_stats'] = {key: (int(value.strip()) if value.strip().isdigit() else value)
                                  for key, value in physical_stats.items()}

        # Traits
        traits = response.xpath('//div[contains(@class, "playerprofile-stats")]//div[contains(text(), "Traits")]/text()').get()
        item['traits'] = traits.strip('Traits: ').split(', ')

        # Stats
        stat_val = {}

        # Principal stats
        stat_label_main_list = response.xpath('//div[@class="statBlock"]/div[@class="title"]/child::*[1]/text()').getall()
        for label in stat_label_main_list:
            stat_val[f'{label}'] = response.xpath(f"""//div[@class="row stats"]
                                                      //div[@class="statBlock"]
                                                      //div[contains(text(),"{label}")]
                                                      /following::*/text()""") \
                                                      .get()

        # Remaining stats
        stat_label_list = response.xpath('//div[@class="individual-stat-bar-label"]//text()').getall()
        for label in stat_label_list:
            stat_val[f'{label}'] = response.xpath(f"""//div[@class="row stats"]
                                                      //div[@class="statBlock"]
                                                      //div[contains(text(),"{label}")]
                                                      /following::*/text()""") \
                                                      .get()

        item['stat_val'] = { key.replace('.', ''): int(value) for key, value in stat_val.items() if value.isdigit() }
        

        yield item
