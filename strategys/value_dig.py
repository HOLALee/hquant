# -*- coding: UTF-8 -*-
import datetime
from rqalpha.api import *
from rqalpha import run_func
import tushare as ts
import pandas as pd
import numpy as np

YEAR =  datetime.datetime.now().year
MONTH =  datetime.datetime.now().month
SH_SUFFIX = 'XSHG' #沪市后缀
SZ_SUFFIX = 'XSHE' #深市后缀

#在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
def init(context):
    #根据当前年月获取季报
    Q = 1
    if MONTH > 4 and MONTH < 10:
        Q = 1
    elif MONTH > 10 or MONTH < 4:
        Q = 3

    #获取股票列表、业绩报告
    stocks = ts.get_stock_basics()
    report = ts.get_report_data(2017, 3)
    logger.info("ddd")
    profit = ts.get_profit_data(YEAR, Q)
    growth = ts.get_growth_data(YEAR, Q)

    #将查询到的数据合并
    data = pd.merge(stocks, report)
    data = pd.merge(data, profit)
    data = pd.merge(data, growth)

    #数据清洗，补全空值、剔除ST股票、去重、选取列
    data.fillna(0)
    data = data.drop_duplicates('code')
    data = data[~data.name.str.contains("S")]
    data = data.loc[:,['code','name','industry', 'c_name', 'npr', 'esp', 'roe','pb','pe','nav']]

    #计算各列平均值
    mean = data.mean()
    industry_mean = data.groupby(data['industry']).mean()

    #根据指标进行选股
    data = data.loc[(data.pe>mean['pe'])&(data.pb<2)]

    data['market'] = data['code'].startswith('60') and SH_SUFFIX or SZ_SUFFIX

    # 在context中保存全局变量
    context.s1 = "000001.XSHE"
    # 实时打印日志
    logger.info("RunInfo: {}".format(context.run_info))

# before_trading此函数会在每天策略交易开始前被调用，当天只会被调用一次
def before_trading(context):
    logger.info("开盘前执行before_trading函数")

# 你选择的证券的数据更新将会触发此段逻辑，例如日或分钟历史数据切片或者是实时数据切片更新
def handle_bar(context, bar_dict):
    logger.info("每一个Bar执行")
    logger.info("打印Bar数据：")
    #logger.info(bar_dict[context.s1])

# after_trading函数会在每天交易结束后被调用，当天只会被调用一次
def after_trading(context):
    logger.info("收盘后执行after_trading函数")

#策略配置
config = {
  "base": {
    "start_date": "2016-06-01",
    "end_date": "2016-12-01",
    "benchmark": "000300.XSHG",
    "accounts": {
        "stock": 100000
    }
  },
  "extra": {
    "log_level": "verbose",
  },
  "mod": {
    "sys_analyser": {
      "enabled": True,
      "plot": True
    }
  }
}

run_func(init=init, before_trading=before_trading, handle_bar=handle_bar, config=config)
