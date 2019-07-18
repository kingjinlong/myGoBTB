
# import tushare as ts
from tqsdk import TqApi, TqSim
from datetime import datetime
from contextlib import closing
from tqsdk.tools import DataDownloader
import pandas as pd
import os
# ab = ts.get_hist_data('600848') #一次性获取全部日k线数据
# print(ab)


def test_tdsdk_quote():
    api = TqApi(TqSim())
    quote = api.get_quote("SHFE.cu1908")
    print (quote["last_price"], quote["volume"])
    while True:
        api.wait_update()
        print (quote["datetime"], quote["last_price"])

def get_all_symbol_CFFEX():
    exchange = ["CFFEX",'SHFE','DCE','CZCE','INE']
    product_CFFEX = ['IF','IC','IH','T','TF','TS']
    product_SHFE = ['rb','hc','cu','al','zn','pb','ni','sn','fu','bu','ru','sp','ag','au']
    year = ['10','11','12','13','14','15','16','17','18','19']
    month = ['01','02','03','04','05','06','07','08','09','10','11','12']
    back = []
    for valp in product_CFFEX:
        for valyear in year:
            for valmon in month:
                symbol = valp + valyear + valmon
                back.append(symbol)
    return back

def get_tqsdk_data(ex,symbol):
    bb = get_all_symbol_CFFEX()
    # # 下载从 2018-01-01 到 2018-09-01 的 SR901 日线数据
    # download_tasks["SR_daily"] = DataDownloader(api, symbol_list="CZCE.SR901", dur_sec=24*60*60,
    #                     start_dt=date(2018, 1, 1), end_dt=date(2018, 9, 1), csv_file_name="SR901_daily.csv")
    # # 下载从 2017-01-01 到 2018-09-01 的 rb主连 5分钟线数据
    # download_tasks["rb_5min"] = DataDownloader(api, symbol_list="KQ.m@SHFE.rb", dur_sec=5*60,
    #                     start_dt=date(2017, 1, 1), end_dt=date(2018, 9, 1), csv_file_name="rb_5min.csv")
    # # 下载从 2018-01-01凌晨6点 到 2018-06-01下午4点 的 cu1805,cu1807,IC1803 分钟线数据，所有数据按 cu1805 的时间对齐
    # # 例如 cu1805 夜盘交易时段, IC1803 的各项数据为 N/A
    # # 例如 cu1805 13:00-13:30 不交易, 因此 IC1803 在 13:00-13:30 之间的K线数据会被跳过
    # download_tasks["cu_min"] = DataDownloader(api, symbol_list=["SHFE.cu1805", "SHFE.cu1807", "CFFEX.IC1803"], dur_sec=60,
    #                     start_dt=datetime(2018, 1, 1, 6, 0 ,0), end_dt=datetime(2018, 6, 1, 16, 0, 0), csv_file_name="cu_min.csv")
    # 下载从 2018-05-01凌晨0点 到 2018-06-01凌晨0点 的 T1809 盘口Tick数据
    name = ex + '.' + symbol
    ff_name = './data/' + ex + '_' + symbol + '.csv'
    print(symbol)
    print(name)
    print(ff_name)

    # //检查是否存在这个文件
    bb = os.path.exists(ff_name)
    if bb==True:
        print('文件已经存在了！！')
        return

    api = TqApi(TqSim())
    download_tasks = {}
    download_tasks["T_tick"] = DataDownloader(api, symbol_list=[name], dur_sec=0,start_dt=datetime(2000, 1, 1), end_dt=datetime(2019, 6, 1), csv_file_name=ff_name)
    # 使用with closing机制确保下载完成后释放对应的资源
    with closing(api):
        while not all([v.is_finished() for v in download_tasks.values()]):
            api.wait_update()
            print("progress: " + name , { k:("%.2f%%" % v.get_progress()) for k,v in download_tasks.items() })

def load_data():
    ppname = "./data/CFFEX_IF1903.csv"
    cc = pd.DataFrame(pd.read_csv(ppname))
    print(cc)


# test_tdsdk_quote()
# get_all_symbol_CFFEX()
    # get_tqsdk_data('CFFEX','IF1811')

# vcll = ['IF1905','IF1904','IF1903','IF1902','IF1901']
# vcll = ['IF1812','IF1811','IF1810','IF1809','IF1808','IF1807','IF1806','IF1805','IF1804','IF1803','IF1802','IF1801']
# vcll = ['IF1712','IF1711','IF1710','IF1709','IF1708','IF1707','IF1706','IF1705','IF1704','IF1703','IF1702','IF1701']
# vcll = ['IF1612','IF1611','IF1610','IF1609','IF1608','IF1607','IF1606','IF1605','IF1604','IF1603','IF1602','IF1601']
# 没有数据
# vcll = ['IF1512','IF1511','IF1510','IF1509','IF1508','IF1507','IF1506','IF1505','IF1504','IF1503','IF1502','IF1501']


vcll = []
vcll.extend(['1905','1904','1903','1902','1901'])
vcll.extend(['1812','1811','1810','1809','1808','1807','1806','1805','1804','1803','1802','1801'])
vcll.extend(['1712','1711','1710','1709','1708','1707','1706','1705','1704','1703','1702','1701'])
vcll.extend(['1612','1611','1610','1609','1608','1607','1606','1605','1604','1603','1602','1601'])

# vcll.extend(['1905','1903','1901'])
# vcll.extend(['1811','1809','1807','1805','1803','1801'])
# vcll.extend(['1711','1709','1707','1705','1703','1701'])
# vcll.extend(['1611','1609','1607','1605','1603','1601'])

# vcll.extend(['1905','1903','1901'])
# vcll.extend(['1809','1805','1801'])
# vcll.extend(['1709','1705','1701'])
# vcll.extend(['1609','1605','1601'])



# vcll.extend(['905','904','903','902','901'])
# vcll.extend(['812','811','810','809','808','807','806','805','804','803','802','801'])
# vcll.extend(['712','711','710','709','708','707','706','705','704','703','702','701'])
# vcll.extend(['612','611','610','609','608','607','606','605','604','603','602','601'])


# vcll.extend(['905','901'])
# vcll.extend(['809','805','801'])
# vcll.extend(['709','705','701'])
# vcll.extend(['609','605','601'])




# vcll.extend(['1601'])   '905',


# vcll.extend(['1512','1511','1510','1509','1508','1507','1506','1505','1504','1503','1502','1501'])

# IH IC IF 
# rb hc cu al zn pb ni sn fu ag au bu 
# fu 1802 后
# 
# 

#SR CF CY ZC FG MA TA  ZC RM OI SF SM AP

#m y p a b c cs l pp v jd j jm i

# for val in vcll:
#     ins  = "T" + val
#     # print(ins)
#     get_tqsdk_data('CFFEX',ins)
#     # get_tqsdk_data('SHFE',ins)
#     # get_tqsdk_data('CZCE',ins)
#     # get_tqsdk_data('DCE',ins)


# load_data()

#get kline


def get_tqsdk_data_kline():
    api = TqApi(TqSim())
    download_tasks = {}
    download_tasks["yzyl0905_min"] = DataDownloader(api, symbol_list=["DCE.m1905", "DCE.y1905", "DCE.p1905","CZCE.RM905", "CZCE.OI905",], dur_sec=60,
                        start_dt=datetime(2019, 2, 1, 0, 0 ,0), end_dt=datetime(2019, 4, 28, 0, 0, 0), csv_file_name="cu_min.csv")
    # 使用with closing机制确保下载完成后释放对应的资源
    with closing(api):
        while not all([v.is_finished() for v in download_tasks.values()]):
            api.wait_update()
            print("progress: "  , { k:("%.2f%%" % v.get_progress()) for k,v in download_tasks.items() })


get_tqsdk_data_kline()
print('end ')
