#-*- coding=utf-8 -*-

import pandas as pd
import numpy as np
import xlrd
import openpyxl
import json
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class AnlStBase(object):
    """docstring for AnlStBase."""
    def __init__(self, root, industry):
        super(AnlStBase, self).__init__()
        self.root = root
        self.industry = industry

    def importJSON(self, filename):
        path = self.root+"\data\\" + filename
        df = pd.read_excel(path,encoding="utf-8")
        return df

    def axisData(self, *args):
        dfs = []
        for i in args:
            dfs.append(self.importJSON(i))
        df = pd.merge(dfs[0], dfs[1])
        df = pd.merge(df, dfs[2])
        df = pd.merge(df, dfs[3])
        df = pd.merge(df, dfs[4])

        #df.to_excel(self.root + "/data/dfs_ex.xlsx")
        #删除空值行
        df = df.dropna(axis=0)
        df = df.loc[df.industry.str.contains('小金属')]
        #增加净利润资产率=净利润/总资产
        # df['profit_assets'] = df['net_profits']/df['totalAssets']
        # #0补全空值
        # df.fillna(0)
        # df = df.loc[:,['code','name','industry','pb','pe','nav','roe','gross_profit_rate','profit_assets','currentasset_turnover','rateofreturn']]
        # df = df.sort_values(by=['nav','roe','currentasset_turnover','rateofreturn','gross_profit_rate','profit_assets'])
        # df = df[~df.name.str.contains("S")]
        # df = df.drop_duplicates('code')
        # #市盈率小于20且大于0,市净率小于10，净资产增长率大于0
        # df = df.loc[(df.pe>0)&(df.pe<20)&(df.nav>0)&(df.roe>10)&(df.gross_profit_rate>30)&(df.pb<10)&(df.rateofreturn>0.05)]
        return df

if __name__ == "__main__":
    a = AnlStBase("D:\py\\ts","小金属")
    dfs = a.axisData(
        "get_stock_basics.xlsx",
        "get_profit_data.xlsx",
        "get_operation_data.xlsx",
        "get_growth_data.xlsx",
        "get_cashflow_data.xlsx"
    )
    dfs.to_excel(a.root + "/data/dfs.xlsx")
