# -*- coding:utf-8 -*-
import tushare as ts
from common import base

#获取当前年份与季度
(year,q) = base.getYearAndQua()

#获取业绩报表数据
def get_report_data():
    return ts.get_report_data(year,q)
