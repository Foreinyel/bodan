# -*- coding: UTF-8 -*-

# 计算收益率

import sys

reload(sys)
# python默认环境编码时ascii
sys.setdefaultencoding("utf-8")
sys.path.append('/Users/shihao/Documents/adagu-project/adagu_bodan')

from adagu_bodan.model import loadSession
from adagu_bodan.model.match_500 import Match500

session = loadSession()

matches = session.query(Match500).filter(Match500.predict_win_no_win==1).order_by(Match500.start_time).all()

#资金池最少金额
lowest_money = 10.0

# 资金池注入金额，初始10
total_cost = lowest_money

#资金池总金额，初始同注入金额
total_money = total_cost

for match in matches:
    total_money = total_money + float(match.profit)

    #如果资金池资金不够最少金额，注入金额直至达到最少金额
    if total_money < lowest_money:
        total_cost = total_cost + lowest_money - total_money
        total_money = lowest_money

print '资金池总注入金额%f,资金池最后金额%f'%(total_cost,total_money)
