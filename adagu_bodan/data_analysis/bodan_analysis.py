# -*- coding: UTF-8 -*-
import sys

reload(sys)
# python默认环境编码时ascii
sys.setdefaultencoding("utf-8")
sys.path.append('/Users/shihao/Documents/adagu-project/adagu_bodan')

from adagu_bodan.model import loadSession
from adagu_bodan.model.bodan_500 import Bodan500

session = loadSession()

bodans = session.query(Bodan500).filter(Bodan500.away_goal != None, Bodan500.zero_one != None).all()

odds_name = [
    'one_zero',
    'two_zero',
    'two_one',
    'three_zero',
    'three_one',
    'three_two',
    'four_zero',
    'four_one',
    'four_two',
    'four_three',
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


def number_two_str(number):
    if number == 0:
        return 'zero'
    elif number == 1:
        return 'one'
    elif number == 2:
        return 'two'
    elif number == 3:
        return 'three'
    elif number == 4:
        return 'four'
    else:
        return 'overflow'

def find_lowest_odds(bodan):
    curr_lowest = 999999
    for name in odds_name:
        if float(bodan.__getattribute__(name)) <= float(curr_lowest):
            curr_lowest = float(bodan.__getattribute__(name))
    bodan.lowest_odds = curr_lowest

# 按照赔率将每场比赛波胆排序，计算每场比赛命中第几个
def set_odds_standing(bodan):
    score = number_two_str(bodan.home_goal) + '_' + number_two_str(bodan.away_goal)
    if score.find('overflow') >= 0:
        bodan.hit_standing = -1
        bodan.hit_odds = -1
        return

    # 命中赔率
    hit_odds = bodan.__getattribute__(score)
    hit_standing = 1

    for name in odds_name:
        if float(bodan.__getattribute__(name)) <= float(hit_odds) and name != score:
            hit_standing += 1

    bodan.hit_standing = hit_standing
    bodan.hit_odds = hit_odds
    # print bodan.__dict__['home_goal']
    # bodan.__getattribute__('home_goal')
    # dir(bodan)
    # print hit_standing

def set_win_or_lose(match):
    if int(match.home_goal) > int(match.away_goal):
        match.win_or_lose = '1'
    elif match.home_goal == match.away_goal:
        match.win_or_lose = '0'
    else:
        match.win_or_lose = '2'

def set_win_no_win(match):
    if int(match.home_goal) > int(match.away_goal):
        match.win_no_win = '1'
    else:
        match.win_no_win = '0'

for bodan in bodans:
    set_odds_standing(bodan)
    find_lowest_odds(bodan)
    set_win_or_lose(bodan)
    set_win_no_win(bodan)

session.commit()