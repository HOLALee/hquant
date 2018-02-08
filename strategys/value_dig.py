# -*- coding: UTF-8 -*-
import datetime
from rqalpha.api import *
from rqalpha import run_func
import tushare as ts
import pandas as pd
import numpy as np

YEAR = datetime.datetime.now().year

#在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
def init(context):
    context.dir = 'D:\GitHub\hquant'
    #定时任务：每周一进行一次选股
    scheduler.run_weekly(selectStock, weekday=1)
    # 在context中保存全局变量
    context.s1 = "000001.XSHE"

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


#选股
def selectStock(context, bar_dict):
    logger.info('更新股池~~~~')
    YEAR = datetime.datetime.now().year
    MONTH = datetime.datetime.now().month
    DAY = datetime.datetime.now().day
    Q = 1
    if MONTH > 4 and MONTH < 8:
        Q = 1
    elif MONTH > 8 and MONTH < 10:
        Q = 2
    elif MONTH > 10 and MONTH:
        Q = 3

    basics = ts.get_stock_basics()
    report = ts.get_report_data(YEAR, Q)
    profit = ts.get_profit_data(YEAR, Q)
    growth = ts.get_growth_data(YEAR, Q)

    data = pd.merge(basics, report)
    data = pd.merge(data, profit)
    data = pd.merge(data, growth)

    data.fillna(0)
    data = data[~data.name.str.contains("S")]
    data = data.drop_duplicates('code')
    data = data.loc[:,['code','name','industry', 'c_name','npr', 'esp', 'roe','pb','pe','nav','gross_profit_rate']]
    mean = data.mean()
    data = data.loc[(data.pe>mean['pe'])&(data.pb<2)]

    data.to_excel(context.dir + '/data/' + YEAR + MONTH + DAY + '.xlsl')
    logger.info('股池已完成更新！')

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
    #"log_level": "verbose",
  },
  "mod": {
    "sys_analyser": {
      "enabled": True,
      "plot": True
    }
  }
}

run_func(init=init, before_trading=before_trading, handle_bar=handle_bar, config=config)
