# import pandas as pd
# import httpx
# import datetime
#
# # df=pd.DataFrame(data=None)
# # # df3 = pd.DataFrame({'id':[3,4],'age':[30,40]})
# # for i in range(4):
# #     r = httpx.get("https://financialmodelingprep.com/api/v3/historical-chart/1hour/aapl?from=2019-11-11&to=2020-01-29&apikey=d27af5809bd7c7ead4fbe7241f0da792")
# #     ls = pd.DataFrame(r.json())
# #     # print(ls)
# #     df=df.append([ls],ignore_index=True)
# #     print(df)
#
# # #
# # import pandas as pd
# #
# # idnumber = [1,2,5]
# # fname = ['Kate','John','Eli']
# # age = [10,20,50]
# # grade = ['A','B','C']
# #
# # df1 = pd.DataFrame(data=None)
# # df2 = pd.DataFrame({'age':age,'grade':grade})
# # df3 = pd.DataFrame({'id':[3,4],'age':[30,40]})
# # print("df1:\n{}".format(df1))
# # print("df2:\n{}".format(df2))
# # print("df3:\n{}".format(df3))
# #
# # df1_append_df2 = df1.append(df2)
# # print("df1_append_df2:\n{}".format(df1_append_df2))
# #
# # df1_append_df2_df3 = df1.append([df2,df3], ignore_index = True)
# # print("df1_append_df2_df3:\n{}".format(df1_append_df2_df3))
# # r = httpx.get("https://financialmodelingprep.com/api/v3/historical-chart/1hour/aapl?from=2019-11-11&to=2020-01-29&apikey=d27af5809bd7c7ead4fbe7241f0da792")
# # ls = pd.DataFrame(r.json())
# # print(ls.append(df3))
#
# lll='2012-05-31'
# wwww='2012-05-18'
#
# d1 = datetime.datetime.strptime(lll,'%Y-%m-%d')
# d2 = datetime.datetime.strptime(wwww,'%Y-%m-%d')
# delta = d1 - d2
# print(delta.days)
import tushare as ts
import numpy as np
import pandas as pd
from scipy import stats

# 获取股票数据
df = ts.get_hist_data('000001', start='2020-01-01', end='2020-12-31')
df.index = pd.to_datetime(df.index)

# 下载无风险收益率数据
rf = ts.get_k_data('sh000001', start='2020-01-01', end='2020-12-31')
rf.index = pd.to_datetime(rf['date'])
rf = rf[['close']]
rf = (1 + (rf / 100)).resample('M').prod() - 1
rf.index = rf.index.strftime('%Y-%m')

# 计算收益率
df['return'] = df['close'].pct_change()
df = df.dropna()

# 计算市场收益率
market = df['return'] - rf['close']

# 计算SMB和HML
size = np.log(df['volume'])
size = pd.qcut(size, 5, labels=False) + 1
value = pd.DataFrame()
value['pb_ratio'] = df['pb_ratio']
value['pe_ratio'] = df['pe_ratio']
value = (value - value.mean()) / value.std()
value = value['pb_ratio'] - value['pe_ratio']
value = pd.qcut(value, 5, labels=False) + 1
smb = df.groupby([size, value])['return'].mean()
smb.index.names = ['size', 'value']
smb = smb.unstack()
smb = smb.iloc[:, -1] - smb.iloc[:, 0]

hml = df.groupby([size, value])['return'].mean()
hml.index.names = ['size', 'value']
hml = hml.unstack()
hml = (hml.iloc[:, 0] + hml.iloc[:, -1]) / 2 - smb

# 计算市场因子收益率、SMB和HML因子收益率
X = pd.DataFrame()
X['market'] = market
X['smb'] = smb
X['hml'] = hml
X = X.dropna()

# 计算CAPM系数、SMB系数、HML系数
results = []
for column in X.columns:
    slope, intercept, r_value, p_value, std_err = stats.linregress(X[column], df['return'] - rf['close'])
    results.append(slope)

# 输出结果
print('CAPM系数: ', results[0])
print('SMB系数: ', results[1])
print('HML系数: ', results[2])