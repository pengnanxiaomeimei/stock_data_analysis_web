import re
import time

import requests

from analyze_stock.shanghai_stock_exchange.stock_config_data import StockTradeConfigData

from analyze_stock.shanghai_stock_exchange.utils.date_utils import date_add


# 获取某只股票待处理的日k线数据
# stock_code 股票编码 beg_time 查询开始时间字符串 格式 yyyy-MM-dd module 所在交易所 默认 上证
def get_deal_day_data(stock_code, module=None, beg_time=None, end_time=None):
    # 获取当前时间的时间戳
    t = time.time()
    time_stamp = int(round(t * 1000))

    # 获取目标url
    get_quotation_data_api = StockTradeConfigData.day_url

    # 拼接查询参数
    str_parameter = '?cb=' + StockTradeConfigData.cb_str_pre + str(time_stamp)
    str_parameter += '&secid=' + ('0.' if module is not None and module.find('SZ') < 0 else StockTradeConfigData.secid_str_pre) + stock_code
    str_parameter += '&ut=' + StockTradeConfigData.ut
    str_parameter += '&fields1=' + StockTradeConfigData.fields1
    str_parameter += '&fields2=' + StockTradeConfigData.fields2
    str_parameter += '&klt=' + StockTradeConfigData.klt
    str_parameter += '&fqt=' + StockTradeConfigData.fqt
    str_parameter += '&beg=' + (date_add(beg_time, -15, '%Y%m%d') if beg_time is not None else StockTradeConfigData.beg)
    str_parameter += '&end=' + (end_time if end_time is not None else StockTradeConfigData.end)
    str_parameter += '&_=' + str(time_stamp)

    # 组装最终的url
    get_quotation_data_api_url = get_quotation_data_api + str_parameter

    # 发起请求
    r = requests.get(get_quotation_data_api_url)
    p2 = re.compile(r'[(](.*)[)]', re.S)

    result = re.findall(p2, r.content.decode('utf-8'))[0]

    mes_dict = eval(result)

    return mes_dict


# 查询某页股票列表数据
def get_stock_data_list_by_page(page_index):
    # 获取完整的目标url
    get_quotation_data_api_url = get_stock_data_list_target_request(page_index)
    # 发起请求
    r = requests.get(get_quotation_data_api_url)
    p2 = re.compile(r'[(](.*)[)]', re.S)

    result = re.findall(p2, r.content.decode('utf-8'))[0]

    mes_dict = eval(result)

    return mes_dict


# 组装股票列表数据查询请求
def get_stock_data_list_target_request(page_index):
    # 列表查询相关请求参数
    stock_data_list_url = 'http://76.push2.eastmoney.com/api/qt/clist/get'
    # cb参数前缀 拼接时间戳
    cb_param_pre = 'jQuery112406497239864696334_'
    # 每页条数
    pz = '100'
    # 查询参数 po
    po = '1'
    # 查询参数 np
    np = '1'
    # 查询参数 ut
    ut = 'bd1d9ddb04089700cf9c27f6f7426281'
    # 查询参数fltt
    fltt = '2'
    # 查询参数 invt
    invt = '2'
    # 查询参数 fid
    fid = 'f3'
    # 查询参数 fileds
    fileds = 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152'
    # 查询参数 fs
    fs = 'm:1+s:2'

    # 获取当前时间的时间戳
    t = time.time()
    time_stamp = int(round(t * 1000))

    # 获取目标url
    get_quotation_data_api = stock_data_list_url

    # 拼接查询参数
    str_parameter = '?cb=' + cb_param_pre + str(time_stamp)
    str_parameter += '&pn=' + str(page_index)
    str_parameter += '&pz=' + pz
    str_parameter += '&po=' + po
    str_parameter += '&np=' + np
    str_parameter += '&ut=' + ut
    str_parameter += '&fltt=' + fltt
    str_parameter += '&invt=' + invt
    str_parameter += '&fid=' + fid
    str_parameter += '&fields' + fileds
    str_parameter += '&fs' + fs
    str_parameter += '&_=' + str(time_stamp)

    # 组装最终的url
    get_quotation_data_api_url = get_quotation_data_api + str_parameter
    return get_quotation_data_api_url


# 获取所有股票的名称及编码数据集
def get_stock_data_list():
    stock_history_data_list = []
    page_index = 1
    while True:
        stock_page_data = get_stock_data_list_by_page(page_index)
        stock_page_data_dict = stock_page_data['data']
        if not stock_page_data_dict:
            break
        stock_page_data_list = stock_page_data_dict['diff']
        for stock_obj in stock_page_data_list:
            stock_history_data_list.append(stock_obj)
    return stock_history_data_list


# 根据股票名称，拼音，简拼 获取股票编码信息
def query_stock_by_name(name):
    query_request = get_query_stock_by_name_request(name)
    # 发起请求
    r = requests.get(query_request)
    p2 = re.compile(r'[(](.*)[)]', re.S)

    result = re.findall(p2, r.content.decode('utf-8'))[0]

    mes_dict = eval(result)

    query_result = mes_dict['QuotationCodeTable']['Data']

    return query_result


# 获取根据股票名称查询股票编码的完整请求
def get_query_stock_by_name_request(name):
    # 目标查询url
    query_url = 'http://searchapi.eastmoney.com/api/suggest/get'
    # cb查询参数前缀
    cb_param_pre = 'jQuery112406497239864696334_'
    # 股票名称查询条件
    input = name
    # 查询类型
    type = '14'
    # 验证信息
    token = 'D43BF722C8E33BDC906FB84D85E326E8'
    # 预期获取结果数
    count = '5'

    # 获取当前时间的时间戳
    t = time.time()
    time_stamp = int(round(t * 1000))

    # 获取目标url
    get_quotation_data_api = query_url

    # 拼接查询参数
    str_parameter = '?cb=' + cb_param_pre + str(time_stamp)
    str_parameter += '&input=' + name
    str_parameter += '&type=' + type
    str_parameter += '&token=' + token
    str_parameter += '&count=' + count
    str_parameter += '&_=' + str(time_stamp)

    # 组装最终的url
    get_quotation_data_api_url = get_quotation_data_api + str_parameter
    return get_quotation_data_api_url


# get_deal_day_data('000126', "20190901")
# date_parse("2020-08-27", None)
# date_add("20200810", -5)
# deal_day_data('000126', '20190807')
# init_week_day_dict('000126', '消费50')
# query_stock_by_name('消费')
