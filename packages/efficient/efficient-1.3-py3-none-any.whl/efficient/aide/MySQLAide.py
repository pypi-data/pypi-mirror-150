import time
import pymysql
from DBUtils.PooledDB import PooledDB
from pymysql.converters import escape_string

"""
pip install pymysql
pip install DBUtils
连接断开的问题可修改以下参数
self.__cursor.execute('set wait_timeout = 24*3600;')
self.__cursor.execute('set global max_allowed_packet = 67108864;')
self.__cursor.execute('set interactive_timeout = 24*3600;')
"""


class MySQLAide:
    __db_config = None
    __db = None  # 数据库
    __cursor = None  # 操作游标
    pool = None

    class UnknownError(Exception):
        pass

    @classmethod
    def init_connection_pool(cls, conf):
        """
        :param conf:
        {
            'mincached':2,
            'maxcached':2,
            'maxconnections':2,
            'host':'host',
            'username':'host',
            'password':'password',
            'db_name':'db_name',
            'port':3306,
            'charset':'charset',
        }
        """
        t1 = time.time()
        if cls.pool is not None:
            return
        cls.pool = PooledDB(
            creator=pymysql,
            mincached=conf['mincached'],  # 启动时开启的空连接数量
            maxcached=conf['maxcached'],  # 连接池最大可用连接数量
            maxconnections=conf['maxconnections'],  # 最大允许连接数量
            blocking=True,  # 达到最大数量时是否阻塞
            host=conf['host'],
            user=conf['username'],
            passwd=conf['password'],
            db=conf['db_name'],
            port=conf['port'],
            charset=conf['charset'],
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )
        print('生成{}个连接用时'.format(conf['mincached']), time.time() - t1)

    def __init__(self, host=None, username=None, password=None, db_name=None, port=3306, charset='utf8mb4', use_pool=False):
        # 当出现：1366, “Incorrect string value: ‘\xF0\x9F\x98\x81’可以修改连接编码为utf8mb4，当然在数据库中也要设置
        if use_pool:
            self.__db = self.pool.connection()
            self.__cursor = self.__db.cursor()  # 使用cursor()方法获取操作游标
        else:
            self.__db_config = {
                'host': host,
                'username': username,
                'password': password,
                'db_name': db_name,
                'port': port,
                'charset': charset,
            }
            self.__connect()

    def __connect(self):
        self.__db = pymysql.connect(
            host=self.__db_config['host'],
            user=self.__db_config['username'],
            password=self.__db_config['password'],
            database=self.__db_config['db_name'],
            port=self.__db_config['port'],
            cursorclass=pymysql.cursors.DictCursor  # 使返回结果为字典
        )
        self.__cursor = self.__db.cursor()  # 使用cursor()方法获取操作游标
        self.__cursor.execute('set names {charset}'.format(charset=self.__db_config['charset']))

    def reconnect(self):
        self.__db.ping()

    def query(self, sql_str):
        self.__cursor.execute(sql_str)
        return self.__cursor

    def insert(self, table_name, data, need_sql_str=False):
        field, value = '', ''  # 字段,数据值
        for (k, v) in data.items():
            field += '`{}`,'.format(k.rstrip())
            if v is None:
                value += 'null,'
            else:
                value += '"{value}",'.format(value=escape_string(str(v)))
        sql_str = 'INSERT INTO {table_name} ({fields}) VALUES({values});'.format(table_name=table_name, fields=field[0:-1], values=value[0:-1])
        if need_sql_str:
            return sql_str
        self.__query(sql_str)
        return self.__cursor.lastrowid  # 返回刚插入的数据id

    def update(self, table_name, data, condition, need_sql_str=False):
        sql_str = 'UPDATE {table_name} SET '.format(table_name=table_name)
        for (k, v) in data.items():
            if v is None:
                sql_str += '`{k}` = null,'.format(k=k)
            else:
                sql_str += '`{k}` = "{v}",'.format(k=k, v=escape_string(str(v)))
        sql_str = '{sql_str} WHERE {condition};'.format(sql_str=sql_str[0: -1], condition=condition)
        if need_sql_str:
            return sql_str
        self.__query(sql_str)
        return self.__cursor.rowcount  # 返回影响的数据条数

    def insert_batch(self, table_name, data, limit=2):
        for a in range(0, len(data), limit):  # 把数据分批插入
            b = a + limit
            sql_str = ''
            for one in data[a:b]:
                field, value = '', ''  # 字段,数据值
                for (k, v) in one.items():
                    field += f'`{k.rstrip()}`,'
                    if v is None:
                        value += 'null,'
                    else:
                        value += '"{value}",'.format(value=escape_string(str(v)))
                sql_str += 'INSERT INTO {table_name} ({fields}) VALUES({values});'.format(table_name=table_name, fields=field[0:-1], values=value[0:-1])
            self.__query(sql_str)  # 需要连接数据库时加上allowMultiQueries=true

    def delete(self, table_name, condition):
        sql_str = 'DELETE FROM {table_name} WHERE {condition}'.format(table_name=table_name, condition=condition)
        self.__query(sql_str)
        return self.__cursor.rowcount  # 返回影响的数据条数

    def one(self, table_name, condition='1', order=None, field='*'):
        sql_str = 'SELECT {field} FROM {table_name} WHERE {condition}'.format(field=field, table_name=table_name, condition=condition)
        if order:
            sql_str += ' ORDER BY {order}'.format(order=order)
        sql_str += ' LIMIT 1'
        self.__query(sql_str)
        return self.__cursor.fetchone()  # 取出数据,使用 fetchall() 方法获取多条数据

    def all(self, table_name, condition, field='*', order=None, limit=None):
        sql_str = 'SELECT {field} FROM {table_name} WHERE {condition}'.format(field=field, table_name=table_name, condition=condition)
        if order:
            sql_str += ' ORDER BY {order}'.format(order=order)
        if limit:
            sql_str += ' LIMIT {limit}'.format(limit=limit)
        self.__query(sql_str)
        return self.__cursor.fetchall()  # 取出数据,使用 fetchone() 方法获取一条数据

    def db(self):
        # 事务
        # db().begin()
        # db().commit()
        # db().rollback()
        return self.__db

    def __query(self, sql_str):
        try:
            self.__cursor.execute(sql_str)
            self.__db.commit()  # 注意如果不加commit会出现 ERROR 1205 (HY000): Lock wait timeout exceeded; try restarting transaction
        except pymysql.Error as e:
            self.__db.rollback()
            raise Exception('{e}; the sql was: {sql_str}'.format(e=e, sql_str=sql_str))
        except Exception as e:
            # 使用阿里的polardb报错：struct.error: unpack_from requires a buffer of at least 4 bytes
            self.__db.rollback()
            raise self.UnknownError('{e}; the sql was: {sql_str}'.format(e=e, sql_str=sql_str))

    def __del__(self):
        # print('mysql closed')  # 注意，线程中运行的时候，线程结束就开始关闭连接了
        self.__cursor.close()
        self.__db.close()


if '__main__' == __name__:
    test = MySQLAide('120.79.180.249', 'root', 'z#Ss1g12Mm_over3', 'test')
    print(test.query('show tables').fetchall())
    print(test.insert('users', {'name': 2}))
    print(test.update('users', {'name': 5}, 'id = 8'))
    print(test.one('users', 'id = 8'))
    print(test.all('users', 'id < 8'))
