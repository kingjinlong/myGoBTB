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
    print("测试对冲策略")
    date_File = "cu_min.csv"
    cc_data = pd.DataFrame(pd.read_csv(date_File))
    N=len(cc_data)
    R = 10
    H = 5

    print(N)
    print(cc_data.columns)

    aa_data = pd.DataFrame()
    aa_data["datetime"] = cc_data['datetime'][0:500]
    aa_data["m"] = cc_data['DCE.m1905.close'][0:500]
    aa_data["RM"] = cc_data['CZCE.RM905.close'][0:500]
    aa_data["y"] = cc_data['DCE.y1905.close'][0:500]
    aa_data["p"] = cc_data['DCE.p1905.close'][0:500]
    aa_data["OI"] = cc_data['CZCE.OI905.close'][0:500]
    aa_data = aa_data.set_index('datetime')
    #提取商品名字
    commodity_name = aa_data.columns.values.tolist()  
    spread_data = aa_data.diff(periods = R)
    print(spread_data)

    # positable=np.zeros(shape=(len(aa_data),aa_data.columns.size))
    positable=np.zeros(shape=(0,aa_data.columns.size))
    df_empty = pd.DataFrame(positable)
    df_empty.columns=commodity_name
    # df_empty['datetime']=cc_data['datetime']
    # df_empty = df_empty.set_index('datetime')

    df_pos = pd.DataFrame(positable)
    df_pos.columns = commodity_name

    ii = 0
    for index, row in spread_data.iterrows():
        aa = [i[0] for i in sorted(enumerate(row), key=lambda x:x[1])]
        df_empty.loc[index] = aa
        bb = []
        if ii <R:
            bb = [0,0,0,0,0]
        else:
            if (ii - R) % H == 0:
                #换仓点
                for i in range(len(aa)):
                    if aa[i] == 0: bb.append(1)
                    if aa[i] == 1: bb.append(1)
                    if aa[i] == 2: bb.append(0)
                    if aa[i] == 3: bb.append(-1)
                    if aa[i] == 4: bb.append(-1)
            else:
                bb = df_pos.iloc[ii - 1].tolist()
        df_pos.loc[index] = bb
        ii = ii +1
    print(df_pos)
  
test_movement_thread2()
print('ALL IS END......')