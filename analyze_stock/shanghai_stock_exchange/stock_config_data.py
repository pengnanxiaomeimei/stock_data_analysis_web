# encoding=utf8


class StockTradeConfigData:
    # 股票code
    stock_code = None
    # 股票市场
    stock_market = 'SHANG_ZHENG'
    # 股票名称
    sotck_name = None
    # cb查询参数前缀 拼接 当前时间戳 毫秒值
    cb_str_pre = 'jQuery112402130161940877767_'
    # fileds1
    fields1 = 'f1,f2,f3,f4,f5'
    # fileds2
    fields2 = 'f51,f52,f53,f54,f55,f56,f57,f58'
    # secid 拼接 股票编码
    secid_str_pre = '1.'
    # ut
    ut = 'fa5fd1943c7b386f172d6893dbfba10b'
    # klt
    klt = '101'
    # fqt
    fqt = '0'
    # beg 查询区间开始时间 yyyyMMdd
    beg = '19900101'
    # end 查询区间结束时间 yyyyMMdd
    end = '20500000'
    # 日k线数据url
    day_url = 'http://push2his.eastmoney.com/api/qt/stock/kline/get'
