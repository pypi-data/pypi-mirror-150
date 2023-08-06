import os
import logging

"""
级别排序:CRITICAL > ERROR > WARNING > INFO > DEBUG
格式化
%(levelno)s：打印日志级别的数值
%(levelname)s：打印日志级别的名称
%(pathname)s：打印当前执行程序的路径，其实就是sys.argv[0]
%(filename)s：打印当前执行程序名
%(funcName)s：打印日志的当前函数
%(lineno)d：打印日志的当前行号
%(asctime)s：打印日志的时间
%(thread)d：打印线程ID
%(threadName)s：打印线程名称
%(process)d：打印进程ID
%(message)s：打印日志信息
"""

out_formatter = logging.Formatter('%(asctime)s %(threadName)s %(levelname)s %(filename)s:%(lineno)d >>> %(message)s')


# out_formatter = logging.Formatter('%(asctime)s %(threadName)s %(levelname)s %(pathname)s:%(lineno)d >>> %(message)s')


# 输出到文件
def to_file_handler(log_file, level=3, mode='a'):
    file_path = os.path.dirname(log_file)
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    level_conf = {
        1: logging.DEBUG,
        2: logging.INFO,
        3: logging.WARNING,
        4: logging.ERROR,
        5: logging.CRITICAL,
    }
    handler = logging.FileHandler(log_file, mode=mode)
    handler.setFormatter(out_formatter)
    handler.setLevel(level_conf[level])
    return handler


# 输出到console
def to_console_handler():
    handler = logging.StreamHandler()
    handler.setFormatter(out_formatter)
    handler.setLevel(logging.INFO)
    return handler


console_handler = to_console_handler()
logging.getLogger().setLevel(logging.DEBUG)  # 这里应用了单例模式，注意如果这里不设置信息等级的话，StreamHandler的设置将无效
logging.getLogger().addHandler(console_handler)
# logging.getLogger().removeHandler(console_handler)

if '__main__' == __name__:
    logging.debug(u"debug")  # 打印全部的日志,详细的信息,通常只出现在诊断问题上
    logging.info(u"info")  # 打印info,warning,error,critical级别的日志,确认一切按预期运行
    logging.warning(u"warning")  # 打印warning,error,critical级别的日志,一个迹象表明,一些意想不到的事情发生了,或表明一些问题在不久的将来(例如。磁盘空间低”),这个软件还能按预期工作
    logging.error(u"error")  # 打印error,critical级别的日志,更严重的问题,软件没能执行一些功能
    logging.critical(u"critical")  # 打印critical级别,一个严重的错误,这表明程序本身可能无法继续运行
    try:
        print(1 + 'a')
    except Exception as e:
        logging.critical("发生异常 {}".format(e), exc_info=True)
