from json import dumps as json_dumps


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


# 搜索元素在数组中的路径
class Tree:
    __key = None  # 数组的键名，如果是数字就转成字符串
    __val = None  # 数组的键值

    def __init__(self, data, key=None):
        # 把数组转成树状结构，查找的时候每个分枝对比自己的__val就好了
        self.__key = key
        if type(data) is dict:
            for k, v in data.items():
                setattr(self, k, Tree(v, k))
        elif type(data) is list:
            for idx, i in enumerate(data):
                setattr(self, str(idx), Tree(i, str(idx)))
        else:
            self.__val = data

    def search(self, val, path=''):
        for i in self.__dict__:
            # print(type(i), i)
            if '_Tree' not in i:
                _t = getattr(self, i)
                _t.search(val, "{}/{}".format(path, _t.__key))
                if _t.__val == val:
                    print('搜索结果', val, path + '/' + _t.__key)
