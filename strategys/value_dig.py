# -*- coding: UTF-8 -*-
import datetime
from WindPy import w
from rqalpha.api import *
from rqalpha import run_func
import tushare as ts
import pandas as pd
import numpy as np
import xlrd
import openpyxl

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

        #ex = ts.get_hist_data(code).head(1)
        #如果收盘价低于20日均价则买入
        #if ex['ma20'][0] > ex['close'][0]:
        order_book_id = get_order_book_id(code,'rqalpha')
        if order_book_id in list(context.portfolio.positions.keys()):
            continue
        elif not is_suspended(order_book_id):
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

    logger.info('1.正在更新股池~~~~' + str(context.now.year) + '-' + str(Month) + '-' + str(Day))
    logger.info('查询的报告年度与季度：' + str(Year) + '-' + str(q))
    #查询最新股票数据,股票列表、业绩报告（主表）、盈利能力、成长能力
    data = ts.get_report_data(Year,q)
    logger.info('1.1 tushare get_report_data success')
    data.to_excel(context.Dir + '/data/merge.xlsx', encoding = 'utf-8')
    #调整数据，0补全空值、剔除ST、去重、取评估指标列
    data.fillna(0)
    data = data[~data.name.str.contains("S")]
    data = data.drop_duplicates('name')
    data = data.loc[(data.roe > 0)&(data.net_profits > 0)&(data.profits_yoy > 0)&(data.eps_yoy>0)]
    #data = data.head(20)

    #估值指标list
    #pe
    pe_ttms = []
    #总市值/息税折旧及摊销前利润ttm行业相对值
    val_pebitdaindu_ttms = []
    #pb市净率行业相对值
    val_pbindus = []
    #净资产收益率
    fa_roeexdiluteds = []
    trade_codes = []

    codes = data.code.values
    code_num = len(codes)
    count = 0

    logger.info('1.2 从wind平台获取估值指标数据~~~')
    w.start();
    for code in codes:
        count = count + 1
        bookid = get_order_book_id(code,'wind')
        date = context.now.strftime("%Y-%m-%d")
        wsd_data = w.wsd(bookid, "pe_ttm,val_pebitdaindu_ttm,val_pbindu,fa_roeexdiluted,trade_code", date, date, "")
        logger.info(str(count) + '/' + str(code_num) + '------' + str(wsd_data.ErrorCode))
        if wsd_data.ErrorCode is 0:
            pe_ttms.append(wsd_data.Data[0][0])
            val_pebitdaindu_ttms.append(wsd_data.Data[1][0])
            val_pbindus.append(wsd_data.Data[2][0])
            fa_roeexdiluteds.append(wsd_data.Data[3][0])
            trade_codes.append(wsd_data.Data[4][0])
        else:
            pe_ttms.append(0)
            val_pebitdaindu_ttms.append(0)
            val_pbindus.append(0)
            fa_roeexdiluteds.append(0)
            trade_codes.append(0)

    #整理估值指标数据，0填充None
    pe_ttms = map(NoneTo0, pe_ttms)
    val_pebitdaindu_ttms = map(NoneTo0, val_pebitdaindu_ttms)
    val_pbindus = map(NoneTo0, val_pbindus)
    fa_roeexdiluteds = map(NoneTo0, fa_roeexdiluteds)
    trade_codes = map(NoneTo0, trade_codes)
    #将估值指标相关数据构建一个dataframe
    wsd_df = pd.DataFrame(
        {
        'pe_ttm':pe_ttms,
        "val_pebitdaindu_ttm":val_pebitdaindu_ttms,
        "val_pbindu":val_pbindus,
        "fa_roeexdiluted":fa_roeexdiluteds,
        "code":trade_codes
        },
        columns =['pe_ttm','val_pebitdaindu_ttm','val_pbindu','fa_roeexdiluted','code'])

    #将估值指标数据合并到主表
    data = pd.merge(data, wsd_df, on = ['code'])

    #data.fillna(0)
    data.to_excel(context.Dir + '/data/with_wsd.xlsx', encoding = 'utf-8')
    #先删除估值指标为0的标的，不参与计算平均值
    data = data.loc[(data.pe_ttm>0)&(data.fa_roeexdiluted>0)]
    #求均值
    mean = data.mean()
    #按指标筛选股票
    _val_pbindu = mean['val_pbindu'] * 0.5
    data = data.loc[(data.pe_ttm>mean['pe_ttm'])&(data.val_pbindu<_val_pbindu)]
    #如果标的数量大于20再根据净资产收益率进行筛选
    if(len(data.pe_ttm.values)>30):
        mean = data.mean()
        data = data.loc[(data.fa_roeexdiluted>mean['fa_roeexdiluted'])]
    data.sort_values(by=['val_pbindu','fa_roeexdiluted'])

    #更新候选股票数据
    context.stocks = data
    context.codes = data.code.values

    #保存最新更新的股票池数据
    backup = context.Dir + '/data/' + str(Year) + str(Month) + str(Day) + '.xlsx'
    data.to_excel(backup, encoding = 'utf-8')
    logger.info('股池已完成更新:' + backup)

#根据code返回市场标签
def get_order_book_id(x, ctype='rqalpha'):
    SZ_SUFFIX = 'XSHE'  #00或者30开头的深市股票
    SH_SUFFIX = 'XSHG'  #600开头的沪市股票
    if ctype is 'wind':
        SZ_SUFFIX = 'SZ'
        SH_SUFFIX = 'SH'
    if x.startswith('00') or x.startswith('30'):
        return x + '.' + SZ_SUFFIX
    elif x.startswith('60'):
        return x + '.' + SH_SUFFIX

#0替换None
def NoneTo0(s):
    if s is None:
        return 0
    else:
        return s

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
