# 将获取的股票数据进行实际业务处理

import sys
from decimal import Decimal

from analyze_stock.shanghai_stock_exchange.stock_data_pull import get_deal_day_data, get_stock_data_list
from analyze_stock.shanghai_stock_exchange.utils.date_utils import is_pre_day, date_parse_2_week_day, date_diff

sys.setrecursionlimit(1000000)

# 预定义定投计划数据
stock_auto_invest_plan_list = {
    # 上证
    '000001': {'stock_plan_a': {'name': '每周一，周四定投', 'days': [1,4]},
               'stock_plan_b': {'name': '每周一定投', 'days': [1]},
               'stock_plan_c': {'name': '每周四定投', 'days': [4]},
               'auto_invest_mony': 200
               },
    # 深成
    '399001': {'stock_plan_a': {'name': '每周二定投', 'days': [2]},
               'stock_plan_b': {'name': '每周三定投', 'days': [3]},
               'stock_plan_c': {'name': '每周五定投', 'days': [5]},
               'auto_invest_mony': 200
               },
    # 创业
    '399006': {'stock_plan_a': {}, 'stock_plan_b': {}, 'stock_plan_c': {}}
}


# 获取所有股票的已处理日数据
def get_all_stock_day_data(beg_time=None, end_time=None):
    all_stock_day_data = []
    all_stock_data_list = get_stock_data_list()
    if not all_stock_data_list:
        return all_stock_day_data
    for stock_obj in all_stock_data_list:
        stock_name = stock_obj['f14']
        stock_code = stock_obj['f12']
        stock_day_data = deal_day_data(stock_code, beg_time, end_time)
        all_stock_day_data.append(stock_day_data)

    return all_stock_day_data


# 处理某只股票日k线数据并得出定投计划a的分析数据
# stock_code 股票编码 module 股市交易所 beg_time 查询开始时间 日期字符串 yyyy-MM-dd
def deal_day_data_4_auto_invest_plan_a(stock_code, module=None, beg_time=None, end_time=None):
    stock_plan_data = stock_auto_invest_plan_list[stock_code]
    stock_plan_a_data = stock_plan_data['stock_plan_a']
    auto_invest_mony = stock_plan_data['auto_invest_mony']
    deal_data = get_deal_day_data(stock_code, module, beg_time, end_time)
    # 股票编码
    stock_code = deal_data['data']['code']
    # 股票名称
    stock_name = deal_data['data']['name']
    # 定投计划
    stock_plan = stock_plan_a_data['name']
    # 本次定投预测结果汇总dict
    total_auto_invest_plan_dict = {}
    # 定投总数
    auto_invest_count = 0
    # 完成定投目标数
    auto_invest_ok_count = 0
    # 完成定投目标列表数据
    auto_invest_ok_list = []
    # k线数据
    kLines = deal_data['data']['klines']
    # 总循环次数
    total_loop_count = 0
    for index in range(len(kLines)):
        total_loop_count += 1
        cur_line = kLines[index]
        data_details = cur_line.split(",")
        # 交易时间
        date_str = data_details[0]
        # 当前日期为周几
        week_day = date_parse_2_week_day(date_str)
        if week_day == stock_plan_a_data['days'][0]:
            auto_invest_count += 1
            # 执行定投计划
            cur_auto_invest_plan_result = auto_invest_plan_a(cur_line, index, kLines, 0, 0, round(Decimal(str(auto_invest_mony)) / len(stock_plan_a_data['days']),2),
                                                             stock_plan_a_data['days'])
            if cur_auto_invest_plan_result[0] == 1:
                # 组装当前成功定投结果数据
                cur_ok_auto_invest = {}
                cur_ok_auto_invest['stock_name'] = stock_name
                cur_ok_auto_invest['stock_code'] = stock_code
                cur_ok_auto_invest['stock_plan'] = stock_plan
                cur_ok_auto_invest['start_deal_date'] = date_str
                cur_ok_auto_invest['end_deal_date'] = cur_auto_invest_plan_result[1]
                cur_ok_auto_invest['take_days'] = date_diff(date_str, cur_auto_invest_plan_result[1])
                cur_ok_auto_invest['auto_invest_mony'] = auto_invest_mony
                auto_invest_ok_list.append(cur_ok_auto_invest)
                auto_invest_ok_count += 1
    # 结果集的特殊数据 体现本次定投计划的定投成功数和成功率
    last_line_analyze_data = {}
    last_line_analyze_data['auto_invest_ok_count'] = auto_invest_ok_count
    last_line_analyze_data['auto_invest_count'] = auto_invest_count
    # 获取定投成功率 定投成功数/定投总数
    last_line_analyze_data['auto_invest_ok_rate'] = round(
        Decimal(str(auto_invest_ok_count)) / Decimal(str(auto_invest_count)), 2)
    auto_invest_ok_list.append(last_line_analyze_data)
    total_auto_invest_plan_dict['auto_invest_ok_list'] = auto_invest_ok_list
    total_auto_invest_plan_dict['auto_invest_ok_rate'] = round(Decimal(str(auto_invest_ok_count)) / Decimal(
        str(auto_invest_count)), 2)
    print(total_auto_invest_plan_dict)
    return total_auto_invest_plan_dict


# 处理某只股票日k线数据并得出定投计划b的分析数据
# stock_code 股票编码 module 股市交易所 beg_time 查询开始时间 日期字符串 yyyy-MM-dd
def deal_day_data_4_auto_invest_plan_b(stock_code, module=None, beg_time=None, end_time=None):
    stock_plan_data = stock_auto_invest_plan_list[stock_code]
    stock_plan_b_data = stock_plan_data['stock_plan_b']
    auto_invest_mony = stock_plan_data['auto_invest_mony']
    deal_data = get_deal_day_data(stock_code, module, beg_time, end_time)
    # 股票编码
    stock_code = deal_data['data']['code']
    # 股票名称
    stock_name = deal_data['data']['name']
    # 定投计划
    stock_plan = stock_plan_b_data['name']
    # 本次定投预测结果汇总dict
    total_auto_invest_plan_dict = {}
    # 定投总数
    auto_invest_count = 0
    # 完成定投目标数
    auto_invest_ok_count = 0
    # 完成定投目标列表数据
    auto_invest_ok_list = []
    # k线数据
    kLines = deal_data['data']['klines']
    for index in range(len(kLines)):
        cur_line = kLines[index]
        data_details = cur_line.split(",")
        # 交易时间
        date_str = data_details[0]
        # 当前日期为周几
        week_day = date_parse_2_week_day(date_str)
        if week_day == stock_plan_b_data['days'][0]:
            auto_invest_count += 1
            # 执行定投计划
            cur_auto_invest_plan_result = auto_invest_plan_b(cur_line, index, kLines, 0, 0, auto_invest_mony,
                                                             stock_plan_b_data['days'])
            if cur_auto_invest_plan_result[0] == 1:
                auto_invest_ok_count += 1
                # 组装当前成功定投结果数据
                cur_ok_auto_invest = {}
                cur_ok_auto_invest['stock_name'] = stock_name
                cur_ok_auto_invest['stock_code'] = stock_code
                cur_ok_auto_invest['stock_plan'] = stock_plan
                cur_ok_auto_invest['start_deal_date'] = date_str
                cur_ok_auto_invest['end_deal_date'] = cur_auto_invest_plan_result[1]
                cur_ok_auto_invest['take_days'] = date_diff(date_str, cur_auto_invest_plan_result[1])
                cur_ok_auto_invest['auto_invest_mony'] = auto_invest_mony
                auto_invest_ok_list.append(cur_ok_auto_invest)
    # 结果集的特殊数据 体现本次定投计划的定投成功数和成功率
    last_line_analyze_data = {}
    last_line_analyze_data['auto_invest_ok_count'] = auto_invest_ok_count
    last_line_analyze_data['auto_invest_count'] = auto_invest_count
    last_line_analyze_data['auto_invest_ok_rate'] = round(
        Decimal(str(auto_invest_ok_count)) / Decimal(str(auto_invest_count)), 2)
    auto_invest_ok_list.append(last_line_analyze_data)
    total_auto_invest_plan_dict['auto_invest_ok_list'] = auto_invest_ok_list
    total_auto_invest_plan_dict['auto_invest_ok_rate'] = round(Decimal(str(auto_invest_ok_count)) / Decimal(
        str(auto_invest_count)), 2)
    return total_auto_invest_plan_dict


# 处理某只股票日k线数据并得出定投计划c的分析数据
# stock_code 股票编码 module 股市交易所 beg_time 查询开始时间 日期字符串 yyyy-MM-dd
def deal_day_data_4_auto_invest_plan_c(stock_code, module=None, beg_time=None, end_time=None):
    stock_plan_data = stock_auto_invest_plan_list[stock_code]
    stock_plan_c_data = stock_plan_data['stock_plan_c']
    auto_invest_mony = stock_plan_data['auto_invest_mony']
    deal_data = get_deal_day_data(stock_code, module, beg_time, end_time)
    # 股票编码
    stock_code = deal_data['data']['code']
    # 股票名称
    stock_name = deal_data['data']['name']
    # 定投计划
    stock_plan = stock_plan_c_data['name']
    # 本次定投预测结果汇总dict
    total_auto_invest_plan_dict = {}
    # 定投总数
    auto_invest_count = 0
    # 完成定投目标数
    auto_invest_ok_count = 0
    # 完成定投目标列表数据
    auto_invest_ok_list = []
    # k线数据
    kLines = deal_data['data']['klines']
    for index in range(len(kLines)):
        cur_line = kLines[index]
        data_details = cur_line.split(",")
        # 交易时间
        date_str = data_details[0]
        # 当前日期为周几
        week_day = date_parse_2_week_day(date_str)
        if week_day == stock_plan_c_data['days'][0]:
            auto_invest_count += 1
            # 执行定投计划
            cur_auto_invest_plan_result = auto_invest_plan_c(cur_line, index, kLines, 0, 0, auto_invest_mony,
                                                             stock_plan_c_data['days'])
            if cur_auto_invest_plan_result[0] == 1:
                auto_invest_ok_count += 1
                # 组装当前成功定投结果数据
                cur_ok_auto_invest = {}
                cur_ok_auto_invest['stock_name'] = stock_name
                cur_ok_auto_invest['stock_code'] = stock_code
                cur_ok_auto_invest['stock_plan'] = stock_plan
                cur_ok_auto_invest['start_deal_date'] = date_str
                cur_ok_auto_invest['end_deal_date'] = cur_auto_invest_plan_result[1]
                cur_ok_auto_invest['take_days'] = date_diff(date_str, cur_auto_invest_plan_result[1])
                cur_ok_auto_invest['auto_invest_mony'] = auto_invest_mony
                auto_invest_ok_list.append(cur_ok_auto_invest)
    # 结果集的特殊数据 体现本次定投计划的定投成功数和成功率
    last_line_analyze_data = {}
    last_line_analyze_data['auto_invest_ok_count'] = auto_invest_ok_count
    last_line_analyze_data['auto_invest_count'] = auto_invest_count
    last_line_analyze_data['auto_invest_ok_rate'] = round(
        Decimal(str(auto_invest_ok_count)) / Decimal(str(auto_invest_count)), 2)
    auto_invest_ok_list.append(last_line_analyze_data)
    total_auto_invest_plan_dict['auto_invest_ok_list'] = auto_invest_ok_list
    total_auto_invest_plan_dict['auto_invest_ok_rate'] = round(Decimal(str(auto_invest_ok_count)) / Decimal(
        str(auto_invest_count)), 2)
    return total_auto_invest_plan_dict

# 处理某只股票日k线数据并得出定投计划a的分析数据
# stock_code 股票编码 module 股市交易所 beg_time 查询开始时间 日期字符串 yyyy-MM-dd
def deal_day_data_4_auto_invest_plan_d(stock_code, module=None, beg_time=None, end_time=None):
    stock_plan_data = stock_auto_invest_plan_list[stock_code]
    stock_plan_d_data = stock_plan_data['stock_plan_d']
    auto_invest_mony = stock_plan_data['auto_invest_mony']
    deal_data = get_deal_day_data(stock_code, module, beg_time, end_time)
    # 股票编码
    stock_code = deal_data['data']['code']
    # 股票名称
    stock_name = deal_data['data']['name']
    # 定投计划
    stock_plan = stock_plan_d_data['name']
    # 本次定投预测结果汇总dict
    total_auto_invest_plan_dict = {}
    # 定投总数
    auto_invest_count = 0
    # 完成定投目标数
    auto_invest_ok_count = 0
    # 完成定投目标列表数据
    auto_invest_ok_list = []
    # k线数据
    kLines = deal_data['data']['klines']
    # 总循环次数
    total_loop_count = 0
    for index in range(len(kLines)):
        total_loop_count += 1
        cur_line = kLines[index]
        data_details = cur_line.split(",")
        # 交易时间
        date_str = data_details[0]
        # 当前日期为周几
        week_day = date_parse_2_week_day(date_str)
        if week_day == stock_plan_d_data['days'][0]:
            auto_invest_count += 1
            # 执行定投计划
            cur_auto_invest_plan_result = auto_invest_plan_d(cur_line, index, kLines, 0, 0, auto_invest_mony / 2,
                                                             stock_plan_d_data['days'])
            if cur_auto_invest_plan_result[0] == 1:
                # 组装当前成功定投结果数据
                cur_ok_auto_invest = {}
                cur_ok_auto_invest['stock_name'] = stock_name
                cur_ok_auto_invest['stock_code'] = stock_code
                cur_ok_auto_invest['stock_plan'] = stock_plan
                cur_ok_auto_invest['start_deal_date'] = date_str
                cur_ok_auto_invest['end_deal_date'] = cur_auto_invest_plan_result[1]
                cur_ok_auto_invest['take_days'] = date_diff(date_str, cur_auto_invest_plan_result[1])
                cur_ok_auto_invest['auto_invest_mony'] = auto_invest_mony
                auto_invest_ok_list.append(cur_ok_auto_invest)
                auto_invest_ok_count += 1
    # 结果集的特殊数据 体现本次定投计划的定投成功数和成功率
    last_line_analyze_data = {}
    last_line_analyze_data['auto_invest_ok_count'] = auto_invest_ok_count
    last_line_analyze_data['auto_invest_count'] = auto_invest_count
    # 获取定投成功率 定投成功数/定投总数
    last_line_analyze_data['auto_invest_ok_rate'] = round(
        Decimal(str(auto_invest_ok_count)) / Decimal(str(auto_invest_count)), 2)
    auto_invest_ok_list.append(last_line_analyze_data)
    total_auto_invest_plan_dict['auto_invest_ok_list'] = auto_invest_ok_list
    total_auto_invest_plan_dict['auto_invest_ok_rate'] = round(Decimal(str(auto_invest_ok_count)) / Decimal(
        str(auto_invest_count)), 2)
    print(total_auto_invest_plan_dict)
    return total_auto_invest_plan_dict



# 定投a计划
# cur_line 当前日期数据字符串, cur_index 当前k线列表下标, kLines k线列表数据,
# total_principal 全部本金, total_lot 全部股票份额, auto_invest_mony 定投金额, invest_days 定投日列表
def auto_invest_plan_a(cur_line, cur_index, kLines, total_principal, total_lot, auto_invest_mony, invest_days):
    data_details = cur_line.split(",")
    # 交易时间
    date_str = data_details[0]
    # 当日开盘价
    open_price = data_details[1]
    # 当日收盘价
    close_price = data_details[2]
    # 当日最高价
    highest_price = data_details[3]
    result_list = []
    # 已获利金额 =（已有股票份额 * 当日收盘价）- 已投本金
    # 如果 已投本金 * 0.15 - 已获利金额 <= 0 则定投成功
    cur_profit = round(Decimal(str(total_lot)) * Decimal(close_price), 2) - Decimal(str(total_principal))
    if total_principal != 0 and cur_profit > 0:
        if round(Decimal(str(total_principal)) * Decimal('0.15'), 2) - cur_profit <= 0:
            result_list.append(1)
            result_list.append(date_str)
            return result_list

    if len(kLines) - 1 <= cur_index:
        result_list.append(0)
        result_list.append(date_str)
        return result_list
    week_day = date_parse_2_week_day(date_str)
    # 开始投钱
    if week_day == invest_days[0] or week_day == invest_days[1]:
        # 算出定投金额下的所得份额
        cur_lot = round(Decimal(str(auto_invest_mony)) / Decimal(close_price), 2)
        # 重新计算投资的本金
        total_principal = Decimal(str(total_principal)) + Decimal(str(auto_invest_mony))
        # 重新计算获取的总份额
        total_lot = Decimal(str(total_lot)) + Decimal(str(cur_lot))
    result_list = auto_invest_plan_a(kLines[cur_index + 1], cur_index + 1, kLines, total_principal, total_lot,
                                     auto_invest_mony, invest_days)
    return result_list


# 定投b计划
# cur_line 当前日期数据字符串, cur_index 当前k线列表下标, kLines k线列表数据,
# total_principal 全部本金, total_lot 全部股票份额, auto_invest_mony 定投金额, invest_days 定投日列表
def auto_invest_plan_b(cur_line, cur_index, kLines, total_principal, total_lot, auto_invest_mony, invest_days):
    data_details = cur_line.split(",")
    # 交易时间
    date_str = data_details[0]
    # 当日开盘价
    open_price = data_details[1]
    # 当日收盘价
    close_price = data_details[2]
    cur_profit = round(Decimal(str(total_lot)) * Decimal(close_price), 2) - Decimal(str(total_principal))
    if total_principal != 0 and cur_profit > 0:
        if round(Decimal(str(total_principal)) * Decimal('0.15'), 2) - cur_profit <= 0:
            return (1, date_str)

    if len(kLines) - 1 <= cur_index:
        return (0, date_str)
    week_day = date_parse_2_week_day(date_str)
    # 开始投钱
    if week_day == invest_days[0]:
        # 算出定投金额下的所得份额
        cur_lot = round(Decimal(str(auto_invest_mony)) / Decimal(close_price), 2)
        # 重新计算投资的本金
        total_principal = Decimal(str(total_principal)) + Decimal(str(auto_invest_mony))
        # 重新计算获取的总份额
        total_lot = Decimal(str(total_lot)) + Decimal(str(cur_lot))
    return auto_invest_plan_b(kLines[cur_index + 1], cur_index + 1, kLines, total_principal, total_lot,
                              auto_invest_mony, invest_days)


# 定投c计划
# cur_line 当前日期数据字符串, cur_index 当前k线列表下标, kLines k线列表数据,
# total_principal 全部本金, total_lot 全部股票份额, auto_invest_mony 定投金额, invest_days 定投日列表
def auto_invest_plan_c(cur_line, cur_index, kLines, total_principal, total_lot, auto_invest_mony, invest_days):
    data_details = cur_line.split(",")
    # 交易时间
    date_str = data_details[0]
    # 当日开盘价
    open_price = data_details[1]
    # 当日收盘价
    close_price = data_details[2]
    cur_profit = round(Decimal(str(total_lot)) * Decimal(close_price), 2) - Decimal(str(total_principal))
    if total_principal != 0 and cur_profit > 0:
        if round(Decimal(str(total_principal)) * Decimal('0.15'), 2) - cur_profit <= 0:
            return (1, date_str)

    if len(kLines) - 1 <= cur_index:
        return (0, date_str)
    week_day = date_parse_2_week_day(date_str)
    # 开始投钱
    if week_day == invest_days[0]:
        # 算出定投金额下的所得份额
        cur_lot = round(Decimal(str(auto_invest_mony)) / Decimal(close_price), 2)
        # 重新计算投资的本金
        total_principal = Decimal(str(total_principal)) + Decimal(str(auto_invest_mony))
        # 重新计算获取的总份额
        total_lot = Decimal(str(total_lot)) + Decimal(str(cur_lot))
    return auto_invest_plan_c(kLines[cur_index + 1], cur_index + 1, kLines, total_principal, total_lot,
                              auto_invest_mony, invest_days)


# 定投a计划
# cur_line 当前日期数据字符串, cur_index 当前k线列表下标, kLines k线列表数据,
# total_principal 全部本金, total_lot 全部股票份额, auto_invest_mony 定投金额, invest_days 定投日列表
def auto_invest_plan_d(cur_line, cur_index, kLines, total_principal, total_lot, auto_invest_mony, invest_days):
    data_details = cur_line.split(",")
    # 交易时间
    date_str = data_details[0]
    # 当日开盘价
    open_price = data_details[1]
    # 当日收盘价
    close_price = data_details[2]
    # 当日最高价
    highest_price = data_details[3]
    result_list = []
    # 已获利金额 =（已有股票份额 * 当日收盘价）- 已投本金
    # 如果 已投本金 * 0.15 - 已获利金额 <= 0 则定投成功
    cur_profit = round(Decimal(str(total_lot)) * Decimal(close_price), 2) - Decimal(str(total_principal))
    if total_principal != 0 and cur_profit > 0:
        if round(Decimal(str(total_principal)) * Decimal('0.15'), 2) - cur_profit <= 0:
            result_list.append(1)
            result_list.append(date_str)
            return result_list

    if len(kLines) - 1 <= cur_index:
        result_list.append(0)
        result_list.append(date_str)
        return result_list
    week_day = date_parse_2_week_day(date_str)
    # 开始投钱
    if week_day == invest_days[0] or week_day == invest_days[1] or week_day == invest_days[2]:
        # 算出定投金额下的所得份额
        cur_lot = round(Decimal(str(auto_invest_mony)) / Decimal(close_price), 2)
        # 重新计算投资的本金
        total_principal = Decimal(str(total_principal)) + Decimal(str(auto_invest_mony))
        # 重新计算获取的总份额
        total_lot = Decimal(str(total_lot)) + Decimal(str(cur_lot))
    result_list = auto_invest_plan_d(kLines[cur_index + 1], cur_index + 1, kLines, total_principal, total_lot,
                                     auto_invest_mony, invest_days)
    return result_list



# 处理某只股票日k线数据并得出以周为单位某天的股票数据
# beg_time 查询开始时间 日期字符串 yyyy-MM-dd
def deal_day_data(stock_code, module=None, beg_time=None, end_time=None):
    deal_data = get_deal_day_data(stock_code, module, beg_time, end_time)
    # 股票编码
    stock_code = deal_data['data']['code']
    # 股票名称
    stock_name = deal_data['data']['name']
    # k线数据
    kLines = deal_data['data']['klines']
    # 初始化以一周为单位的结构体数据
    week_day_dict = init_week_day_dict(stock_code, stock_name)
    # 设置前一天的收盘价格
    pre_close_price = None
    for currentLine in kLines:
        data_details = currentLine.split(",")
        # 交易时间
        date_str = data_details[0]
        # 当日开盘价
        open_price = data_details[1]
        # 当日收盘价
        close_price = data_details[2]
        # 如果预期结果的前一天有交易信息,进行前一天收盘价格的设置
        if beg_time is not None and is_pre_day(date_str, beg_time):
            pre_close_price = close_price
            continue
        # week_day 前缀
        week_day_pre = 'week_day_'
        # 当前日期是周几
        week_day = date_parse_2_week_day(date_str)
        # 获取字典中对应的week_day对象
        week_day_obj = week_day_dict[week_day_pre + str(week_day)]

        if pre_close_price is None:
            if Decimal(close_price) - Decimal(open_price) >= 0:
                week_day_obj['up_times'] += 1
                cur_up_range = Decimal(close_price) - Decimal(open_price)
                cur_total_up_range = Decimal(week_day_obj['total_up_range']) + cur_up_range
                week_day_obj['total_up_range'] = str(cur_total_up_range)

            else:
                week_day_obj['down_times'] += 1
                cur_down_range = Decimal(open_price) - Decimal(close_price)
                cur_total_down_range = Decimal(week_day_obj['total_down_range']) + cur_down_range
                week_day_obj['total_down_range'] = str(cur_total_down_range)
        else:
            if Decimal(close_price) - Decimal(pre_close_price) >= 0:
                week_day_obj['up_times'] += 1
                cur_up_range = Decimal(close_price) - Decimal(pre_close_price)
                cur_total_up_range = Decimal(week_day_obj['total_up_range']) + cur_up_range
                week_day_obj['total_up_range'] = str(cur_total_up_range)
            else:
                week_day_obj['down_times'] += 1
                cur_down_range = Decimal(pre_close_price) - Decimal(close_price)
                cur_total_down_range = Decimal(week_day_obj['total_down_range']) + cur_down_range
                week_day_obj['total_down_range'] = str(cur_total_down_range)
    print(week_day_dict)
    return week_day_dict


# 初始化周数据字典
# 返回值 字典(元祖)
def init_week_day_dict(stock_code, stock_name):
    week_day_dict = {}
    # 循环设置从周一到周日的week_day_obj
    for i in range(7):
        week_day_obj = {}
        week_day_obj['week_day'] = i + 1
        week_day_obj['down_times'] = 0
        week_day_obj['total_down_range'] = 0
        week_day_obj['up_times'] = 0
        week_day_obj['total_up_range'] = '0.0'
        week_day_dict["week_day_" + str(i + 1)] = week_day_obj

    # 设置初始化周数据字典值的股票编码和股票名称数据
    week_day_dict['stock_code'] = stock_code
    week_day_dict['stock_name'] = stock_name

    return week_day_dict

# deal_day_data('399001', 'SC')
# deal_day_data_4_auto_invest_plan_b('000001')



