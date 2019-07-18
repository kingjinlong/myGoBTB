import tushare as ts
import time
import math
import cmath
import csv
import numpy as np
import datetime
import os 
import pandas as pd
from collections import defaultdict


def test_movement_thread():
    print("测试tick策略")
    date_File = ".\data\DCE_y1601.csv"
    cc_data = pd.DataFrame(pd.read_csv(date_File))
    print(cc_data)

    N=len(cc_data)
    
    print(N)
    print(cc_data.columns)



    # #收盘价中 缺失值的处理 沿用上一收盘价
    for i in range(3,N,1):
        if (cc_data['ask_price1'].loc[i] > cc_data['ask_price1'].loc[i - 1]
            and cc_data['ask_price1'].loc[i - 1] > cc_data['ask_price1'].loc[i - 2]
            and cc_data['ask_price1'].loc[i - 2] > cc_data['ask_price1'].loc[i - 3]):
            print('aaaa' + str(i))

        if (cc_data['bid_price1'].loc[i] < cc_data['bid_price1'].loc[i - 1]
            and cc_data['bid_price1'].loc[i - 1] < cc_data['bid_price1'].loc[i - 2]
            and cc_data['bid_price1'].loc[i - 2] < cc_data['bid_price1'].loc[i - 3]):
            print('bbbb' + str(i))

        if (cc_data['bid_price1'].loc[i] > cc_data['bid_price1'].loc[i - 1]
            and cc_data['bid_price1'].loc[i - 1] < cc_data['bid_price1'].loc[i - 2]):
            print('ccc' + str(i))

        if (cc_data['ask_price1'].loc[i] < cc_data['ask_price1'].loc[i - 1]
            and cc_data['ask_price1'].loc[i - 1] > cc_data['ask_price1'].loc[i - 2]):
            print('ddd' + str(i))


        # ask_price1 = cc_data['ask_price1'].loc[i]
        # ask_volume1 = cc_data['ask_volume1'].loc[i]
        # bid_price1 = cc_data['bid_price1'].loc[i]
        # bid_volume1 = cc_data['bid_volume1'].loc[i]




        # print(ask_price1)


        # for j in range(1,cc_data.columns.size-1,1):

def test_movement_thread2():
    print("测试tick策略")
    date_File = "cu_min.csv"
    cc_data = pd.DataFrame(pd.read_csv(date_File))
    # cc_data = origin_data.set_index('datetime')
    print(cc_data)
    
    N=len(cc_data)
    R = 10

    print(N)
    print(cc_data.columns)

    aa_data = pd.DataFrame()
    aa_data["datetime"] = cc_data['datetime']
    aa_data["m"] = cc_data['DCE.m1905.close']
    aa_data["RM"] = cc_data['CZCE.RM905.close']
    aa_data["y"] = cc_data['DCE.y1905.close']
    aa_data["p"] = cc_data['DCE.p1905.close']
    aa_data["OI"] = cc_data['CZCE.OI905.close']
    aa_data = aa_data.set_index('datetime')
    #提取商品名字
    commodity_name = aa_data.columns.values.tolist()  
    spread_data = aa_data.diff(periods = R)
    print(spread_data)

    ###创建一个空的order数据框
    positable=np.zeros(shape=(0,aa_data.columns.size))
    df_empty = pd.DataFrame(positable)
    df_empty.columns=commodity_name
    print(df_empty)
    # df_empty['datetime']=cc_data['datetime']
    # df_empty = df_empty.set_index('datetime')



    ii = 0
    for index, row in spread_data.iterrows():
        aa = [i[0] for i in sorted(enumerate(row), key=lambda x:x[1])]
        # print(str(index) + str(aa))
        df_empty=df_empty.append(pd.DataFrame(aa),ignore_index=True)
        if ii>20:
            break
        ii = ii+1

    print(df_empty )

# #创建一个空的Dataframe
# result =pd.DataFrame(columns=('idx','degree','weight','diameter'))
# #将计算结果逐行插入result,注意变量要用[]括起来,同时ignore_index=True，否则会报错，ValueError: If using all scalar values, you must pass an index
# for i in idx:
#     degree=
#     weight=
#     diameter=
#     result=result.append(pd.DataFrame({'idx':[i],'degree':[degree],'weight':[weight],'diameter':[diameter]}),ignore_index=True

# df.loc[i] = kjcgml.loc[i].append(bzwzcgml.loc[j])



    # #删除中文字，日期
    # del commodity_name[0]        
    # #计算每个品种每隔R天的收益率
    # rate_return=[]
    # for index, value in enumerate(commodity_name):
    #     rate_list=[]    
    #     for i in range(R-1,N,1):    
    #         print(aa_data[value][i])        
    #         rate=(aa_data[value][i]-aa_data[value][i-(R-1)])/aa_data[value][i-(R-1)]
    #         rate_list.append(rate)
    #     rate_return.append(rate_list)


a = [3,4,2,5,6]

test_movement_thread2()

myList = [1, 2, 3, 100, 5]
aa = [i[0] for i in sorted(enumerate(myList), key=lambda x:x[1])]
# [0, 1, 2, 4, 3]
print(aa)