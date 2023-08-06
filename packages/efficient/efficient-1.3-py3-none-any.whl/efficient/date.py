import time
import datetime


# 格式化时间戳为日期
def date(fmt=None, timestamp=None):
    if fmt is None:
        fmt = '%Y-%m-%d %H:%M:%S'
    if timestamp is None:
        timestamp = round(time.time())
    date_str = time.strftime(fmt, time.localtime(timestamp))
    return date_str


# 日期转为时间戳
def date_to_time(date_str, fmt="%Y-%m-%d %H:%M:%S"):
    # date convert to array
    time_array = time.strptime(date_str, fmt)
    timestamp = round(time.mktime(time_array))
    return timestamp


# 日期计算，以天累加
def calc_date(days=0, fmt='%Y-%m-%d'):
    now_time = datetime.datetime.now()
    calculate = now_time + datetime.timedelta(days=days)
    return calculate.strftime(fmt)


if '__main__' == __name__:
    print(date('%Y%m%d'))
    print(date('%Y-%m-%d', time.time() + 30 * 24 * 3600))
    print(date('%Y-%m-%d %H:%M:%S', 1))
    print(date_to_time('2018-12-09 12:30:21'))
    print(calc_date(-2, '%Y-%m-%d %H:%M:%S'))
