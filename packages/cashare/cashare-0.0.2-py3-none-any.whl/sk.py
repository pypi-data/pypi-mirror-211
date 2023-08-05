import httpx
from dname import url1,url2
import datetime

def daily(sk_code,start_date='19910101',end_date=str(datetime.date.today().strftime('%Y%m%d'))):
    # lll=url2+'/stock/weekly/'+sk_code+'/'+start_date+'/'+end_date
    lll='http://localhost:8010/us/stock/history/000001.sz/2022-02-03/2023-03-04'
    print(lll)
    r = httpx.get(lll)
    print(r)



    import pandas as pd
    ls=pd.DataFrame(r.json())
    print(ls)
    return ls

if __name__ == '__main__':
    daily('000001.sz',end_date=str(20221223))