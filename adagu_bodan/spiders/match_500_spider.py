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
from adagu_bodan.items import Match500
from adagu_bodan.items import Match500TeamStanding
from adagu_bodan.items import Match500History
from adagu_bodan.items import Match500Recent
from adagu_bodan.items import Match500Ouzhi
from adagu_bodan.items import Match500Rangqiu
from adagu_bodan.items import Match500Daxiao
from adagu_bodan.items import Match500Bifen
from adagu_bodan.model import loadSession
from adagu_bodan.model.spider_crawl_err_urls import SpiderCrawlErrUrls


class Match_500_Spider(scrapy.Spider):
    name = "match500"
    allowed_domains = ['500.com']
    # start_urls = ['http://odds.500.com/fenxi/daxiao-556541.shtml?ctype=2']

    # start_urls = ['http://odds.500.com/bodan_jczq_2016-01-16.shtml']

    start_urls = []

    spider_errs = []

    def __init__(self):
        self.init_start_urls()
        pass

    def spider_closed(self,spider):
        self.save_errs()

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(Match_500_Spider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def init_start_urls(self):
        begin_date = datetime.datetime.strptime('2017-04-01', "%Y-%m-%d")
        end_date = datetime.datetime.strptime('2017-08-31', '%Y-%m-%d')

        while begin_date <= end_date:
            date_str = begin_date.strftime("%Y-%m-%d")
            url = 'http://odds.500.com/bodan_jczq_' + date_str + '.shtml'
            begin_date += datetime.timedelta(days=1)
            self.start_urls.append(url)

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 0.5})

    # 保存异常
    def add_err_urls(self,url,txt=None):
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

    def parse(self, response):
        url = response.url
        if url.find('/bodan_jczq_') >= 0:
            return self.parse_daily_matches(response)
        if url.find('/fenxi/shuju-') >= 0:
            return self.parse_shuju(response)
        if url.find('/fenxi/ouzhi-') >= 0:
            return self.parse_ouzhi(response)
        if url.find('fenxi/rangqiu-') >=0:
            return self.parse_rangqiu(response)
        if url.find('/fenxi/daxiao-') >=0:
            return self.parse_daxiao(response)
        if url.find('fenxi/bifen-') >= 0:
            return self.parse_bifen(response)

    # 根据比赛ID生成对应的链接
    def gen_match_urls_with_id(self, match_id):
        urls = []
        prefix = "http://odds.500.com/fenxi/"
        # 1 数据分析
        shuju_url = prefix + "shuju-" + match_id + ".shtml"
        urls.append(shuju_url)

        # 2 百家欧赔
        ouzhi_url = prefix + "ouzhi-" + match_id + ".shtml?ctype=2"
        urls.append(ouzhi_url)

        # 3 让球指数
        rangqiu_url = prefix + "rangqiu-" + match_id + ".shtml?ctype=2"
        urls.append(rangqiu_url)

        # 4 亚盘对比
        # yazhi_url = prefix + "yazhi-" + match_id + ".shtml"
        # urls.append(yazhi_url)

        # 5 大小指数
        daxiao_url = prefix + "daxiao-" + match_id + ".shtml?ctype=2"
        urls.append(daxiao_url)

        # 6 比分指数
        bifen_url = prefix + "bifen-" + match_id + ".shtml?ctype=2"
        urls.append(bifen_url)

        return urls

    # 解析比赛获得比赛ID
    def parse_daily_matches(self, response):
        try:
            result = response.xpath('//tbody[@id="main-tbody"]')
            # 每五行为一个结果
            count = 1
            for tr in result.xpath('.//tr'):
                if count == 1:
                    match_id = tr.xpath('.//@data-fid').extract_first()
                    match_urls = self.gen_match_urls_with_id(match_id)
                    for url in match_urls:
                        yield SplashRequest(url, self.parse, args={'wait': 1})
                count += 1
                if count == 6:
                    count = 1
        except:
            self.add_err_urls(response.url,traceback.format_exc())

    # 数据分析
    def parse_shuju(self, response):

        try:
            match_id = response.url.split('shuju-')[1].split('.')[0]

            # 基本数据
            head_table = response.xpath('//div[@class="odds_header"]/div[@class="odds_hd_cont"]/table/tbody/tr')
            match = Match500()
            match['id'] = match_id
            match['home'] = head_table.xpath('.//td[1]/ul/li[1]/a/text()').extract_first()
            match['home_txt'] = head_table.xpath('.//td[1]/ul/li[1]/a/@href').extract_first()
            # match['home_standing_before'] = head_table.xpath('.//td[1]/ul/li[2]/span/text()').extract_first()
            round_txt = head_table.xpath(
                './/td[3]/div[@class="odds_hd_center"]/div[@class="odds_hd_ls"]/a/text()').extract_first()
            match['round_txt'] = round_txt if not round_txt else round_txt.strip()
            start_time_txt = head_table.xpath('.//td[3]/div/p[@class="game_time"]/text()').extract_first()
            start_time_txt = start_time_txt[4:]
            match['start_time'] = datetime.datetime.strptime(start_time_txt, '%Y-%m-%d %H:%M')
            home_away_goal = head_table.xpath('.//td[3]/div/p[@class="odds_hd_bf"]/strong/text()').extract_first()
            match['home_goal'] = home_away_goal.split(':')[0]
            match['away_goal'] = home_away_goal.split(':')[1]
            match['away'] = head_table.xpath('.//td[5]/ul/li[1]/a/text()').extract_first()
            match['away_txt'] = head_table.xpath('.//td[5]/ul/li[1]/a/@href').extract_first()
            # match['away_standing_before'] = head_table.xpath('.//td[5]/ul/li[2]/span/text()').extract_first()

            content = response.xpath('//div[@class="odds_content"]')
            for div in content.xpath('./div'):
                title = div.xpath('./div[@class="M_title"]/h4/text()').extract_first()
                if not title:
                    continue
                # 赛前联赛积分排名
                if title.find('赛前联赛积分排名') >= 0:

                    # 获取主客队简称
                    subtitle = div.xpath('./div[@class="M_sub_title"]')
                    match['home_short'] = subtitle.xpath('./div[1]/text()').extract_first()
                    match['away_short'] = subtitle.xpath('./div[2]/text()').extract_first()
                    yield match

                    div_content = div.xpath('./div[@class="M_content"]')
                    team_home = div_content.xpath('./div[@class="team_a"]/table')
                    idx_home = 0
                    for tr in team_home.xpath('.//tbody/tr'):
                        if idx_home >= 1:
                            standing = Match500TeamStanding()
                            standing['match_id'] = match_id
                            if idx_home == 1:
                                type = 'all'
                            elif idx_home == 2:
                                type = 'home'
                            else:
                                type = 'away'
                            standing['type'] = type
                            standing['team_type'] = 'home'
                            standing['match_count'] = tr.xpath('.//td[2]/text()').extract_first()
                            standing['win'] = tr.xpath('.//td[3]/text()').extract_first()
                            standing['draw'] = tr.xpath('.//td[4]/text()').extract_first()
                            standing['lose'] = tr.xpath('.//td[5]/text()').extract_first()
                            standing['goals'] = tr.xpath('.//td[6]/text()').extract_first()
                            standing['lost_goals'] = tr.xpath('.//td[7]/text()').extract_first()
                            standing['total_goals'] = tr.xpath('.//td[8]/text()').extract_first()
                            standing['marks'] = tr.xpath('.//td[9]/span/text()').extract_first()
                            standing['standing'] = tr.xpath('.//td[10]/text()').extract_first()
                            win_rate = tr.xpath('.//td[11]/text()').extract_first()
                            standing['win_rate'] = win_rate if not win_rate else win_rate.replace('%', '')
                            yield standing
                        idx_home += 1

                    team_away = div_content.xpath('./div[@class="team_b"]/table')
                    idx_away = 0
                    for tr in team_away.xpath('.//tbody/tr'):
                        if idx_away >= 1:
                            standing = Match500TeamStanding()
                            standing['match_id'] = match_id
                            if idx_away == 1:
                                type = 'all'
                            elif idx_away == 2:
                                type = 'home'
                            else:
                                type = 'away'
                            standing['type'] = type
                            standing['team_type'] = 'away'
                            standing['match_count'] = tr.xpath('.//td[2]/text()').extract_first()
                            standing['win'] = tr.xpath('.//td[3]/text()').extract_first()
                            standing['draw'] = tr.xpath('.//td[4]/text()').extract_first()
                            standing['lose'] = tr.xpath('.//td[5]/text()').extract_first()
                            standing['goals'] = tr.xpath('.//td[6]/text()').extract_first()
                            standing['lost_goals'] = tr.xpath('.//td[7]/text()').extract_first()
                            standing['total_goals'] = tr.xpath('.//td[8]/text()').extract_first()
                            standing['marks'] = tr.xpath('.//td[9]/span/text()').extract_first()
                            standing['standing'] = tr.xpath('.//td[10]/text()').extract_first()
                            win_rate = tr.xpath('.//td[11]/text()').extract_first()
                            standing['win_rate'] = win_rate if not win_rate else win_rate.replace('%', '')
                            yield standing
                        idx_away += 1
                elif title.find('交战历史') >= 0:
                    content = div.xpath('./div[@class="M_content"]/table')
                    count = 0
                    for tr in content.xpath('./tbody/tr'):
                        if count >= 2:
                            history = Match500History()
                            history['match_id'] = match_id
                            history['league_name'] = tr.xpath('./td[1]/a/text()').extract_first()
                            start_date = tr.xpath('./td[2]/text()').extract_first()
                            history['start_date'] = datetime.datetime.strptime(start_date, '%Y-%m-%d')
                            history['history_url'] = tr.xpath('./td[3]/a/@href').extract_first()
                            history['home'] = tr.xpath('./td[3]/a/span[1]/text()').extract_first()
                            history['away'] = tr.xpath('./td[3]/a/span[2]/text()').extract_first()
                            home_goal = tr.xpath('./td[3]/a/em').extract_first()
                            home_goal, no = re.subn('<[^\d:]*>', '', home_goal)
                            history['home_goal'] = home_goal.split(':')[0]
                            history['away_goal'] = home_goal.split(':')[1]
                            yield history

                        count += 1
                elif title.find('近期战绩') >= 0:
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

                    # 2、客队近十场战绩
                    zhanji_00 = div.xpath(
                        './/div[@id="team_zhanji_0"]/form[@id="zhanji_00"]/div[@class="M_content"]/table/tbody')
                    for tr in zhanji_00.xpath('./tr'):
                        tr_class = tr.xpath('./@class').extract_first()
                        if tr_class == 'tr1' or tr_class == 'tr2':
                            recent = Match500Recent()
                            recent['match_id'] = match_id
                            recent['team_type'] = 'away'
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

                    # 3、主队近十场主场战绩
                    zhanji_11 = div.xpath(
                        './/div[@id="team_zhanji2_1"]/form[@id="zhanji_11"]/div[@class="M_content"]/table/tbody')
                    for tr in zhanji_11.xpath('./tr'):
                        tr_class = tr.xpath('./@class').extract_first()
                        if tr_class == 'tr1' or tr_class == 'tr2':
                            recent = Match500Recent()
                            recent['match_id'] = match_id
                            recent['team_type'] = 'home'
                            recent['recent_type'] = 'home_away'
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

                    # 4、客队近十场客队战绩
                    zhanji_20 = div.xpath(
                        './/div[@id="team_zhanji2_0"]/form[@id="zhanji_20"]/div[@class="M_content"]/table/tbody')
                    for tr in zhanji_20.xpath('./tr'):
                        tr_class = tr.xpath('./@class').extract_first()
                        if tr_class == 'tr1' or tr_class == 'tr2':
                            recent = Match500Recent()
                            recent['match_id'] = match_id
                            recent['team_type'] = 'away'
                            recent['recent_type'] = 'home_away'
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

    # 百家欧赔
    def parse_ouzhi(self,response):

        try:
            match_id = response.url.split('ouzhi-')[1].split('.')[0]
            odds_table = response.xpath('//div[@id="table_cont"]/table/tbody')
            for tr in odds_table.xpath('./tr'):
                ouzhi = Match500Ouzhi()
                ouzhi['match_id'] = match_id
                ouzhi['comp'] = tr.xpath('./td[2]/p/a/span[@class="quancheng"]/text()').extract_first()
                ouzhi['win'] = tr.xpath('./td[3]/table/tbody/tr[2]/td[1]/text()').extract_first()
                ouzhi['draw'] = tr.xpath('./td[3]/table/tbody/tr[2]/td[2]/text()').extract_first()
                ouzhi['lose'] = tr.xpath('./td[3]/table/tbody/tr[2]/td[3]/text()').extract_first()
                ouzhi['returns'] = tr.xpath('./td[5]/table/tbody/tr[2]/td/text()').extract_first().replace('%', '')
                ouzhi['kelly_win'] = tr.xpath('./td[6]/table/tbody/tr[2]/td[1]/text()').extract_first()
                ouzhi['kelly_draw'] = tr.xpath('./td[6]/table/tbody/tr[2]/td[2]/text()').extract_first()
                ouzhi['kelly_lose'] = tr.xpath('./td[6]/table/tbody/tr[2]/td[3]/text()').extract_first()
                yield ouzhi
        except:
            self.add_err_urls(response.url, traceback.format_exc())


    # 让球指数
    def parse_rangqiu(self,response):

        try:
            match_id = response.url.split('rangqiu-')[1].split('.')[0]
            odds_table = response.xpath('//div[@id="table_cont"]/table/tbody')
            for tr in odds_table.xpath('./tr'):
                if tr.xpath('./@id').extract_first() == 'step_line':
                    continue
                rangqiu = Match500Rangqiu()
                rangqiu['match_id'] = match_id
                rangqiu['comp'] = tr.xpath('./td[2]/p/span[@class="quancheng"]/text()').extract_first()
                rangqiu['handicap'] = tr.xpath('./td[3]/text()').extract_first()
                rangqiu['win'] = tr.xpath('./td[4]/table/tbody/tr[2]/td[1]/text()').extract_first()
                rangqiu['draw'] = tr.xpath('./td[4]/table/tbody/tr[2]/td[2]/text()').extract_first()
                rangqiu['lose'] = tr.xpath('./td[4]/table/tbody/tr[2]/td[3]/text()').extract_first()
                rangqiu['returns'] = tr.xpath('./td[6]/table/tbody/tr[2]/td/text()').extract_first().replace('%', '')
                rangqiu['kelly_win'] = tr.xpath('./td[7]/table/tbody/tr[2]/td[1]/text()').extract_first()
                rangqiu['kelly_draw'] = tr.xpath('./td[7]/table/tbody/tr[2]/td[2]/text()').extract_first()
                rangqiu['kelly_lose'] = tr.xpath('./td[7]/table/tbody/tr[2]/td[3]/text()').extract_first()
                yield rangqiu
        except:
            self.add_err_urls(response.url, traceback.format_exc())


    # 大小球指数
    def parse_daxiao(self,response):
        try:
            match_id = response.url.split('daxiao-')[1].split('.')[0]
            odds_table = response.xpath('//div[@id="table_cont"]/table/tbody')
            for tr in odds_table.xpath('./tr'):
                tr_id = tr.xpath('./@id').extract_first()
                if tr_id == 'step_line':
                    continue
                daxiao = Match500Daxiao()
                daxiao['match_id'] = match_id
                daxiao['comp'] = tr.xpath('./td[2]/p/a/span[@class="quancheng"]/text()').extract_first()
                over = tr.xpath('./td[3]/table/tbody/tr/td[1]/text()').extract_first()
                handicap = tr.xpath('./td[3]/table/tbody/tr/td[2]/text()').extract_first()
                under = tr.xpath('./td[3]/table/tbody/tr/td[3]/text()').extract_first()
                daxiao['over'], no = re.subn('[^\d.]*', '', over)
                daxiao['handicap'], no = re.subn('[^\d./]*', '', handicap)
                daxiao['under'], no = re.subn('[^\d.]*', '', under)
                yield daxiao
        except:
            self.add_err_urls(response.url, traceback.format_exc())


    # 比分指数
    def parse_bifen(self,response):

        try:
            match_id = response.url.split('bifen-')[1].split('.')[0]
            odds_table = response.xpath(
                '//div[@class="mar_b M_box M_box_bifen"]/div[@class="M_content table_cont"]/table/tbody')
            for tr in odds_table.xpath('./tr'):
                tr_class = tr.xpath('./@class').extract_first()
                if tr_class == 'tr1' or tr_class == 'tr2':
                    bifen = Match500Bifen()
                    bifen['match_id'] = match_id
                    bifen['comp'] = tr.xpath('./td[2]/p/a/text()').extract_first()
                    bifen['one_zero'] = tr.xpath('./td[4]/span/text()').extract_first()
                    bifen['zero_one'] = tr.xpath('./td[4]/text()').extract_first()
                    bifen['two_zero'] = tr.xpath('./td[5]/span/text()').extract_first()
                    bifen['zero_two'] = tr.xpath('./td[5]/text()').extract_first()
                    bifen['two_one'] = tr.xpath('./td[6]/span/text()').extract_first()
                    bifen['one_two'] = tr.xpath('./td[6]/text()').extract_first()
                    bifen['three_zero'] = tr.xpath('./td[7]/span/text()').extract_first()
                    bifen['zero_three'] = tr.xpath('./td[7]/text()').extract_first()
                    bifen['three_one'] = tr.xpath('./td[8]/span/text()').extract_first()
                    bifen['one_three'] = tr.xpath('./td[8]/text()').extract_first()
                    bifen['three_two'] = tr.xpath('./td[9]/span/text()').extract_first()
                    bifen['two_three'] = tr.xpath('./td[9]/text()').extract_first()
                    bifen['four_zero'] = tr.xpath('./td[10]/span/text()').extract_first()
                    bifen['zero_four'] = tr.xpath('./td[10]/text()').extract_first()
                    bifen['four_one'] = tr.xpath('./td[11]/span/text()').extract_first()
                    bifen['one_four'] = tr.xpath('./td[11]/text()').extract_first()
                    bifen['four_two'] = tr.xpath('./td[12]/span/text()').extract_first()
                    bifen['two_four'] = tr.xpath('./td[12]/text()').extract_first()
                    bifen['four_three'] = tr.xpath('./td[13]/span/text()').extract_first()
                    bifen['three_four'] = tr.xpath('./td[13]/text()').extract_first()
                    bifen['zero_zero'] = tr.xpath('./td[14]/text()').extract_first()
                    bifen['one_one'] = tr.xpath('./td[15]/text()').extract_first()
                    bifen['two_two'] = tr.xpath('./td[16]/text()').extract_first()
                    bifen['three_three'] = tr.xpath('./td[17]/text()').extract_first()
                    bifen['four_four'] = tr.xpath('./td[18]/text()').extract_first()
                    yield bifen
        except:
            self.add_err_urls(response.url, traceback.format_exc())