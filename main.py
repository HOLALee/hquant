#!\usr\bin\python
# -*- coding: utf-8 -*-

import os,sys
import pandas as pd
import tushare as ts
from rqalpha.api import *
from WindPy import w


def getStockBase():
    stock_list = industry('A01')
    return stock_list

if __name__ == '__main__':
    w.start(); #u"date=20130608;sector=全部A股"
    #industry_data = w.wset("indscalestatbywind","industrytype=证监会行业;enddate=2018-02-12")
    sector_data = w.wset("sectorconstituent",u"date=2010-02-12;sectorname=CSRC林业")
    print len(sector_data.Data[1])
