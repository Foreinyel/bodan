# -*- coding: UTF-8 -*-

# 计算收益

import sys

reload(sys)
# python默认环境编码时ascii
sys.setdefaultencoding("utf-8")
sys.path.append('/Users/shihao/Documents/adagu-project/adagu_bodan')

from adagu_bodan.model import loadSession
from adagu_bodan.model.match_500 import Match500
from adagu_bodan.model.match_500_ouzhi import Match500Ouzhi

session = loadSession()

# 1 找到澳门独赢赔率

results = session.query(Match500, Match500Ouzhi).join(Match500Ouzhi).filter(Match500.predict_win_no_win == 1,
                                                                            Match500Ouzhi.comp == 'Bet365').all()

for result in results:
    match = result.Match500
    ouzhi = result.Match500Ouzhi
    session.query(Match500).filter(Match500.id==match.id).update({"ouzhi_odds_aomen":ouzhi.win})
session.commit()



# 2 计算利润
single_bet=10.0
matches = session.query(Match500).filter(Match500.predict_win_no_win==1).all()
for match in matches:
    if match.home_goal > match.away_goal:
        if match.ouzhi_odds_aomen is None:
            profit = 0
        else:
            profit = single_bet * (float(match.ouzhi_odds_aomen) - 1)
    else:
        profit = - single_bet
    match.profit = profit

session.commit()