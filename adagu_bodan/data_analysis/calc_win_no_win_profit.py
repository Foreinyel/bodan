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
odds_name1 = [
    'one_zero',
    'two_zero',
    'two_one',
    'three_zero',
    'three_one',
    'three_two',
    'four_zero',
    'four_one',
    'four_two',
    'four_three']
odds_name0 = [
    'zero_one',
    'zero_two',
    'one_two',
    'zero_three',
    'one_three',
    'two_three',
    'zero_four',
    'one_four',
    'two_four',
    'three_four',
    'zero_zero',
    'one_one',
    'two_two',
    'three_three',
    'four_four',
]

home_win_bodan = ['1:0','2:0','2:1','3:0','3:1','3:2','4:0']
home_no_win_bodan = ['0:0','1:1','2:2','0:1','0:2','1:2','0:3','1:3']

def calc_profit_by_match(match):

    #1、根据predict_win_no_win划分下注边界,主队赢5球及以下占据大部分select count(1),t.abc from (select bodan_500.home_goal + bodan_500.away_goal as abc from soccer_data.bodan_500 where bodan_500.away_goal IS NOT NULL AND bodan_500.zero_one IS NOT NULL and  bodan_500.home_goal > bodan_500.away_goal) t group by t.abc
    #主队不赢4球及以下占据大部分select count(1),t.abc from (select bodan_500.home_goal + bodan_500.away_goal as abc from soccer_data.bodan_500 where bodan_500.away_goal IS NOT NULL AND bodan_500.zero_one IS NOT NULL and  bodan_500.home_goal <= bodan_500.away_goal) t group by t.abc
    #那么主队赢购买波胆为：1:0,2:0;2:1,3:0,3:1,3:2,4:0
    #主队不赢购买波胆为：0:0,1:1,2:2,0:1,0:2,1:2,0:3,1:3
    cost = 0.0
    profit = 0.0
    score_str = str(match.home_goal) + ':' + str(match.away_goal)
    if match.predict_win_no_win == 1:
        cost = 7 * single_bet

        # 买中
        if score_str in home_win_bodan:
            profit = single_bet * float(match.hit_odds)

    # elif match.predict_win_no_win == 0:
    #     cost = 8 * single_bet
    #     # 买中
    #     if score_str in home_no_win_bodan:
    #         profit = single_bet * float(match.hit_odds)

    match.win_no_win_cost = cost
    match.win_no_win_profit = profit

for match in bodans:
    calc_profit_by_match(match)

session.commit()


#summary 2017-03-14
#模型预测主队赢和不赢准确率为64%，下注波胆总成本876070.0000，最后总成本为'632249.0000'，亏损24万
#只下注主队赢的比赛，下注总成本为''282310.0000''，最后总成本为'211413.5000'