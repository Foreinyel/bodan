# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from model import loadSession
from model.bodan_500 import Bodan500
from model.match_500 import Match500
from model.match_500_team_standing import Match500TeamStanding
from model.match_500_history import Match500History
from model.match_500_recent import Match500Recent
from model.match_500_ouzhi import Match500Ouzhi
from model.match_500_rangqiu import Match500Rangqiu
from model.match_500_daxiao import Match500Daxiao
from model.match_500_bifen import Match500Bifen

class AdaguBodanPipeline(object):
    def process_item(self, item, spider):
        item_type = item.__class__.__name__
        # print 'item_type:%s, item content: %s' % (item.__class__.__name__, str(item))
        if item_type == 'Bodan':
            self.save_bodan(item)
        elif item_type == 'Match500':
            self.save_match500(item)
        elif item_type == 'Match500TeamStanding':
            self.save_match500_team_standing(item)
        elif item_type == 'Match500History':
            self.save_match500_history(item)
        elif item_type == 'Match500Recent':
            self.save_match500_recent(item)
        elif item_type == 'Match500Ouzhi':
            self.save_match500_ouzhi(item)
        elif item_type == 'Match500Rangqiu':
            self.save_match500_rangqiu(item)
        elif item_type == 'Match500Daxiao':
            self.save_match500_daxiao(item)
        elif item_type == 'Match500Bifen':
            self.save_match500_bifen(item)
        return item

    def save_match500(self,item):
        session = loadSession()
        session.query(Match500).filter(Match500.id == item['id']).delete()
        match = Match500()
        match.id = item['id']
        match.round_txt = item['round_txt']
        match.start_time = item['start_time']
        match.home_txt = item['home_txt']
        match.away_txt = item['away_txt']
        match.home = item['home']
        match.away = item['away']
        match.home_goal = item['home_goal']
        match.away_goal = item['away_goal']
        match.home_short = item['home_short']
        match.away_short = item['away_short']
        session.add(match)
        session.commit()

    def save_match500_team_standing(self,item):
        session = loadSession()

        session.query(Match500TeamStanding).filter(Match500TeamStanding.match_id==item['match_id'],Match500TeamStanding.type==item['type'],Match500TeamStanding.team_type==item['team_type']).delete()

        standing = Match500TeamStanding()
        standing.match_id = item['match_id']
        standing.type = item['type']
        standing.team_type = item['team_type']
        standing.match_count = item['match_count']
        standing.win = item['win']
        standing.draw = item['draw']
        standing.lose = item['lose']
        standing.goals = item['goals']
        standing.lost_goals = item['lost_goals']
        standing.total_goals = item['total_goals']
        standing.marks = item['marks']
        standing.standing = item['standing']
        standing.win_rate = item['win_rate']

        session.add(standing)
        session.commit()

    def save_match500_history(self,item):
        session = loadSession()

        session.query(Match500History).filter(Match500History.match_id==item['match_id'],Match500History.history_url==item['history_url']).delete()

        history = Match500History()
        history.match_id = item['match_id']
        history.league_name = item['league_name']
        history.start_date = item['start_date']
        history.history_url = item['history_url']
        history.home = item['home']
        history.away = item['away']
        history.home_goal = item['home_goal']
        history.away_goal = item['away_goal']

        session.add(history)
        session.commit()

    def save_match500_recent(self,item):
        session = loadSession()

        session.query(Match500Recent).filter(Match500Recent.match_id==item['match_id'],Match500Recent.team_type==item['team_type'],Match500Recent.recent_type == item['recent_type'],Match500Recent.recent_url==item['recent_url']).delete()

        recent = Match500Recent()
        recent.match_id = item['match_id']
        recent.team_type = item['team_type']
        recent.recent_type = item['recent_type']
        recent.recent_url = item['recent_url']
        recent.league_name = item['league_name']
        recent.start_date = item['start_date']
        recent.home = item['home']
        recent.away = item['away']
        recent.home_goal = item['home_goal']
        recent.away_goal = item['away_goal']

        session.add(recent)
        session.commit()

    def save_match500_ouzhi(self,item):
        session = loadSession()

        ouzhi = Match500Ouzhi()
        ouzhi.match_id = item['match_id']
        ouzhi.comp = item['comp']
        ouzhi.returns = item['returns']
        ouzhi.win = item['win']
        ouzhi.draw = item['draw']
        ouzhi.lose = item['lose']
        ouzhi.kelly_win = item['kelly_win']
        ouzhi.kelly_draw = item['kelly_draw']
        ouzhi.kelly_lose = item['kelly_lose']

        session.add(ouzhi)
        session.commit()

    def save_match500_rangqiu(self,item):
        session = loadSession()

        rangqiu = Match500Rangqiu()
        rangqiu.match_id = item['match_id']
        rangqiu.comp = item['comp']
        rangqiu.handicap = item['handicap']
        rangqiu.returns = item['returns']
        rangqiu.win = item['win']
        rangqiu.draw = item['draw']
        rangqiu.lose = item['lose']
        rangqiu.kelly_win = item['kelly_win']
        rangqiu.kelly_draw = item['kelly_draw']
        rangqiu.kelly_lose = item['kelly_lose']

        session.add(rangqiu)
        session.commit()

    def save_match500_daxiao(self,item):
        session = loadSession()

        daxiao = Match500Daxiao()
        daxiao.match_id = item['match_id']
        daxiao.comp = item['comp']
        daxiao.handicap = item['handicap']
        daxiao.over = item['over']
        daxiao.under = item['under']

        session.add(daxiao)
        session.commit()

    def save_match500_bifen(self,item):
        session = loadSession()

        bifen = Match500Bifen()
        bifen.match_id = item['match_id']
        bifen.comp = item['comp']
        bifen.one_zero = item['one_zero']
        bifen.two_zero = item['two_zero']
        bifen.two_one = item['two_one']
        bifen.three_zero = item['three_zero']
        bifen.three_one = item['three_one']
        bifen.three_two = item['three_two']
        bifen.four_zero = item['four_zero']
        bifen.four_one = item['four_one']
        bifen.four_two = item['four_two']
        bifen.four_three = item['four_three']
        bifen.zero_one = item['zero_one']
        bifen.zero_two = item['zero_two']
        bifen.one_two = item['one_two']
        bifen.zero_three = item['zero_three']
        bifen.one_three = item['one_three']
        bifen.two_three = item['two_three']
        bifen.zero_four = item['zero_four']
        bifen.one_four = item['one_four']
        bifen.two_four = item['two_four']
        bifen.three_four = item['three_four']
        bifen.zero_zero = item['zero_zero']
        bifen.one_one = item['one_one']
        bifen.two_two = item['two_two']
        bifen.three_three = item['three_three']
        bifen.four_four = item['four_four']

        session.add(bifen)
        session.commit()

    def save_bodan(self,item):
        session = loadSession()
        bodan500 = Bodan500()
        bodan500.league = item['league']
        bodan500.start_time = item['start_time']
        bodan500.home = item['home']
        bodan500.away = item['away']
        bodan500.home_goal = item['home_goal']
        bodan500.away_goal = item['away_goal']
        bodan500.odds_comp = item['odds_comp']
        bodan500.one_zero = item['one_zero']
        bodan500.two_zero = item['two_zero']
        bodan500.two_one = item['two_one']
        bodan500.three_zero = item['three_zero']
        bodan500.three_one = item['three_one']
        bodan500.three_two = item['three_two']
        bodan500.four_zero = item['four_zero']
        bodan500.four_one = item['four_one']
        bodan500.four_two = item['four_two']
        bodan500.four_three = item['four_three']
        bodan500.zero_one = item['zero_one']
        bodan500.zero_two = item['zero_two']
        bodan500.one_two = item['one_two']
        bodan500.zero_three = item['zero_three']
        bodan500.one_three = item['one_three']
        bodan500.two_three = item['two_three']
        bodan500.zero_four = item['zero_four']
        bodan500.one_four = item['one_four']
        bodan500.two_four = item['two_four']
        bodan500.three_four = item['three_four']
        bodan500.zero_zero = item['zero_zero']
        bodan500.one_one = item['one_one']
        bodan500.two_two = item['two_two']
        bodan500.three_three = item['three_three']
        bodan500.four_four = item['four_four']
        bodan500.returns = item['returns']
        session.add(bodan500)
        session.commit()

