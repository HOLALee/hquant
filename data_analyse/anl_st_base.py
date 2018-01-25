#-*- coding=utf-8 -*-
"""
选股策略
根据质量因子对股票进行筛选
质量因子：净资产增长率、净资产收益率、毛利率、流动资产周转率、资产的经营现金流量回报率、净利润资产率
"""
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
    def __init__(self, root, industry, industryCode):
        super(AnlStBase, self).__init__()
        self.root = root
        if industryCode is None:
            self.industryCode = "all"
        else:
            self.industryCode = industryCode
        self.industry = unicode(industry, "utf-8")

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

        """
        数据整理
        1.删除空值行
        2.根据行业参数选出行业范围标的
        3.添加净利润资产率=净利润/总资产
        4.0补全空值
        6.删除ST或者S股票
        7.去重
        6.排序
        7.删除不必要的列
        8.求各列均值
        """
        df = df.dropna(axis=0)
        if self.industry:
            df = df.loc[df.industry.str.contains(self.industry)]
        #增加净利润资产率=净利润/总资产
        df['profit_assets'] = df['net_profits']/df['totalAssets']
        df.fillna(0)
        df = df[~df.name.str.contains("S")]
        df = df.drop_duplicates('code')
        df = df.sort_values(by=['nav','roe','currentasset_turnover','rateofreturn','gross_profit_rate','profit_assets'])
        df = df.loc[:,['code','name','industry','pb','pe','nav','roe','gross_profit_rate','profit_assets','currentasset_turnover','rateofreturn']]
        mean = df.mean()

        """
        因子筛选策略：
        1.市盈率小于行业均值且大于0
        2.净资产收益率大于行业均值
        3.毛利率大于行业均值
        """
        filter_df = df.loc[(df.pe>0)&(df.pe<mean['pe'])&(df.roe>mean['roe'])&(df.gross_profit_rate>mean['gross_profit_rate'])]
        filter_df.append(mean,ignore_index=True)

        #保存到excel
        df.to_excel(a.root + "/data/" + self.industryCode + ".xlsx")
        filter_df.to_excel(a.root + "/data/" + self.industryCode + ".Top.xlsx")
        #return df,filter_df

if __name__ == "__main__":
    a = AnlStBase("D:\py\\ts","小金属","xiaojinshu")
    a.axisData(
        "get_stock_basics.xlsx",
        "get_profit_data.xlsx",
        "get_operation_data.xlsx",
        "get_growth_data.xlsx",
        "get_cashflow_data.xlsx"
    )
