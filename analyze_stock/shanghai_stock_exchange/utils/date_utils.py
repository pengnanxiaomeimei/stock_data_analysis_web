# 日期工具

# current_dtstr  当前kline时间字符串-> yyyy-MM-dd beg_time 查询开始时间字符串-> yyyyMMdd
import datetime


# 当前日期是否在目标日期之前
# 参数为字符串类型 格式 yyyy-MM-dd
# 返回值boolean true 当前日期在目标日期前
def is_pre_day(current_dtstr, target_dtstr):
    current_date = datetime.datetime.strptime(current_dtstr, "%Y-%m-%d")
    beg_date = datetime.datetime.strptime(target_dtstr, "%Y-%m-%d")
    return (beg_date - current_date).days > 0


# 根据时间字符串获取传入的日期是周几
# dtstr 日期字符串
def date_parse_2_week_day(dtstr):
    dateformat = "%Y-%m-%d"
    d = datetime.datetime.strptime(dtstr, dateformat).date()
    print(d.isoweekday())
    if d.isoweekday() == 6 or d.isoweekday() == 7:
        print(dtstr)
    return d.isoweekday()


# 根据传入的日期字符串和目标差异天数获取最终日期字符串
# dtstr 日期字符串 yyyy-MM-dd
# add_day 整数 可为负数
# 返回值 日期字符串 格式默认 yyyy-MM-dd 如果dateformat有值，以dateformate为主
def date_add(dtstr, add_day, dateformat):
    dateformat = dateformat if dateformat is not None else "%Y-%m-%d"
    time = datetime.datetime.strptime(dtstr, "%Y-%m-%d")
    if add_day < 0:
        add_day = - add_day
        time = time - datetime.timedelta(days=add_day)
    else:
        time = time + datetime.timedelta(days=add_day)

    print(type(time))
    print(datetime.datetime.strftime(time, dateformat))

    return datetime.datetime.strftime(time, dateformat)


# 获取传入的日期字符串差异天数
# dtstr1,2 日期字符串 yyyy-MM-dd
# add_day 整数 可为负数
# 返回值 相差天数
def date_diff(dtstr1, dtstr2):
    dateformat = "%Y-%m-%d"
    time1 = datetime.datetime.strptime(dtstr1, dateformat)
    time2 = datetime.datetime.strptime(dtstr2, dateformat)
    diff_days = (time2 - time1).days
    print(diff_days)
    if diff_days < 0:
        return - diff_days
    return diff_days


# 根据传入的日期字符串和目标差异年数获取最终日期字符串
# dtstr 日期字符串 yyyy-MM-dd
# add_year 整数 可为负数
# 返回值 日期字符串 格式默认 yyyy-MM-dd 如果dateformat有值，以dateformate为主
def date_add_for_year(dtstr, add_year, dateformat):
    dateformat = dateformat if dateformat is not None else "%Y-%m-%d"
    time = datetime.datetime.now() if dtstr is None else datetime.datetime.strptime(dtstr, dateformat)
    last_year = int(time.year) + add_year
    last_month = datetime.datetime.strftime(time, "%m")
    last_day = datetime.datetime.strftime(time, "%d")

    result_time = '{}-{}-{}'.format(last_year, last_month, last_day) if dateformat.find("-") > 0 else '{}{}{}'.format(last_year, last_month, last_day)



    print(result_time)

    return result_time


# 历史上的某天
# 日期格式 yyyy-MM-dd
def date_4_history(date, history_date):
    date_time = datetime.datetime.strptime(date, "%Y-%m-%d")
    date_time_month = datetime.datetime.strftime(date_time, "%m")
    date_time_day = datetime.datetime.strftime(date_time, "%d")
    history_date_time = datetime.datetime.strptime(history_date, "%Y-%m-%d")
    history_date_time_month = datetime.datetime.strftime(history_date_time, "%m")
    history_date_time_day = datetime.datetime.strftime(history_date_time, "%d")
    if date_time_month == history_date_time_month and date_time_day == history_date_time_day:
        return True
    return False

date_4_history("2020-09-29", "1999-09-28")

# date_add_for_year(None,-5,'%Y%m%d')
# date_diff('2020-09-01','2020-09-08')