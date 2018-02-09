# -*- coding:utf-8 -*-
#Python 3.5.0
from WindPy import w
import pandas as pd
import datetime
#w.start();

def format_name(s):
    if s is None:
        return 0
    else:
        return s

print map(format_name, [None, 2, 3, 4, 5, 6, 7, 8, 9])

# pe_ttms = []
# val_pebitdaindu_ttms = []
# val_pbindus = []
# for code in ['000001.SZ','000002.SZ','000003.SZ']:
#     wsd_data=w.wsd(code, "pe_ttm,val_pebitdaindu_ttm,val_pbindu", "2015-12-10", "2015-12-10", "Fill=Previous")
#     print wsd_data
#     pe_ttms.append(wsd_data.Data[0][0])
#     val_pebitdaindu_ttms.append(wsd_data.Data[1][0])
#     val_pbindus.append(wsd_data.Data[2][0])
#
# print pe_ttms
# print val_pebitdaindu_ttms
# print val_pbindus


#演示如何将api返回的数据装入Pandas的DataFrame
# fm=pd.DataFrame(wsd_data.Data,index=wsd_data.Fields,columns=wsd_data.Times)
# fm=fm.T #将矩阵转置
# print('fm:/n',fm)
