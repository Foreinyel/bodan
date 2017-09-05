# -*- coding: UTF-8 -*-
import sys

reload(sys)
# python默认环境编码时ascii
sys.setdefaultencoding("utf-8")

import scrapy
from scrapy_splash import SplashRequest
import datetime
from adagu_bodan.items import Bodan


class Bodan_500_Spider(scrapy.Spider):
    name = 'bodan500'
    start_urls = ['http://odds.500.com/bodan_jczq_2016-12-31.shtml']
    # start_urls = []
    allowed_domains = ['500.com']

    def __init__(self):
        pass
        # self.init_start_urls()

    # 初始化start urls，爬去2016年全年澳门波胆数据
    def init_start_urls(self):
        begin_date = datetime.datetime.strptime('2016-01-01', "%Y-%m-%d")
        end_date = datetime.datetime.strptime('2016-12-31', '%Y-%m-%d')

        while begin_date <= end_date:
            date_str = begin_date.strftime("%Y-%m-%d")
            url = 'http://odds.500.com/bodan_jczq_' + date_str + '.shtml'
            begin_date += datetime.timedelta(days=1)
            self.start_urls.append(url)

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 0.5})

    def parse(self, response):
        result = response.xpath('//tbody[@id="main-tbody"]')
        # 每五行为一个结果
        count = 1
        bodan = Bodan()
        for tr in result.xpath('.//tr'):
            if count == 1:
                bodan['league'] = tr.xpath('.//td[2]/a/text()').extract_first()
                start_time_str = '2016-' + tr.xpath('.//td[2]/text()').extract_first()
                bodan['start_time'] = datetime.datetime.strptime(start_time_str, '%Y-%m-%d %H:%M')
                bodan['home'] = tr.xpath('.//td[2]/span/a[1]/text()').extract_first()
                bodan['away'] = tr.xpath('.//td[2]/span/a[2]/text()').extract_first()
                score = tr.xpath('.//td[2]/span/text()').extract_first().strip()
                if score.find(':')>0:
                    bodan['home_goal'] = score.split(':')[0]
                    bodan['away_goal'] = score.split(':')[1]
                else:
                    bodan['home_goal'] = None
                    bodan['away_goal'] = None
            if count == 4:
                count2 = 1
                for td in tr.xpath('.//td'):
                    if count2 == 1:
                        key = 'odds_comp'
                    elif count2 == 2:
                        key = 'one_zero'
                    elif count2 == 3:
                        key = 'two_zero'
                    elif count2 == 4:
                        key = 'two_one'
                    elif count2 == 5:
                        key = 'three_zero'
                    elif count2 == 6:
                        key = 'three_one'
                    elif count2 == 7:
                        key = 'three_two'
                    elif count2 == 8:
                        key = 'four_zero'
                    elif count2 == 9:
                        key = 'four_one'
                    elif count2 == 10:
                        key = 'four_two'
                    elif count2 == 11:
                        key = 'four_three'
                    elif count2 == 12:
                        key = 'zero_one'
                    elif count2 == 13:
                        key = 'zero_two'
                    elif count2 == 14:
                        key = 'one_two'
                    elif count2 == 15:
                        key = 'zero_three'
                    elif count2 == 16:
                        key = 'one_three'
                    elif count2 == 17:
                        key = 'two_three'
                    elif count2 == 18:
                        key = 'zero_four'
                    elif count2 == 19:
                        key = 'one_four'
                    elif count2 == 20:
                        key = 'two_four'
                    elif count2 == 21:
                        key = 'three_four'
                    elif count2 == 22:
                        key = 'zero_zero'
                    elif count2 == 23:
                        key = 'one_one'
                    elif count2 == 24:
                        key = 'two_two'
                    elif count2 == 25:
                        key = 'three_three'
                    elif count2 == 26:
                        key = 'four_four'
                    elif count2 == 27:
                        key = 'returns'
                    else:
                        break
                    count2 += 1
                    bodan[key] = td.xpath('.//text()').extract_first()

                yield bodan

            count += 1
            if count == 6:
                count = 1
