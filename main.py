#!\usr\bin\python
# -*- coding: utf-8 -*-

import os,sys
import pandas as pd
import tushare as ts
import json
from common import base
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

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
        year = 2016
        q = 1
        print "数据说明：",year,"年",q,"季度"
        df1 = ts.get_stock_basics()
        df1.to_excel(root + "\data\get_stock_basics.xlsx")
        print "get_stock_basics success..."

        df2 = ts.get_report_data(year,q)
        df2.to_excel(root + "\data\get_report_data.xlsx",encoding="utf-8")
        print "get_report_data success..."

        df3 = ts.get_profit_data(year,q)
        df3.to_excel(root + "\data\get_profit_data.xlsx",encoding="utf-8")
        print "get_profit_data success..."

        df4 = ts.get_operation_data(year,q)
        df4.to_excel(root + "\data\get_operation_data.xlsx",encoding="utf-8")
        print "get_operation_data success..."

        df5 = ts.get_growth_data(year,q)
        df5.to_excel(root + "\data\get_growth_data.xlsx",encoding="utf-8")
        print "get_growth_data success..."

        df6 = ts.get_debtpaying_data(year,q)
        df6.to_excel(root + "\data\get_debtpaying_data.xlsx",encoding="utf-8")
        print "get_debtpaying_data success..."

        df7 = ts.get_cashflow_data(year,q)
        df7.to_excel(root + "\data\get_cashflow_data.xlsx",encoding="utf-8")
        print "get_cashflow_data success..."

        df8 = ts.get_concept_classified()
        df8.to_excel(root + "\data\get_concept_classified.xlsx",encoding="utf-8")
        print "get_concept_classified success..."

if __name__ == '__main__':
    data = ts.get_report_data(2016,1)
    #调整数据，0补全空值、剔除ST、去重、取评估指标列
    data.fillna(0)
    data = data[~data.name.str.contains("S")]
    data = data.drop_duplicates('name')
    #data = data.loc[:,['name','esp','pb','pe','esp','npr']]
    print len(data.roe.values)
    data = data.loc[(data.roe > 0)&(data.net_profits > 0)&(data.eps_yoy>0)]
    print len(data.roe.values)
    #data.to_excel(context.Dir + '/data/clean1.xlsx', encoding = 'utf-8')
