#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pandas as pd
from common import base
from stock_base import stock_base as sb
import csv

class Main:

    def __init__(self):
        pass

    def readCsv(self, path):

        #营运能力指标
        currentasset_turnovers = [] #流动性资产周转率

        #营运能力指标
        inventory_turnovers = [] #存货周转率

        #盈利能力指标
        nprgs = []           #净利润增长率
        nprofits_Assets = [] #净利润资产率
        roes = []            #净资产收益率

        #成长能力指标
        navs = []            #净资产增长率
        targs = []           #总资产增长率

        reader = csv.reader(open(path))
        for _id, code,  name in reader:
            profit = ts.get_profit_data(y,q)

if __name__ == '__main__':
    v = [1,2,3,4,5,6,7,8]
    print v[v > 1]
