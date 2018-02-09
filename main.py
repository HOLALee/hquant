#!\usr\bin\python
# -*- coding: utf-8 -*-

import os,sys
import pandas as pd
import tushare as ts
from rqalpha.api import *


def getStockBase():
    stock_list = industry('A01')
    return stock_list

if __name__ == '__main__':
    data = getStockBase()
    print data
