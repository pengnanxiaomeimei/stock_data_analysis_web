from django.shortcuts import render

from django.shortcuts import HttpResponse

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

import json

from analyze_stock.shanghai_stock_exchange.stock_data_deal import get_history_one_day_deal_data_by_stock_code_and_date
from analyze_stock.shanghai_stock_exchange.stock_data_pull import query_stock_by_name

from analyze_stock.shanghai_stock_exchange.utils.json_util import JsonEncoder

user_list = []


@csrf_exempt
def index(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        temp = {'user': username, 'pwd': password}
        user_list.append(temp)
    # 将用户数据列表作为上下文参数提供render渲染index页面
    # return render(request, 'index.html', {'data': user_list})
    return HttpResponse(json.dumps({'data': user_list}))
    # return render(request, 'index.html')


# 获取某天某股票在历史上的今天的整体上涨和下跌概率
# stock_code 股票编码
# date 日期 yyyy-MM-dd
@csrf_exempt
def get_history_one_day_deal_data(request):
    if not request.method == 'POST':
        return HttpResponse(json.dumps({'data': None, 'code': 400, 'msg': 'bad request method'}))
    stock_code = request.POST.get('stock_code')
    date = request.POST.get('date')
    moudle = request.POST.get('moudle')
    deal_data = get_history_one_day_deal_data_by_stock_code_and_date(stock_code, date, moudle)
    return HttpResponse(json.dumps({'data': deal_data, 'code': 200}, cls=JsonEncoder))
    # return render(request, 'index.html')


# 通过关键词获取相应的股票名称、编码等主要数据
# stock_code 股票编码
# date 日期 yyyy-MM-dd
@csrf_exempt
def get_stock_by_keyword(request):
    if not request.method == 'GET':
        return HttpResponse(json.dumps({'data': None, 'code': 400, 'msg': 'bad request method'}))
    keyword = request.GET.get('keyword')
    deal_data = None
    if keyword is not None and len(keyword) != 0 and keyword.isspace() == False:
        deal_data = query_stock_by_name(keyword)
    print(deal_data)
    return HttpResponse(json.dumps({'data': deal_data, 'code': 200}, cls=JsonEncoder))
    # return render(request, 'index.html')
