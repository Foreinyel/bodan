# -*- coding: UTF-8 -*-
import sys

reload(sys)
# python默认环境编码时ascii
sys.setdefaultencoding("utf-8")

import scrapy
import re
from scrapy_splash import SplashRequest
import datetime
import traceback
from scrapy import signals
from adagu_bodan.items import Match500TeamStanding
from adagu_bodan.items import Match500History
from adagu_bodan.items import Match500Recent
from adagu_bodan.items import Match500Ouzhi
from adagu_bodan.items import Match500Rangqiu
from adagu_bodan.items import Match500Daxiao
from adagu_bodan.items import Match500Bifen
from adagu_bodan.model import loadSession
from adagu_bodan.model.spider_crawl_err_urls import SpiderCrawlErrUrls
from adagu_bodan.model.match_500 import Match500
from sqlalchemy import distinct
from sqlalchemy import func
from adagu_bodan.model.match_500_recent import Match500Recent as Match500RecentModel


class Match_500_Extra_Spider(scrapy.Spider):
    name = "match500extra"
    allowed_domains = ['500.com']

    # start_urls = ['http://odds.500.com/fenxi/shuju-518987.shtml']
    start_urls = []
    spider_errs = []

    def __init__(self):
        self.init_start_urls()
        # pass

    def start_requests(self):
        for url in self.start_urls:
            print url
            yield SplashRequest(url, self.parse, args={'wait': 0.5})

    def spider_closed(self, spider):
        self.save_errs()

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(Match_500_Extra_Spider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def init_start_urls(self):
        session = loadSession()
        # matches = session.query(Match500.id).all()
        matchids = session.query(distinct(Match500RecentModel.match_id).label('match_id')).group_by(Match500RecentModel.match_id).having(func.count(1) != 40).all()
        for matchid in matchids:
            # print matchid[0]
            # print dir(matchid)
            url = self.gen_match_urls_with_id(str(matchid[0]))
            self.start_urls.append(url)
            # count = 500
            # offset = 0
            # while count == 500:
            #     matches = session.query(Match500.id).limit(500).offset(offset).all()
            #     count = len(matches)
            #     offset += 500
            #     print count
            #     for match in matches:
            #         url = self.gen_match_urls_with_id(str(match.id))
            #         self.start_urls.append(url)


            # 保存异常

    def add_err_urls(self, url, txt=None):

        err = SpiderCrawlErrUrls()
        err.spider_name = self.name
        err.req_url = url
        err.txt = txt
        self.spider_errs.append(err)

    def save_errs(self):
        session = loadSession()
        for err in self.spider_errs:
            session.add(err)
        session.commit()

    # 根据比赛ID生成对应的链接
    def gen_match_urls_with_id(self, match_id):
        prefix = "http://odds.500.com/fenxi/"
        # 1 数据分析
        shuju_url = prefix + "shuju-" + match_id + ".shtml"
        return shuju_url

    def parse(self, response):

        url = response.url

        if url.find('/fenxi/shuju-') >= 0:
            return self.parse_shuju(response)

    # 数据分析

    def parse_shuju(self, response):

        try:
            match_id = response.url.split('shuju-')[1].split('.')[0]
            content = response.xpath('//div[@class="odds_content"]')
            for div in content.xpath('./div'):
                title = div.xpath('./div[@class="M_title"]/h4/text()').extract_first()
                if not title:
                    continue
                # 近期战绩
                if title.find('近期战绩') >= 0:
                    # 1、主队近十场战绩
                    zhanji_01 = div.xpath(
                        './/div[@id="team_zhanji_1"]/form[@id="zhanji_01"]/div[@class="M_content"]/table/tbody')
                    for tr in zhanji_01.xpath('./tr'):
                        tr_class = tr.xpath('./@class').extract_first()
                        if tr_class == 'tr1' or tr_class == 'tr2':
                            recent = Match500Recent()
                            recent['match_id'] = match_id
                            recent['team_type'] = 'home'
                            recent['recent_type'] = 'all'
                            recent['league_name'] = tr.xpath('./td[1]/a/text()').extract_first()
                            start_date = '20' + tr.xpath('./td[2]/text()').extract_first()
                            recent['start_date'] = datetime.datetime.strptime(start_date, '%Y-%m-%d')
                            recent['recent_url'] = tr.xpath('./td[3]/a/@href').extract_first()
                            recent['home'] = tr.xpath('./td[3]/a/span[1]/text()').extract_first()
                            recent['away'] = tr.xpath('./td[3]/a/span[2]/text()').extract_first()
                            home_goal = tr.xpath('./td[3]/a/em').extract_first()
                            home_goal, no = re.subn('<[^\d:]*>', '', home_goal)
                            recent['home_goal'] = home_goal.split(':')[0]
                            recent['away_goal'] = home_goal.split(':')[1]
                            yield recent


        except:
            self.add_err_urls(response.url, traceback.format_exc())
