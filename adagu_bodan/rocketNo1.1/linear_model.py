# -*- coding: UTF-8 -*-

#线性模型

import sys

reload(sys)
# python默认环境编码时ascii
sys.setdefaultencoding("utf-8")
sys.path.append('/Users/shihao/Documents/adagu-project/adagu_bodan')

import pandas as pd
import numpy as np

from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

#1、获取模型

column_names = [
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
    'class'
]

threshold = 0.7

data = pd.read_csv('/Users/shihao/Documents/adagu-project/adagu_bodan/adagu_bodan/rocketNo1/learn_data.csv',names=column_names)

X_train,X_test,y_train,y_test=train_test_split(data[column_names[0:25]],data[column_names[25]],test_size=0.25,random_state=33)

ss=StandardScaler()
X_train=ss.fit_transform(X_train)
X_test=ss.transform(X_test)
lr=LogisticRegression()
lr.fit(X_train,y_train)
# lr_y_predict=lr.predict(X_test)
lr_y_predict_prob = lr.predict_proba(X_test)

lr_y_predict = lr.classes_[np.argmax(lr_y_predict_prob > threshold, axis=1)]

print classification_report(y_test,lr_y_predict)

# print lr.coef_.T

# print lr_y_predict_prob
#
# print 'Accuracy of LR Classifier:',lr.score(X_test,y_test)


#2、对2017.1.1-2017.4.1区间数据回测

from adagu_bodan.model import loadSession
from adagu_bodan.model.match_500_bifen import Match500Bifen
from adagu_bodan.model.match_500 import Match500

session = loadSession()

matches = session.query(Match500Bifen).join(Match500).filter(Match500Bifen.comp=='澳门',Match500.start_time>='2017-01-01',Match500.start_time<='2017-04-31').all()
print 'matches:%f'%(len(matches))
def predict_win_no_win(match):
    x_column_names = column_names[0:25]
    X = np.array([[match.__dict__[name] for name in x_column_names]])
    X = ss.transform(X)
    # X.reshape(-1, 1)
    y_predict_prob = lr.predict_proba(X)
    y_predict = lr.classes_[np.argmax(y_predict_prob > threshold, axis=1)]
    session.query(Match500).filter(Match500.id==match.match_id).update({"predict_win_no_win":y_predict[0]})

for match in matches:
    predict_win_no_win(match)

session.commit()
