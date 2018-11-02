# -*- coding: utf-8 -*-
import scrapy


class ToScrapeSpiderXPath(scrapy.Spider):
    name = 'toscrape-xpath'
    start_urls = [
        'https://donors.biotexcom.com/donors-database/001531.html',
    ]

    def parse(self, response):
        self.logger.debug("Starting")
        if "You are already logged in." in response.text or "Wellcome back, !" in response.text:
            self.logger.info("Login successful, starting scraping")
            return self.start_scrape(response)

        self.logger.debug("Not logged, trying to login")
        return self.start_scrape(response)
        # return scrapy.FormRequest.from_response(
        #     response,
        #     formdata={'username': 'john', 'password': 'secret'},
        #     callback=self.after_login
        # )

    def after_login(self, response):
        # check login succeed before going on
        if "The username or password you entered is incorrect." in response.text:
            self.logger.error("Login failed")
            return self.start_scrape(response)
        elif "You are already logged in." in response.text or "Wellcome back, !" in response.text:
            self.logger.info("Login successful, starting scraping")
            return self.start_scrape(response)

    def start_scrape(self, response):
        base_url = response.xpath('string(.//base/@href)').extract_first()
        for pleft in response.xpath('.//div[contains(@class, "profile-left")]'):
            id = pleft.xpath('.//h3[contains(@class, "profile-left-header")]/text()').extract_first()
            # photo = pleft.xpath('string(. // a[ @ href = "#photo"] / img / @ src)').extract_first()
            photo = pleft.xpath('.//h3[contains(@class, "profile-left-header")]/text()').extract_first()
            threedview = pleft.xpath('string(.//div[@id="3dview"]/img/@src)').extract_first()
            video = pleft.xpath('string(.//div[@id="video"]/img/@src)').extract_first()
            yield {
                'id': id,
                'photo': photo,
                '3dview': threedview,
                'video': video
            }

        for pright in response.xpath('.//div[@id="tab1"]'):
            age = pright.xpath('.//ul[@class="list2"][1]/li[1]/text()').extract_first()
            height = pright.xpath('.//ul[@class="list2"][1]/li[2]/text()').extract_first()
            weight = pright.xpath('.//ul[@class="list2"][1]/li[3]/text()').extract_first()
            eye_color = pright.xpath('.//ul[@class="list2"][1]/li[4]/text()').extract_first()
            hair_color = pright.xpath('.//ul[@class="list2"][1]/li[5]/text()').extract_first()
            hair_type = pright.xpath('.//ul[@class="list2"][1]/li[6]/text()').extract_first()
            body_type = pright.xpath('.//ul[@class="list2"][1]/li[7]/text()').extract_first()

        yield {
            'id': id,
            'photo': photo,
            '3dview': threedview,
            'video': video,
            'age': age,
            'height': height,
            'weight': weight,
            'eye_color': eye_color,
            'hair_color': hair_color,
            'hair_type': hair_type,
            'body_type': body_type,
        }

        next_page_url = response.xpath("string(//div[contains(@class, 'breadcrumb')]//a[.//i[contains(@class, 'fa-arrow-right')]]/@href)").extract_first()
        self.logger.debug(next_page_url)
        # return
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(base_url + next_page_url))

