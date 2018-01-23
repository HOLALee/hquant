#!/usr/bin/python
# -*- coding: UTF-8 -*-

import datetime

"""
基础模块
1.getYearAndQua   获取当前的年份与季度
"""
def getYearAndQua():
    y = datetime.datetime.now().year
    m = datetime.datetime.now().month;
    if(m>=1 and m<=3):
        m = 1
    elif(m>=4 and m<=6):
        m = 2
    elif(m>=7 and m<=9):
        m = 3
    elif(m>=10 and m<=12):
        m = 4
    return y,m


if __name__ == '__main__':
    print getYearAndQua()
