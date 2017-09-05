# -*- coding: UTF-8 -*-
import sys

reload(sys)
# python默认环境编码时ascii
sys.setdefaultencoding("utf-8")
sys.path.append('/Users/shihao/Documents/adagu-project/adagu_bodan')

import os

from adagu_bodan.model import loadSession
from adagu_bodan.model.bodan_500 import Bodan500

session = loadSession()

bodans = session.query(Bodan500).filter(Bodan500.away_goal != None, Bodan500.zero_one != None).all()

try:
       os.remove('svm.csv')
except:
       pass

bodan_file = open('svm.csv', 'a')

split_tag = ','
lines = []

for bodan in bodans:
    line = bodan.one_zero + split_tag + bodan.two_zero + split_tag + bodan.two_one + split_tag + bodan.three_zero + split_tag + \
           bodan.three_one + split_tag + bodan.three_two + split_tag + bodan.four_zero + split_tag + bodan.four_one + split_tag + \
           bodan.four_two + split_tag + bodan.four_three + split_tag + bodan.zero_one + split_tag + bodan.zero_two + split_tag + \
           bodan.one_two + split_tag + bodan.zero_three + split_tag + bodan.one_three + split_tag + bodan.two_three + split_tag + \
           bodan.zero_four + split_tag + bodan.one_four + split_tag + bodan.two_four + split_tag + bodan.three_four + split_tag + \
           bodan.zero_zero + split_tag + bodan.one_one + split_tag + bodan.two_two + split_tag + bodan.three_three + split_tag + \
           bodan.four_four + split_tag

    #y为胜平负
    # if int(bodan.home_goal) > int(bodan.away_goal):
    #        result = '1'
    # elif bodan.home_goal == bodan.away_goal:
    #        result = '0'
    # else:
    #        result = '2'

    #y为比分
    # result = str(bodan.home_goal * 10 + bodan.away_goal)

    #y为让球数
    result = str(bodan.home_goal - bodan.away_goal)

    line += result + '\n'
    lines.append(line)

bodan_file.writelines(lines)
bodan_file.flush()
bodan_file.close()