import pandas as pd
import sys
import xlwt

from analyze_stock.shanghai_stock_exchange.stock_data_deal import deal_day_data, get_all_stock_day_data, \
    deal_day_data_4_auto_invest_plan

sys.setrecursionlimit(5000000)

# 预定义定投计划数据
stock_auto_invest_plan_list = {
    # 上证
    '000001': {'stock_plan_a': {'name': '每周一定投', 'days': [1]},
               'stock_plan_b': {'name': '每周四定投', 'days': [4]},
               'stock_plan_c': {'name': '每周一，周四定投', 'days': [1, 4]},
               'stock_plan_d': {'name': '每周二定投', 'days': [2]},
               'stock_plan_e': {'name': '每周三定投', 'days': [3]},
               'stock_plan_f': {'name': '每周五定投', 'days': [5]},
               'auto_invest_mony': 200,
               'stock_plan_name_container': ['stock_plan_a', 'stock_plan_b', 'stock_plan_c', 'stock_plan_d',
                                             'stock_plan_e', 'stock_plan_f']
               },
    # 深成
    '399001': {'stock_plan_a': {'name': '每周一，周四定投', 'days': [1, 4]},
               'stock_plan_b': {'name': '每周一定投', 'days': [1]},
               'stock_plan_c': {'name': '每周四定投', 'days': [4]},
               'stock_plan_d': {'name': '每周二，周三，周五定投', 'days': [2, 3, 5]},
               'auto_invest_mony': 200,
               'stock_plan_name_container': ['stock_plan_a', 'stock_plan_b', 'stock_plan_c']
               },
    # 创业
    '399006': {'stock_plan_a': {}, 'stock_plan_b': {}, 'stock_plan_c': {}}
}


# 定投计划分析数据excel导出
# stock_code_list [{'code': '000001', 'name':'上证指数', 'module': 'SZ'}]
def export_auto_invest_plan_analyze_data_with_sheet(stock_code_list):
    for stock_code in stock_code_list:
        total_auto_invest_plan_list = []
        print(stock_auto_invest_plan_list)
        stock_plan_dict = stock_auto_invest_plan_list[stock_code['code']]
        stock_plan_name_list = stock_plan_dict['stock_plan_name_container']
        for plan_name in stock_plan_name_list:
            cur_total_auto_invest_plan_dict = {}

            cur_total_auto_invest_plan_dict = deal_day_data_4_auto_invest_plan(plan_name, stock_auto_invest_plan_list,
                                                                               stock_code['code'],
                                                                               stock_code['module'])

            cur_total_auto_invest_plan_list = cur_total_auto_invest_plan_dict['auto_invest_ok_list']
            if cur_total_auto_invest_plan_list is not None:
                sheet_dict = {}
                sheet_dict['sheet_name'] = stock_plan_dict[plan_name]['name']
                sheet_dict['sheet_data'] = cur_total_auto_invest_plan_list
                total_auto_invest_plan_list.append(sheet_dict)
        # 整理数据格式准备导出
        export_excel_4_auto_invest_plan_data_with_sheet(total_auto_invest_plan_list, stock_code['name'])

        # 定投计划分析数据excel导出

# stock_code_list [{'code': '000001', 'name':'上证指数', 'module': 'SZ'}]
def export_auto_invest_plan_analyze_data(stock_code_list):

    for stock_code in stock_code_list:
        total_auto_invest_plan_list = []
        print(stock_auto_invest_plan_list)
        stock_plan_dict = stock_auto_invest_plan_list[stock_code['code']]
        stock_plan_name_list = stock_plan_dict['stock_plan_name_container']
        for plan_name in stock_plan_name_list:
            cur_total_auto_invest_plan_dict = {}

            cur_total_auto_invest_plan_dict = deal_day_data_4_auto_invest_plan(plan_name,
                                                                               stock_auto_invest_plan_list,
                                                                               stock_code['code'],
                                                                               stock_code['module'])

            cur_total_auto_invest_plan_list = cur_total_auto_invest_plan_dict['auto_invest_ok_list']
            if cur_total_auto_invest_plan_list is not None:
                total_auto_invest_plan_list.extend(cur_total_auto_invest_plan_list)
        # 整理数据格式准备导出
        export_excel_4_auto_invest_plan_data(total_auto_invest_plan_list, stock_code['name'])


# 股票历史涨跌数据excel导出
def export_stock_data(stock_code_list=None):
    # beg_time = date_add_for_year(None, -5, '%Y-%m-%d')
    week_day_list = []
    if stock_code_list is None:
        stock_data_list = get_all_stock_day_data(None)
        if stock_data_list is None:
            return
        for week_day_dict in stock_data_list:
            week_day_list_sub = dispose_one_stock_week_day_obj(week_day_dict)
            if week_day_list_sub is None:
                continue
            week_day_list.extend(week_day_list_sub)
        return
    for stock_code in stock_code_list:
        week_day_dict = deal_day_data(stock_code['code'], stock_code['module'])
        week_day_list_sub = dispose_one_stock_week_day_obj(week_day_dict)
        if week_day_list_sub is None:
            continue
        week_day_list.extend(week_day_list_sub)
    export_excel(week_day_list)


# 通过网络请求获取的单个week_day_dict组装week_day_list
def dispose_one_stock_week_day_obj(week_day_dict):
    week_day_list = []
    for i in range(7):
        week_day_obj = week_day_dict['week_day_' + str(i + 1)]
        if week_day_obj is None:
            continue
        week_day_obj['stock_code'] = week_day_dict['stock_code']
        week_day_obj['stock_name'] = week_day_dict['stock_name']
        week_day_list.append(week_day_obj)

    return week_day_list


def export_excel(export):
    # 将字典列表转换为DataFrame
    pf = pd.DataFrame(list(export))
    # 指定字段顺序
    order = ['stock_code', 'stock_name', 'week_day', 'up_times', 'total_up_range', 'down_times', 'total_down_range']
    pf = pf[order]
    # 将列名替换为中文
    columns_map = {
        'stock_name': '股票名称',
        'stock_code': '股票编号',
        'week_day': '周几',
        'up_times': '上涨次数',
        'total_up_range': '累计上涨幅度',
        'down_times': '下跌次数',
        'total_down_range': '累计下跌幅度'
    }
    pf.rename(columns=columns_map, inplace=True)
    # 指定生成的Excel表格名称
    file_path = pd.ExcelWriter('stock_data_export_01_.xlsx')
    # 替换空单元格
    pf.fillna(' ', inplace=True)
    # 输出
    pf.to_excel(file_path, encoding='utf-8', index=False)
    # 保存表格
    file_path.save()


def export_excel_4_auto_invest_plan_data(export, file_name_suffix):
    if export is None:
        return
    # 将字典列表转换为DataFrame
    pf = pd.DataFrame(list(export))
    # 指定字段顺序
    order = ['stock_name', 'stock_code', 'stock_plan', 'start_deal_date', 'end_deal_date', 'take_days',
             'auto_invest_ok_count', 'auto_invest_count', 'auto_invest_ok_rate']
    pf = pf[order]
    # 将列名替换为中文
    columns_map = {
        'stock_name': '股票名称',
        'stock_code': '股票编号',
        'stock_plan': '定投计划',
        'start_deal_date': '开始交易时间',
        'end_deal_date': '结束交易时间',
        'take_days': '持续天数',
        'auto_invest_ok_count': '定投成功次数',
        'auto_invest_count': '定投总数',
        'auto_invest_ok_rate': '定投成功比率'
    }
    pf.rename(columns=columns_map, inplace=True)
    # 指定生成的Excel表格名称
    file_path = pd.ExcelWriter('stock_auto_invest_data_export' + file_name_suffix + '.xlsx')
    # 替换空单元格
    pf.fillna(' ', inplace=True)
    # 输出
    pf.to_excel(file_path, encoding='utf-8', index=False)
    # 保存表格
    file_path.save()

# 将列名替换为中文
first_columns_map = {
    'stock_name': '股票名称',
    'stock_code': '股票编号',
    'stock_plan': '定投计划',
    'start_deal_date': '开始交易时间',
    'end_deal_date': '结束交易时间',
    'take_days': '持续天数',
    'auto_invest_ok_count': '定投成功次数',
    'auto_invest_count': '定投总数',
    'auto_invest_ok_rate': '定投成功比率'
}

def export_excel_4_auto_invest_plan_data_with_sheet(export, file_name_suffix):
    if export is None:
        return

    w = xlwt.Workbook()
    for sheet_data in export:
        sheet_data_list = sheet_data['sheet_data']
        sheet = w.add_sheet(sheet_data['sheet_name'], cell_overwrite_ok=True)
        # 首行内容
        col = 0
        for first_col in first_columns_map:
            sheet.write(0,col,first_columns_map[first_col])
            col += 1

        # sheet页具体数据内容
        row = 1
        for sheet_data_one in sheet_data_list:
            data_col = 0
            # 当前行数据填充
            for first_col in first_columns_map:
                if first_col in sheet_data_one:
                    sheet.write(row, data_col, sheet_data_one[first_col])
                data_col += 1
            row += 1

    w.save('test_stock_analyze_data_001.xls')


# 将分析完成的列表导出为excel表格
export_stock_data(
    [{'code': '000001', 'module': 'SZ'}])
# , {'code': '399001', 'module': 'SC'}, {'code': '399006', 'module': 'CY'}


# w = xlwt.Workbook()
# sheet = w.add_sheet('Sheet--01', cell_overwrite_ok=True)
# sheet.write(0, 0, 1)
# sheet.write(0, 1, 2)
# sheet.write(0, 2, 3)
# sheet.write(1, 0, 1)
# sheet.write(2, 0, 1)
# sheet.write(3, 0, 1)
# w.save('a.xls')

# for entry_set in first_columns_map:
#     print(first_columns_map[entry_set])

# 将分析完成的定投数据列表导出为excel表格
# export_auto_invest_plan_analyze_data_with_sheet(
#     [{'code': '000001', 'name':'上证指数', 'module': 'SZ'}])

# , {'code': '399001', 'name':'深证成指', 'module': 'SC'}


# total_auto_invest_plan_list = []
# sheet_dict = {}
# sheet_dict['sheet_name'] = "test_plan_name"
# sheet_dict['sheet_data'] = ['a','b','c']
# if 'sheet_name' in sheet_dict:
#     print(sheet_dict['sheet_name'])
# total_auto_invest_plan_list.append(sheet_dict)
# export_excel_4_auto_invest_plan_data_with_sheet(total_auto_invest_plan_list,'_a_b')
