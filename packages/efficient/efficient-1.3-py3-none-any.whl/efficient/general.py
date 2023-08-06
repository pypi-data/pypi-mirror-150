import sys
import socket
import subprocess
from math import pi, sin, cos, asin, sqrt


# 获取本机ip地址
def get_my_ip():
    return socket.gethostbyname(socket.gethostname())


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


# 执行cmd指令
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


# 根根两点经纬度计算距离
def distance2l(A, B):
    """
    :param A: [104.145759, 30.634445]
    :param B: [104.153808, 30.681665]
    :return: float
    """
    longitude1, latitude1 = A
    longitude2, latitude2 = B

    longitude1 = (longitude1 * pi) / 180
    latitude1 = (latitude1 * pi) / 180

    longitude2 = (longitude2 * pi) / 180
    latitude2 = (latitude2 * pi) / 180

    calc_longitude = longitude2 - longitude1
    calc_latitude = latitude2 - latitude1
    step_one = pow(sin(calc_latitude / 2), 2) + cos(latitude1) * cos(latitude2) * pow(sin(calc_longitude / 2), 2)
    step_two = 2 * asin(min(1, sqrt(step_one)))
    calculated_distance = 6367000 * step_two  # earthRadius = 6367000
    return round(calculated_distance)  # 单位米


if '__main__' == __name__:
    print(get_my_ip())
    print(color('哈哈', '4;31;47'))
    print(cmd('dir'))
    print(distance2l([104.145759, 30.634445], [104.153808, 30.681665]))
