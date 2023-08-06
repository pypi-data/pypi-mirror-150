import os
import sys
import traceback

"""
sys._getframe().f_back.f_lineno                # 获取调用行号
sys._getframe().f_back.f_code.co_name          # 获取调用函数名
sys._getframe().f_back.f_code.co_filename      # 获取调用函数文件名
sys._getframe().f_lineno                       # 获取当前行号
sys._getframe().f_code.co_name                 # 获取当前函数名
sys._getframe().f_code.co_filename             # 获取当前函数所在文件名

sys.argv # 接收shell脚本传入的参数
sys.path.append(path) # 加入到python系统的环境变量
sys.argv[0] # 代码本身文件路径
sys.argv[1] # 第一个命令行参数
sys.path[0] # 此元素是在程序启动时初始化，自动寻找脚本的目录，所以亦是被运行脚本所在的真实目录

os.path.basename(__file__) # 当前文件名
os.path.dirname(__file__) # 当前目录名
os.path.split(__file__) # 分割成目录与文件
os.path.abspath(__file__) # 返回文件的真实路径，而非软链接所在的路径同os.path.realpath
os.getcwd() # 返回当前工作目录，同sys.path[0]

关于模块导入
在一段程序中相同的模块只会被导入一次
"""

# 文件栈
file_stack = []
call_stack = traceback.extract_stack()
for s in call_stack:
    # 'filename', 文件名
    # 'line', 具体代码
    # 'lineno', 行号
    # 'locals',
    # 'name',函数名
    if '<module>' == s.name:
        file_stack.append(s.filename)  # 如果导入者为入口文件，需要带上绝对路径


# 查看调用文件栈
def show_file_stack():
    for f in file_stack:
        print('show_file_stack: ', f)


# 注册目录到py环境
def register(_file: str):
    sys.path.append(os.path.dirname(_file))


# dirname 指定去除层级
def dir_peel(_file: str, hierarchy=1):
    for n in range(hierarchy):
        _file = os.path.dirname(_file)
    return _file


if '__main__' == __name__:
    print(__file__)
    print(dir_peel(__file__, 3))
    show_file_stack()
