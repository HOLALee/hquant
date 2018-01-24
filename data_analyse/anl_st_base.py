# -*- coding: UTF-8 -*-

import pandas as pd
import numpy as np
import json

class AnlStBase(object):
    """docstring for AnlStBase."""
    def __init__(self, root):
        super(AnlStBase, self).__init__()
        self.root = root

    def importJSON(self, filename):
        path = self.root+"\data\\" + filename
        print "to load file:",path
        #编码转换
        f = open(path,'r')
        r = f.read()
        r = r.decode("utf-8-sig")
        data = json.loads(r)
        #a_js = json.dumps(data)
        df = pd.DataFrame(data)
        return df

    def axisData(self, *args):
        dfs = []
        for i in args:
            dfs.append(self.importJSON(i))
        _df = pd.merge(dfs[0], dfs[1])
        _df = pd.merge(_df, dfs[2])
        _df = pd.merge(_df, dfs[3])
        _df = pd.merge(_df, dfs[4])

        _df.to_excel("D:/py/data/dfs_ex.xlsx")

        #增加净利润资产率=净利润/总资产
        _df['profit_assets'] = _df['net_profits']/_df['totalAssets']
        _df.fillna(0)  #0填充NaN
        _df = _df.loc[:,['code','name','industry','nav','roe','gross_profit_rate','profit_assets','currentasset_turnover','rateofreturn']]
        _df = _df.dropna(axis=0)
        _df = _df.sort_values(by=['nav','roe','currentasset_turnover','rateofreturn','gross_profit_rate','profit_assets'])
        return _df

if __name__ == "__main__":
    a = AnlStBase("D:\py\\ts")
    #a.importJSON("get_stock_basics.json")
    dfs = a.axisData(
        "get_stock_basics.json",
        "get_profit_data.json",
        "get_operation_data.json",
        "get_growth_data.json",
        "get_cashflow_data.json"
    )
    dfs.to_excel("D:/py/data/dfs.xlsx")
