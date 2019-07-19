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
import glbase as glb
import matplotlib.pyplot as plt
from pandas import to_datetime

from datetime import datetime

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

def test_movement_thread1():
    print("测试动量策略")
    pos_File = ".\data-yhh\D1_position.xlsx"
    data_File = ".\data-yhh\D1.xlsx"
    glb.glb_initial_money = 1000000.0
    glb.glb_open_commission = 0.001
    glb.glb_close_commission = 0.001
    cc_pos = pd.DataFrame(pd.read_excel(pos_File))
    cc_data = pd.DataFrame(pd.read_excel(data_File))
    print(cc_data)
    print(cc_pos)
    # all_tradeDetail,all_vc_money,df_back,result,df_mm = glb.cal_vc_pos_kl_dataframe(cc_data,cc_pos,10,10,False,True)
    #all_tradeDetail,all_vc_money,df_back,result,df_mm = glb.cal_vc_pos_kl_dataframe(cc_data,cc_pos,True,True)


# def test(arr):
#     arr1 = arr.copy()
#     arr2 = arr.copy()
#     for i in range(0,len(arr)):
#         for j in range(0,len(arr)-i-1):
#             if arr[j] > arr[j+1]:
#                 arr[j],arr[j+1] = arr[j+1], arr[j]
#     indexs = []
#     for i in arr2:
#         for index in range(0,len(arr)):
#             if i == arr[index]:
#                 indexs.append(index)
#     return indexs

def quchong(arr):
    for i in range(0,len(arr)):
        for j in range(i+1,len(arr)):
            if arr[j] == arr[i]:
                arr[j] += 1
    if len(set(arr))!=len(arr):
        quchong(arr)
    return arr

def test(arr):
    arr = quchong(arr)
    arr2 = arr.copy()
    for i in range(0,len(arr)):
        for j in range(0,len(arr)-i-1):
            if arr[j] > arr[j+1]:
                arr[j],arr[j+1] = arr[j+1], arr[j]
    indexs = []
    for i in arr2:
        indexs.append(arr.index(i))
    return indexs

def test_movement_thread2():
    print("测试对冲策略")
    date_File = "cu_min.csv"
    cc_data = pd.DataFrame(pd.read_csv(date_File))
    N=len(cc_data)
    R = 30
    H = 30
    n = N
    aa_data = pd.DataFrame()
    aa_data["m"] = cc_data['DCE.m1905.close'][0:n]
    aa_data["RM"] = cc_data['CZCE.RM905.close'][0:n]
    aa_data["y"] = cc_data['DCE.y1905.close'][0:n]
    aa_data["p"] = cc_data['DCE.p1905.close'][0:n]
    aa_data["OI"] = cc_data['CZCE.OI905.close'][0:n]
    # aa_data = aa_data.set_index('日期')
    #提取商品名字
    commodity_name = aa_data.columns.values.tolist()  
    spread_data = aa_data.diff(periods = R)
    # print(spread_data)

    # positable=np.zeros(shape=(len(aa_data),aa_data.columns.size))
    positable=np.zeros(shape=(0,aa_data.columns.size))
    df_empty = pd.DataFrame(positable)
    df_empty.columns=commodity_name
    # df_empty['datetime']=cc_data['datetime']
    # df_empty = df_empty.set_index('datetime')
    spread_data = spread_data.fillna(0)

    df_pos = pd.DataFrame(positable)
    df_pos.columns = commodity_name
    daytt = []
    ii = 0
    for index, row in spread_data.iterrows():
        # aa = [i[0] for i in sorted(enumerate(row), key=lambda x:x[1],reverse = False)]
        mulist = []
        for i in range(len(row)):
            mulist.append(float(row[i]))
        aa = test(mulist)


        # if ii == 12:
        #     print(((row)))
        #     mulist = []
        #     for i in range(len(row)):
        #         mulist.append(float(row[i]))
        #     print(test(mulist))
        # #     print(sorted(enumerate(row)))
        # #     print(enumerate((row)))
        #     return

        df_empty.loc[index] = aa
        bb = []
        if ii <R:
            bb = [0,0,0,0,0]
        else:
            if (ii - R) % H == 0:
                #换仓点
                for i in range(len(aa)):
                    if aa[i] == 0: bb.append(-1)
                    if aa[i] == 1: bb.append(-1)
                    if aa[i] == 2: bb.append(0)
                    if aa[i] == 3: bb.append(1)
                    if aa[i] == 4: bb.append(1)
            else:
                bb = df_pos.iloc[ii - 1].tolist()
        df_pos.loc[index] = bb
        ii = ii +1
    # print(spread_data[10:15])
    # print(df_empty[10:15])
    # return
    cc_data.datetime = to_datetime(cc_data.datetime,format="%Y-%m-%d %H:%M:%S")
    cc_data.datetime=cc_data.datetime.apply(lambda x: datetime.strftime(x,"%Y-%m-%d"))

    spread_data = spread_data.fillna(0)
    # spread_data.drop(index=[0],axis=1,inplace=True)
    df_pos = df_pos.shift(-1)
    # aa_data["日期"] = cc_data['datetime'][0:500]
    # df_pos["日期"] = cc_data['datetime'][0:500]
    result = df_pos * spread_data
    result = result.fillna(0)
    #列求和
    result = result.cumsum(0)
    result['totalProfit'] = result.apply(lambda x: x.sum(), axis=1)
    result['totalProfit'].plot()
    print(result)
    plt.show()
test_movement_thread2()
# test_movement_thread2()

print('ALL IS END......')