#run bodan_analysis first
# -*- coding: UTF-8 -*-
import sys

reload(sys)
# python默认环境编码时ascii
sys.setdefaultencoding("utf-8")
sys.path.append('/Users/shihao/Documents/adagu-project/adagu_bodan')
import math
from adagu_bodan.model import loadSession
from adagu_bodan.model.bodan_500 import Bodan500

session = loadSession()

bodans = session.query(Bodan500).filter(Bodan500.away_goal != None, Bodan500.zero_one != None).all()

#收益设置单注10元
single_bet = 10.0
total_cost = 0.0
total_profit = 0

def calc_profit_by_match(match):
    #按照lowest odds来设定单场购买波胆数
    bodan_count = math.ceil(match.lowest_odds)
    #单场成本
    cost = bodan_count * single_bet

    #没买到准确波胆
    if bodan_count < match.hit_standing:
        match.profit = -cost
    else:
        match.profit = float(match.hit_odds) * 10 - cost


for match in bodans:
    calc_profit_by_match(match)

session.commit()