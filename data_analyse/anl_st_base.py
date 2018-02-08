# -*- coding: UTF-8 -*-
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
    def __init__(self, root, industry = None, industryCode = None):
        super(AnlStBase, self).__init__()
        self.root = root
        if industryCode is None:
            self.industryCode = "all"
        else:
            self.industryCode = industryCode
        self.industry = industry

    def importJSON(self, filename):
        path = self.root+"\data\\" + filename
        df = pd.read_excel(path,encoding="utf-8")
        return df

    def axisData(self, mean, *args):
        dfs = []
        for i in args:
            dfs.append(self.importJSON(i))
        df = pd.merge(dfs[0], dfs[1])
        df = pd.merge(df, dfs[2])
        df = pd.merge(df, dfs[3])
        df = pd.merge(df, dfs[4])
        df = pd.merge(df, dfs[5])

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
        #df = df.dropna(axis=0)
        #增加净利润资产率=净利润/总资产
        df.fillna(0)
        #增加净利润资产率=净利润/总资产
        #df['roe_pb'] = df['roe']/df['pb']
        df['sv'] = df['pe']/df['npr']
        df = df[~df.name.str.contains("S")]
        df = df.drop_duplicates('code')

        if mean:
            industry_mean = df.groupby(df['industry']).mean()
            industry_mean.to_excel(a.root + "/data/industry.Mean.xlsx")

        if self.industry:
            df = df.loc[df.industry.isin(self.industry)]

        df = df.sort_values(by=['sv','gross_profit_rate','currentasset_turnover','rateofreturn','nav'])
        df = df.loc[:,['code','name','industry', 'c_name', 'sv', 'npr', 'roe_pb', 'esp', 'roe','pb','pe','nav','gross_profit_rate','currentasset_turnover','rateofreturn']]
        df['code']=df['code'].astype(str).str.zfill(6)
        df['market'] =  df['code'].map(self.getMarket)
        df['label'] = df['code'] + '.' + df['market']
        # if self.industry:
        #     df = df.loc[df.industry.isin(self.industry)]

        mean = df.mean()

        """
        因子筛选策略：
        1.市盈率小于行业均值且大于0
        2.净资产收益率大于行业均值
        3.毛利率大于行业均值
        """
        filter_df = df.loc[(df.pe > mean['pe'])&(df.pb<2)]

        #保存到excel
        df.to_excel(a.root + "/data/" + self.industryCode + ".xlsx")
        filter_df.to_excel(a.root + "/data/" + self.industryCode + ".Top.xlsx")
        #return df,filter_df

    def getMarket(self,x):
        if x.startswith('00') or x.startswith('30'):
            return 'XSHE'
        elif x.startswith('60'):
            return 'XSHG'

if __name__ == "__main__":
    a = AnlStBase("D:\GitHub\hquant")
    a.axisData(
        True,
        "get_stock_basics.xlsx",
        "get_concept_classified.xlsx",
        "get_profit_data.xlsx",
        "get_operation_data.xlsx",
        "get_growth_data.xlsx",
        "get_cashflow_data.xlsx"
    )
