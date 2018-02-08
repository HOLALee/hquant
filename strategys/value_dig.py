# -*- coding: UTF-8 -*-
import datetime
from rqalpha.api import *
from rqalpha import run_func
import tushare as ts
import pandas as pd
import numpy as np
import xlrd
import openpyxl

SZ_SUFFIX = 'XSHE'  #00或者30开头的深市股票
SH_SUFFIX = 'XSHG'  #600开头的沪市股票

"""
init初始化逻辑
context对象将算法策略的任何方法之间做传递。
"""
def init(context):
    #股池备份数据存储目录
    context.Dir = 'D:\GitHub\hquant'
    #策略交易标的集
    context.targets = []
    context.codes = []
    #定时任务：每周一开市后5分钟进行调仓
    scheduler.run_monthly(start, tradingday =1, time_rule = market_open(minute=10))
    logger.info('初始化时间：' +  context.now.strftime("%Y-%m-%d %H:%M:%S"))

# before_trading 策略交易开始前准备，每天只会被调用一次
def before_trading(context):
    #logger.info("----------------------------Are U Ready?!------------------------------")
    #select_stock(context)
    pass

#调仓
def start(context,bar_dict):
    logger.info("----------------------------Are U Ready?!------------------------------")
    select_stock(context)
    logger.info('2.开始调仓~~~~')
    sell_stock(context,bar_dict)  #先卖出股票再买入

    logger.info('4.buy_stock~~~')
    for code in context.codes:
        if len(context.portfolio.positions) >= 10:
            break
        ex = ts.get_hist_data(code).head(1)
        #如果收盘价低于20日均价则买入
        #if ex['ma20'][0] > ex['close'][0]:
        order_book_id = None
        if code.startswith('00') or code.startswith('30'):
            order_book_id = code + '.XSHE'
        elif code.startswith('60'):
            order_book_id = code + '.XSHG'

        if not is_suspended(order_book_id):
            buy_stock(context,order_book_id)

    logger.info('最新持仓标的：')
    logger.info(context.portfolio.positions.keys())
    logger.info('------------------------------finish--------------------------')

#卖出股票
def sell_stock(context,bar_dict):
    logger.info('3.sell_stock~~~')
    logger.info(context.portfolio.positions.keys())
    for order_book_id in list(context.portfolio.positions.keys()):
        code = order_book_id[0:6]
        if not (code in context.codes):
            logger.info('卖出：' + code)
            order_target_value(order_book_id,0)  #如果不在股票列表中则全部卖出

#买入股票
def buy_stock(context,order_book_id):
    logger.info(order_book_id)
    context.percentage = 1
    stock_buy_num = 10 #最多买入股票数量
    stock_percentage = 0.99/stock_buy_num  #每支股票买入的最大仓位
    #logger.info('positions:' + str(len(context.portfolio.positions)))
    if len(context.portfolio.positions) < stock_buy_num:
        if stock_percentage > context.percentage:  #设置单支股票最大买入仓位
            stock_percentage = context.percentage   #更换买入仓位
        order_percent(order_book_id, stock_percentage)     #买入股票

# 你选择的证券的数据更新将会触发此段逻辑，例如日或分钟历史数据切片或者是实时数据切片更新
def handle_bar(context, bar_dict):
    pass

# after_trading函数会在每天交易结束后被调用，当天只会被调用一次
def after_trading(context):
    logger.info("----------------------------Game Over?!------------------------------")


#选股
def select_stock(context):
    #取出当前年月日
    Year = context.now.year
    Month = context.now.month
    Day = context.now.day
    #默认去1季度报
    q = 1
    #4月~8月，取1季度报
    if Month > 4 and Month < 8:
        q = 1
    #8月~10月，取2季度报
    elif Month > 8 and Month < 10:
        q = 2
    #10月~12月，取3季度报
    elif Month > 10 and Month < 12:
        q = 3
    #1月~4月，取前一年3季度报
    elif Month > 0 and Month < 4:
        Year = Year - 1
        q = 3
    logger.info('1.正在更新股池~~~~' + str(Year) + '-' + str(Month) + '-' + str(Day) + ':' + str(q))
    #查询最新股票数据,股票列表、业绩报告（主表）、盈利能力、成长能力
    data = ts.get_report_data(Year,q)
    data.to_excel(context.Dir + '/data/merge.xlsx', encoding = 'utf-8')
    #调整数据，0补全空值、剔除ST、去重、取评估指标列
    data.fillna(0)
    data = data[~data.name.str.contains("S")]
    data = data.drop_duplicates('name')
    #data = data.loc[:,['name','esp','pb','pe','esp','npr']]
    data.to_excel(context.Dir + '/data/clean.xlsx', encoding = 'utf-8')
    #求均值
    mean = data.mean()
    #按指标筛选股票
    data = data.loc[(data.eps_yoy < mean['eps_yoy'])&(data.bvps > mean['bvps'])&(data.roe>mean['roe'])]
    data.sort_values(by=['roe','eps_yoy'])

    #更新候选股票数据
    context.stocks = data
    context.codes = data.code.values

    #保存最新更新的股票池数据
    backup = context.Dir + '/data/' + str(Year) + str(Month) + str(Day) + '.xlsx'
    data.to_excel(backup, encoding = 'utf-8')
    logger.info('股池已完成更新:' + backup)

#根据code返回市场标签
def getMarket(self,x):
    if x.startswith('00') or x.startswith('30'):
        return SZ_SUFFIX
    elif x.startswith('60'):
        return SH_SUFFIX

#策略配置
config = {
  "base": {
    "start_date": "2015-01-01",
    "end_date": "2017-12-30",
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

if __name__ == '__main__':
    run_func(init=init, before_trading=before_trading, handle_bar=handle_bar, config=config)
