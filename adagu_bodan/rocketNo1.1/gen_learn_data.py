# -*- coding: UTF-8 -*-

import sys

reload(sys)
# python默认环境编码时ascii
sys.setdefaultencoding("utf-8")
sys.path.append('/Users/shihao/Documents/adagu-project/adagu_bodan')

# 生成学习数据
# 25 features（比分）
# result:1-主胜,0-主不胜
# table: match_500_bifen

import os

from adagu_bodan.model import loadSession
from adagu_bodan.model.match_500_bifen import Match500Bifen
from adagu_bodan.model.match_500 import Match500

session = loadSession()

# 2016年全年数据作为训练数据
results = session.query(Match500Bifen, Match500).join(Match500).filter(Match500Bifen.comp == '澳门',
                                                                       Match500.start_time >= '2016-01-01',
                                                                       Match500.start_time <= '2016-12-31').all()

try:
    os.remove('learn_data.csv')
except:
    pass

learn_data_file = open('learn_data.csv', 'a')

split_tag = ','
lines = []

for bodan in results:
    match500 = bodan.Match500
    match500bifen = bodan.Match500Bifen
    line = match500bifen.one_zero + split_tag + match500bifen.two_zero + split_tag + match500bifen.two_one + split_tag + match500bifen.three_zero + split_tag + \
           match500bifen.three_one + split_tag + match500bifen.three_two + split_tag + match500bifen.four_zero + split_tag + match500bifen.four_one + split_tag + \
           match500bifen.four_two + split_tag + match500bifen.four_three + split_tag + match500bifen.zero_one + split_tag + match500bifen.zero_two + split_tag + \
           match500bifen.one_two + split_tag + match500bifen.zero_three + split_tag + match500bifen.one_three + split_tag + match500bifen.two_three + split_tag + \
           match500bifen.zero_four + split_tag + match500bifen.one_four + split_tag + match500bifen.two_four + split_tag + match500bifen.three_four + split_tag + \
           match500bifen.zero_zero + split_tag + match500bifen.one_one + split_tag + match500bifen.two_two + split_tag + match500bifen.three_three + split_tag + \
           match500bifen.four_four + split_tag
    if int(match500.home_goal) > int(match500.away_goal):
        result = '1'
    else:
        result = '0'
    line += result + '\n'
    lines.append(line)

learn_data_file.writelines(lines)
learn_data_file.flush()
learn_data_file.close()
