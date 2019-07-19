import time
import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas
import datetime
import math

# 函数说明:
##############################################全局变量申明
#一年定期无风险收益率
glb_noRisk_ratio = 0.0175
#初始测算资金
glb_initial_money = 1000000
#全局初始开仓手续费
glb_open_commission = 0.0005
#全局初始平仓手续费
glb_close_commission = 0.0005
##############################################外部函数
# load_kline
# cal_vc_pos_kl_dataframe：外部调用
# cal_vc_pos_kl_dataframe_byStatus:外部调用
##############################################内部函数
# cal_vc_pos_kl：内部调用，外部不用考虑
# cal_pos_kl：内部调用，外部不用考虑
# cal_tradeDetail:统计成交明细的一些指标
# CalMoney：统计一个净值序列的详细指标
# MaxDrawdown：最大回撤的计算
###############################################

#k线定义
class kline:
    def __init__(self):
     self.name = ''
     self.date = 0
     self.open = 0.0
     self.high = 0.0
     self.low = 0.0
     self.close = 0.0

#测试参数
class InsBase:
    def __init__(self):
     self.name = ''
     self.volumeMulti = 1 #价格系数、合约乘数
     self.open_commission = glb_open_commission
     self.close_commission = glb_close_commission

#成交明细
class tradeDetail:
    def __init__(self):
        self.name = ""
        self.side = 0
        self.open_day = 0
        self.open_price = 0.0
        self.close_day = 0
        self.close_price = 0.0
        self.volume = 0
        self.close_profit = 0
        self.drawdown =0
        self.open_commission = 0.0
        self.close_commission = 0.0

#统计结果
class strategyCalRes:
    def __init__(self):
        self.name = ""
        self.start_date = '' #开始日期
        self.end_date = '' #结算日期
        self.initial_balance = 0 #初始资金
        self.end_balance = 0 #期末资金
        self.total_ratio = 0 # 总收益率
        self.annul_ratio = 0 # 年化收益率
        self.normal_day = 0 #自然日
        self.trade_day = 0 #交易日
        self.number_of_profit_days = 0 #盈利的日子
        self.number_of_loss_days = 0 #亏损的日子
        self.total_return = 0 #总盈亏
        self.total_return_profit = 0 #总盈利额
        self.total_return_loss = 0 #总亏损额
        self.number_of_trades = 0 #总交易笔数
        self.number_of_profit_trades = 0 #盈利笔数
        self.number_of_loss_trades = 0 #亏损笔数
        self.avg_profit = 0 #单笔平均盈利
        self.avg_loss = 0 #单笔平均亏损
        self.max_profit = 0.0 #最大单笔盈利
        self.max_loss = 0.0 #最大单笔亏损
        self.profit_probability = 0.0#胜率
        self.profit_loss_ratio = 0.0#盈亏比
        self.total_commission = 0#总手续费
        self.max_drawdown = 0 #最大回撤比例
        self.max_duration_in_drawdown = 0 #最大回撤持续时间
        self.sharpe_ratio = 0

        self.total_net_pnl = 0
        self.max_margin = 0
        self.max_win_holding_pnl = 0 #最大持仓盈利
        self.max_loss_holding_pnl = 0 #最大持仓浮亏
        self.sortino_ratio = 0
        self.avg_daily_pnl  = 0
        self.avg_daily_commission = 0
        self.avg_daily_return = 0
        self.avg_daily_std = 0
        self.annual_compund_return = 0
        self.annual_average_return = 0
        self.annual_std = 0
        self.pnl = 0

# 读取k线数据:A0001.DCE	2000/1/18 00:00:00	1940	1920	1920	1940	10	0	376
def load_kline(filename):
    rr = []
    with open(filename) as f:
        reader = csv.reader(f)
        for row in list(reader):
            a = kline()
            a.name = row[0]
            a.date = row[1]
            a.open = row[2]
            a.high = row[3]
            a.low = row[4]
            a.close = row[5]
            rr.append(a)
    return rr

def print_trade_detail(dd):
    print("开仓日期-" + str(dd.open_day) + ":开仓价格-" + str(dd.open_price) + ":平仓日期-" + str(dd.close_day) +":平仓价格-" + str(dd.close_price) +":方向-" + str(dd.side) + ":利润-" + str(dd.close_profit))

def print_strategyCalRes(self):
    print("----------------------测试总回报报告----------------")
    print("标的",'\t','\t',self.name)
    print("开始日期",'\t',self.start_date)
    print("结束日期",'\t',self.end_date)
    print("自然日",'\t','\t',self.normal_day)
    print("交易日",'\t','\t',self.trade_day)
    print("盈利日",'\t','\t',str(self.number_of_profit_days))
    print("亏损日",'\t','\t',self.number_of_loss_days)
    print("期初资金",'\t',self.initial_balance)
    print("期末资金",'\t',self.end_balance)
    print("总收益率",'\t',self.total_ratio)
    print("年化收益率",'\t',self.annul_ratio)
    print("最大回撤率",'\t',self.max_drawdown)
    print("最大回撤时间",'\t',self.max_duration_in_drawdown)
    print("夏普率",'\t','\t',self.sharpe_ratio)
    print("总盈亏",'\t','\t',self.total_return)
    print("总盈利额",'\t',self.total_return_profit)
    print("总亏损额",'\t',self.total_return_loss)
    print("总交易笔数",'\t',self.number_of_trades)
    print("盈利笔数",'\t',self.number_of_profit_trades)
    print("亏损笔数",'\t',self.number_of_loss_trades)
    print("单笔平均盈利",'\t',self.avg_profit)
    print("单笔平均亏损",'\t',self.avg_loss)
    print("最大单笔盈利",'\t',self.max_profit)
    print("最大单笔亏损",'\t',self.max_loss)
    print("胜率",'\t','\t',self.profit_probability)
    print("盈亏比",'\t','\t',self.profit_loss_ratio)
    print("总手续费",'\t',self.total_commission)

def MaxDrawdown(return_list):
    print("最大回撤率")
    bb = ((return_list.cummax()-return_list)/return_list.cummax()).max()
    return round(bb,4)

def CalMoney(total_money,total_date):
    total_size = len(total_date)
    # 净值曲线 最大回撤额 最大回撤率 最大回撤持续时间
    code = 'total'
    df = pandas.DataFrame()
    df[code] = total_money
    df['mt'] = df[code].expanding().max()
    df['pt'] = df[code]/df['mt']
    df['drawdown'] = 1 - df['pt']
    min_point_total = df.sort_values(by=['pt']).iloc[[0], df.columns.get_loc('pt')]
    max_point_total = df[df.index <= min_point_total.index[0]].sort_values(by=[code],ascending=False).iloc[[0],df.columns.get_loc(code)]
    df_new = df/df.iloc[0]
    # ss = {}
    # ss[code] = MaxDrawdown(df[code])
    # MD = pandas.DataFrame(ss,index=['最大回撤']).T
    rets = (df.fillna(method='pad')).apply(lambda x:x/x.shift(1)-1)[1:]
    rets.head()
    exReturn = rets- glb_noRisk_ratio / 250
    sharperatio = np.sqrt(len(exReturn))*exReturn.mean()/exReturn.std()

    print("-------------------------------")
    print('exReturn')
    print(exReturn)
    print("-------------------------------")
    print(sharperatio)
    print("-------------------------------")


    result = strategyCalRes()
    result.name = '净值'
    result.initial_balance = total_money[0]
    result.end_balance = total_money[total_size -1 ]
    result.start_date = total_date[0]
    result.end_date = total_date[total_size -1 ]
    result.trade_day = total_size
    t = time.strptime(str(result.start_date)[0:10],"%Y-%m-%d") #struct_time类型
    d = datetime.datetime(t[0], t[1],t[2]) #datetime类型
    t1 = time.strptime(str(result.end_date)[0:10],"%Y-%m-%d") #struct_time类型
    d1 = datetime.datetime(t1[0], t1[1],t1[2]) #datetime类型
    result.normal_day = (d1 - d).days
    result.max_drawdown = MaxDrawdown(df[code])
    # result.max_duration_in_drawdown = (total_date[min_point_total.index[0]] - total_date[max_point_total.index[0]])
    result.sharpe_ratio = sharperatio.iloc[0]
    result.total_return = result.end_balance - result.initial_balance
    result.total_ratio = (result.end_balance - result.initial_balance) / result.initial_balance
    #加权年化
    # result.annul_ratio =  result.total_ratio / result.normal_day * 365
    if result.total_ratio <= -1:
        result.annul_ratio = -1
    else:
        result.annul_ratio =  math.pow(1 + result.total_ratio,365/result.normal_day) - 1

    df_sb = df_new['total'].diff()
    df_sb[0] = 0
    df_sb[df_sb>0] = 1
    df_sb[df_sb<=0] = 0
    result.number_of_profit_days = sum(df_sb)
    result.number_of_loss_days = total_size - result.number_of_profit_days
    df_back = pandas.DataFrame()
    df_back['days'] = total_date
    df_back[code] = total_money
    df_back['val'] =  df_back[code]/df_back[code].iloc[0]
    df_back['drawdown'] = 1 - df['pt']
    # print(df_back)
    return result,df_back

def cal_tradeDetail(vc_tradeDetail):
    # 统计结果
    close_money = []
    result = strategyCalRes()
    for index in range(len(vc_tradeDetail)):
        if vc_tradeDetail[index].side > 0:
            vc_tradeDetail[index].close_profit = (vc_tradeDetail[index].close_price - vc_tradeDetail[index].open_price ) * vc_tradeDetail[index].volume
        if vc_tradeDetail[index].side < 0:
            vc_tradeDetail[index].close_profit = 0 - (vc_tradeDetail[index].close_price - vc_tradeDetail[index].open_price ) * vc_tradeDetail[index].volume
        #总交易笔数
        result.number_of_trades = result.number_of_trades + 1
        #盈利和亏损数统计
        if vc_tradeDetail[index].close_profit > 0:
            #盈利笔数
            result.number_of_profit_trades = result.number_of_profit_trades + 1
            #总盈利额
            result.total_return_profit = result.total_return_profit + vc_tradeDetail[index].close_profit
        else:
            #亏损笔数
            result.number_of_loss_trades = result.number_of_loss_trades + 1
            #总亏损额
            result.total_return_loss = result.total_return_loss + vc_tradeDetail[index].close_profit
        #总盈亏
        result.total_return = result.total_return + vc_tradeDetail[index].close_profit
        #最大单笔盈利
        result.max_profit = max(result.max_profit,vc_tradeDetail[index].close_profit)
        #最大单笔亏损
        result.max_loss = min(result.max_loss,vc_tradeDetail[index].close_profit)
        result.total_commission = result.total_commission + vc_tradeDetail[index].open_commission + vc_tradeDetail[index].close_commission
        if index ==0:
            close_money.append(0.0)
        else:
            close_money.append(result.total_return)
    # print(len(vc_tradeDetail))

    # print("money is :" + str(result.end_balance))
    # print("money is :" + str(result.total_return))
    #单笔平均盈利
    if result.number_of_profit_trades == 0:
        result.avg_profit = 0.0
    else:
        result.avg_profit = result.total_return_profit / result.number_of_profit_trades
    #单笔平均亏损
    if result.number_of_loss_trades == 0:
        result.avg_loss = 0.0
    else:
        result.avg_loss = result.total_return_loss / result.number_of_loss_trades
    #胜率
    if result.number_of_trades == 0:
        result.profit_probability = 0.0
    else:
        result.profit_probability = result.number_of_profit_trades / result.number_of_trades
    #盈亏比
    if result.avg_loss == 0:
        result.profit_loss_ratio = 0.0
    else:
        result.profit_loss_ratio = result.avg_profit / result.avg_loss
    return result,close_money

#输入：日期、价格、持仓表
# 输出：
# 成交明细：all_tradeDetail
# 品种资金：all_vc_money
# 净值序列：df_back
# 统计结果：result
def cal_vc_pos_kl_dataframe(frame_data,frame_pos,ck_plot = False,ck_print = False):
    print("开始回测参数.")
    all_tradeDetail,all_vc_money,df_back,result,df_mm = cal_vc_pos_kl(frame_data,frame_pos)

    df_mm['净值'] = df_back['val'].values
    df_mm['回撤'] = df_back['drawdown'].values
    print(df_mm)
    print(df_back)


    if ck_plot == True:
        # 净值曲线
        fig = plt.figure()
        ax = fig.add_subplot(3,1,1)
        ax1 = fig.add_subplot(3,1,2)
        ax2 = fig.add_subplot(3,1,3)
        ax.plot(df_mm.index.values,df_mm['总权益'].values)
        ax1.plot(df_mm.index.values,df_mm['净值'].values)
        ax2.bar(df_mm.index.values,-df_mm['回撤'].values)
        plt.show()

    if ck_print == True:
        products = frame_pos.columns.values.tolist()
        all_date = frame_data.index.values
        print_strategyCalRes(result)
        for val in products:
            if val != '日期':
                print(val + "    " + str(df_mm[val][len(all_date) - 1]))

    return all_tradeDetail,all_vc_money,df_back,result,df_mm

# 根据数据表和持仓状态表（-1,0,1)得出统计信息：统计手续费以及仓位分配模式:42*244
def cal_vc_pos_kl_dataframe_byStatus(frame_data,frame_pos,ck_plot = False,ck_print = False):
    print("开始回测参数.")
    data_spread = frame_data.diff()
    all_product = frame_pos.columns.values.tolist()
    all_product.remove('日期')
    all_date = frame_data['日期'].values
    total_days = len(all_date)
    total_product = len(all_product)
    print("测试日期有:  " + str(total_days))
    print("测试品种：   "+ str(total_product))
    new_pos = pandas.DataFrame(np.arange(total_days * (total_product + 1)).reshape((total_days,total_product + 1)),columns=frame_pos.columns.values.tolist(),dtype='double')
    new_pos.loc[:][:] = 0
    new_money = pandas.DataFrame(np.arange(total_days * (total_product + 1)).reshape((total_days,total_product + 1)),columns=frame_pos.columns.values.tolist(),dtype='double')
    new_money.loc[:][:] = 0
    DD = (frame_pos == 0).astype(int).sum(axis=1)
    LONG = (frame_pos == 1).astype(int).sum(axis=1)
    SHORT = (frame_pos == -1).astype(int).sum(axis=1)
    TOTAL = LONG + SHORT
    total_money = []
    now_total_money = 0
    for row in range(total_days):
        td_total_money = 0
        if row > 0:
            for vv in range(1,total_product + 1,1):
                #单品种累计的收益率
                new_money.loc[row][vv] = new_money.loc[row - 1][vv] + new_pos.loc[row - 1][vv] * data_spread.loc[row][vv]
                td_total_money = td_total_money + new_money.loc[row][vv]
            # print("abcd  -------:" + str(row) + "  "+ str(frame_data.loc[row][0]) + "    " + str(td_total_money) + "   " + str(now_total_money) + "   " + str(avg_money) + "    " + str(new_pos.loc[row - 1][4] ))
        now_total_money =  td_total_money + glb_initial_money
        total_money.append(now_total_money)
        if row > 0:
            sd = abs(frame_pos.loc[row][1:len(frame_pos.loc[row])] - frame_pos.loc[row-1][1:len(frame_pos.loc[row-1])])
            sd1 = (sd == 0).astype(int).sum(axis=0)
            if sd1 != total_product:
                # 换仓了，进行仓位计算：均分：后面可以按照特殊算法进行仓位分配
                avg_money = now_total_money / TOTAL[row]
                for vv in range(1,total_product + 1,1):
                    new_pos.loc[row][vv] = avg_money / frame_data.loc[row][vv] * frame_pos.loc[row][vv] 
            else:
                #没有换仓，属于持仓，仓位等于昨天
                for vv in range(1,total_product + 1,1):
                    new_pos.loc[row][vv] = new_pos.loc[row - 1][vv]
    frame_pos2 = pandas.DataFrame()
    frame_pos2 = new_pos
    frame_pos2["日期"] = frame_pos["日期"]
    # print(total_money)
    # print(new_pos)
    # print(new_money)
    # print(frame_pos2)
    # pd.DataFrame(new_pos).to_excel("res.xlsx",sheet_name="pos",index=True,header=True)
    # pd.DataFrame(new_money).to_excel("res.xlsx",sheet_name="money",index=True,header=True)
    return cal_vc_pos_kl_dataframe(frame_data,frame_pos2,ck_plot,ck_print)


#data:价格矩阵：第一列为日期yyyy/mm/dd，后面为品种
#pos:仓位列表：第一列为日期yyyy/mm/dd，后面为品种
def cal_vc_pos_kl(data,pos):
    all_tradeDetail = []
    all_result = []
    all_vc_money = []
    all_date = []

    sd = pos.columns.values.tolist()
    all_date = data['日期'].values

    df_mm = pandas.DataFrame()
    df_mm["日期"] = all_date
    df_mm.set_index(["日期"], inplace=True)

    for keys in sd:
        if keys!='日期':
            vc_kl = []
            vc_pos =[]
            #base为品种要素
            base = []
            for row in range(len(data[keys])):
                a = kline()
                a.date = data['日期'].iloc[row]
                a.close = data[keys].iloc[row]
                vc_kl.append(a)
                vc_pos.append(pos[keys].iloc[row])
            #计算交易信息
            base = InsBase()
            vc_tradeDetail,result,vc_money = cal_pos_kl(vc_kl,vc_pos,base)
            result.name = keys
            all_tradeDetail.extend(vc_tradeDetail)
            all_result.append(result)
            all_vc_money.append(vc_money)
            df_mm[keys] = vc_money

    
    df_mm['累计盈亏'] = df_mm.apply(lambda x: x.sum(), axis=1)
    df_mm['总权益'] = df_mm['累计盈亏'] + glb_initial_money

    #总权益
    a = np.array(all_vc_money)
    df = pandas.DataFrame(a)
    df.loc[len(a)] = df.apply(lambda x: x.sum())
    total_money = df.loc[len(a),:]
    print(df.loc[len(a),:])
    total_money = total_money + glb_initial_money
    # 计算资金要素
    res1,df_back = CalMoney(total_money,all_date)
    # 计算交易明细
    res2,close_money = cal_tradeDetail(all_tradeDetail)
    #总交易笔数
    res1.number_of_trades = res2.number_of_trades
    #盈利笔数
    res1.number_of_profit_trades = res2.number_of_profit_trades
    #总盈利额
    res1.total_return_profit = res2.total_return_profit
    #亏损笔数
    res1.number_of_loss_trades = res2.number_of_loss_trades
    #总亏损额
    res1.total_return_loss = res2.total_return_loss
    #总盈亏
    res1.total_return = res2.total_return
    #最大单笔盈利
    res1.max_profit = res2.max_profit
    #最大单笔亏损
    res1.max_loss = res2.max_loss
    res1.total_commission = res2.total_commission
    #单笔平均盈利
    res1.avg_profit = res2.avg_profit
    #单笔平均亏损
    res1.avg_loss = res2.avg_loss
    #胜率
    res1.profit_probability = res2.profit_probability
    #盈亏比
    res1.profit_loss_ratio = res2.profit_loss_ratio
    #打印
    # print_strategyCalRes(res1)
    return all_tradeDetail,all_vc_money,df_back,res1,df_mm

# 根据仓位表 和历史数据，计算出盈亏曲线以及其他统计指标
def cal_pos_kl(vc_kl,vc_pos,base):
    if len(vc_kl) != len(vc_pos) and len(vc_kl) > 0:
        print("参数列表不匹配")
        return
    open_day = ""
    open_price = 0
    side = 0
    # 交易明细
    vc_tradeDetail = []
    # 统计结果
    result = strategyCalRes()
    # 资金曲线
    vc_money = []
    vc_commission = []
    vc_net_money = []
    # 收盘价
    vc_close = []
    # 日期
    vc_now = []
    # 保存最新的累计手续费
    total_comm = 0
    for index in range(len(vc_kl)):
        vc_close.append(float(vc_kl[index].close))
        vc_now.append(vc_kl[index].date)
        if index >0:
            # 昨天有持仓，今天状态和昨天不一样：平仓
            if vc_pos[index - 1] != 0 and vc_pos[index] != vc_pos[index - 1]:
                #平仓
                dd = tradeDetail()
                dd.name = vc_kl[0].name
                dd.close_day = vc_kl[index].date
                dd.close_price = float(vc_kl[index].close)
                dd.open_day = open_day
                dd.open_price = float(open_price)
                dd.side = side
                dd.volume = abs(dd.side)
                dd.open_commission = dd.open_price * dd.volume * base.volumeMulti * base.open_commission
                dd.close_commission = dd.close_price * dd.volume * base.volumeMulti * base.close_commission
                vc_tradeDetail.append(dd)
                total_comm = total_comm + dd.close_price * dd.volume * base.volumeMulti * base.close_commission
            if vc_pos[index] != 0 and vc_pos[index] != vc_pos[index - 1]:
                #开仓
                open_day = vc_kl[index].date
                open_price = vc_kl[index].close
                side = vc_pos[index]
                total_comm = total_comm + open_price * abs(side) * base.volumeMulti * base.open_commission

            # 计算资金
            tdratio = float(vc_kl[index].close) - float(vc_kl[index - 1].close)
            td_value = tdratio * vc_pos[index - 1] + vc_money[index - 1]
            vc_money.append(td_value)
            vc_commission.append(total_comm)

        elif index == 0:
            vc_money.append(0)
            vc_commission.append(0)
        if index == len(vc_kl) - 1:
            #最后一个数据，有持仓 ，平了
            if vc_pos[index] != 0:
                #平仓
                dd = tradeDetail()
                dd.name = vc_kl[0].name
                dd.close_day = vc_kl[index].date
                dd.close_price = float(vc_kl[index].close)
                dd.open_day = open_day
                dd.open_price = float(open_price)
                dd.side = side
                dd.volume = abs(dd.side)
                dd.open_commission = dd.open_price * dd.volume * base.volumeMulti * base.open_commission
                dd.close_commission = dd.close_price * dd.volume * base.volumeMulti * base.close_commission
                vc_tradeDetail.append(dd)
    #统计结果
    result,close_money = cal_tradeDetail(vc_tradeDetail)
    result.start_date = vc_kl[0].date
    result.end_date = vc_kl[len(vc_kl) - 1].date
    # result.normal_day = (result.end_date - result.start_date).days
    result.trade_day = len(vc_kl)
    result.name = vc_kl[0].name
    vc_net_money = [vc_money[i] - vc_commission[i] for i in range(len(vc_money))]

    result.initial_balance = vc_net_money[0]
    result.end_balance = vc_net_money[len(vc_net_money) - 1]
    # print(vc_net_money)
    return vc_tradeDetail,result,vc_net_money

# resample:参数
# # A year
# # M month
# # W week
# # D day
# # H hour
# # T minute
# # S second