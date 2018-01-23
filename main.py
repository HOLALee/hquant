#!\usr\bin\python
# -*- coding: UTF-8 -*-

import os,sys
import pandas as pd
import tushare as ts
import json
from common import base

root = sys.path[0]
(year,q) = base.getYearAndQua()
print root

class Main:

    def __init__(self):
        pass

    def getStockBase(self):

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
        year = 2017
        q = 3
        print "数据说明：",year,"年",q,"季度"
        df1 = ts.get_stock_basics()
        df1.to_json(root + "\data\get_stock_basics.json")
        print "get_stock_basics success..."

        df2 = ts.get_report_data(year,q)
        df2.to_json(root + "\data\get_report_data.json")
        print "get_report_data success..."

        df3 = ts.get_profit_data(year,q)
        df3.to_json(root + "\data\get_profit_data.json")
        print "get_profit_data success..."

        df4 = ts.get_operation_data(year,q)
        df4.to_json(root + "\data\get_operation_data.json")
        print "get_operation_data success..."

        df5 = ts.get_growth_data(year,q)
        df5.to_json(root + "\data\get_growth_data.json")
        print "get_growth_data success..."

        df6 = ts.get_debtpaying_data(year,q)
        df6.to_json(root + "\data\get_debtpaying_data.json")
        print "get_debtpaying_data success..."

        df7 = ts.get_cashflow_data(year,q)
        df7.to_json(root + "\data\get_cashflow_data.json")
        print "get_cashflow_data success..."

if __name__ == '__main__':
    m = Main()
    m.getStockBase()
