import sys
import time
import socket
import datetime
import subprocess
from json import dumps as json_dumps


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
def calculate_date(days=0, fmt='%Y-%m-%d'):
    now_time = datetime.datetime.now()
    calculate = now_time + datetime.timedelta(days=days)
    return calculate.strftime(fmt)


# 获取本机ip地址
def get_my_ip():
    return socket.gethostbyname(socket.gethostname())


# 分割http请求头
def fix_headers(headers_string, is_h2=False):
    headers_list = headers_string.split("\n")
    headers = {}
    h2 = []
    for row in headers_list:
        row = row.strip()
        if row:
            h2.append(row)
            t = row.split(': ')
            headers[t[0]] = t[1].strip()
    if is_h2:
        return h2
    return headers


# json数据提取
def fix_data(config, data):
    """
    :param config: dict eg: {'uid':'uid','name':['user_info','nickname']}
    :param data: dict
    :return:dict
    """
    sql_data = {}
    for k, v in config.items():
        if type(v) is list:
            tmp = None
            for idx, field in enumerate(v):
                if idx > 0:
                    try:
                        tmp = tmp[field]
                    except Exception as e:
                        tmp = None
                else:
                    try:
                        tmp = data[field]
                    except Exception as e:
                        pass
            sql_data[k] = tmp
        else:
            try:
                sql_data[k] = data[v]
            except Exception as e:
                sql_data[k] = None
    # 数据格式化
    for k, v in sql_data.items():
        if type(v) is bool:
            sql_data[k] = 1 if v else 0
        if type(v) in [dict, list]:
            sql_data[k] = json_dumps(v)
    return sql_data


# URL解析
def url_parse(url, idx=-1):
    _split = url.split('?')
    s1 = _split[0].strip('/').split('/')
    if idx is not None:
        return s1[idx]
    return s1


# URL参数解析
def query_parse(url, get_param=None):
    _split = url.split('?')
    s1 = _split[1].split('&')
    p = {}
    for i in s1:
        s2 = i.split('=')
        p[s2[0]] = s2[1]
    if get_param:
        return p.get(get_param)
    return p


# print的颜色
def color(content, conf='0'):
    """
    格式：\033[显示方式;前景色;背景色m … \033[0m
    显示方式，前景色，背景色是可选参数，可以只写其中的某一个或者某两个；
    由于表示三个参数不同含义的数值都是唯一没有重复的，所以三个参数的书写先后顺序没有固定要求，系统都可识别；
    建议按照默认的格式规范书写。
    ###### 显示方式
    0	终端默认设置
    1	高亮显示
    4	使用下划线
    5	闪烁
    7	反白显示
    8	不可见
    22	非高亮显示
    24	去下划线
    25	去闪烁
    27	非反白显示
    28	可见
    ###### 前景色/背景色
    30	40	黑色
    31	41	红色
    32	42	绿色
    33	43	黄色
    34	44	蓝色
    35	45	紫红色
    36	46	青蓝色
    37	47	白色
    """
    return '\033[{conf}m{content}\033[0m'.format(conf=conf, content=content)


def cmd(command, encoding='gb2312'):
    # 加了encoding后out为str，不加的话是 bytes，加encoding后流输出会换行
    result = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, encoding=encoding)
    full_out = ''  # 执行结果
    while True:
        out = result.stdout.readline(1)  # limit -1：等待读完一行 1：读一个字符
        full_out += out
        sys.stdout.flush()  # 如果注释的话，会读完一行才显示
        if not out:
            break
    return full_out


if '__main__' == __name__:
    print(date('%Y%m%d'))
    print(date('%Y-%m-%d', time.time() + 30 * 24 * 3600))
    print(date('%Y-%m-%d %H:%M:%S', 1))
    print(date_to_time('2018-12-09 12:30:21'))
    print(calculate_date(-2, '%Y-%m-%d %H:%M:%S'))
    print(get_my_ip())
    print(color('哈哈', '4;31;47'))
