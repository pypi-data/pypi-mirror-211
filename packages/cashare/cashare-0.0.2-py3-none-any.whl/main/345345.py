import pandas as pd
import httpx
import datetime

# df=pd.DataFrame(data=None)
# # df3 = pd.DataFrame({'id':[3,4],'age':[30,40]})
# for i in range(4):
#     r = httpx.get("https://financialmodelingprep.com/api/v3/historical-chart/1hour/aapl?from=2019-11-11&to=2020-01-29&apikey=d27af5809bd7c7ead4fbe7241f0da792")
#     ls = pd.DataFrame(r.json())
#     # print(ls)
#     df=df.append([ls],ignore_index=True)
#     print(df)

# #
# import pandas as pd
#
# idnumber = [1,2,5]
# fname = ['Kate','John','Eli']
# age = [10,20,50]
# grade = ['A','B','C']
#
# df1 = pd.DataFrame(data=None)
# df2 = pd.DataFrame({'age':age,'grade':grade})
# df3 = pd.DataFrame({'id':[3,4],'age':[30,40]})
# print("df1:\n{}".format(df1))
# print("df2:\n{}".format(df2))
# print("df3:\n{}".format(df3))
#
# df1_append_df2 = df1.append(df2)
# print("df1_append_df2:\n{}".format(df1_append_df2))
#
# df1_append_df2_df3 = df1.append([df2,df3], ignore_index = True)
# print("df1_append_df2_df3:\n{}".format(df1_append_df2_df3))
# r = httpx.get("https://financialmodelingprep.com/api/v3/historical-chart/1hour/aapl?from=2019-11-11&to=2020-01-29&apikey=d27af5809bd7c7ead4fbe7241f0da792")
# ls = pd.DataFrame(r.json())
# print(ls.append(df3))

lll='2012-05-31'
wwww='2012-05-18'

d1 = datetime.datetime.strptime(lll,'%Y-%m-%d')
d2 = datetime.datetime.strptime(wwww,'%Y-%m-%d')
delta = d1 - d2
print(delta.days)
