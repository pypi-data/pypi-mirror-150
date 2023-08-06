from urllib import parse


# 分割http请求头
def fix_headers(headers_string):
    headers = {}
    headers_list = headers_string.split("\n")
    for row in headers_list:
        row = row.strip()
        if row:
            t = row.split(': ')
            headers[t[0]] = t[1].strip()
    return headers


# 把URL中的参数转成字典
def query_parse(url, get_param=None):
    rst = parse.urlparse(url)
    params = parse.parse_qs(rst.query)
    params = {key: params[key][0] for key in params}
    if get_param:
        return params.get(get_param)
    return params


# 从URL中提取路径
def url_parse(url):
    rst = parse.urlparse(url)
    # print('原始参数', rst.query)
    # print('路径', rst.path)
    # print('协义', rst.scheme)
    # print('地址端口', rst.netloc)
    # print('地址', rst.hostname)
    # print('端口', rst.port)
    return rst.path


if '__main__' == __name__:
    u = 'http://111.231.203.16:8082/v1/registerDevice?andid=076c5e3600f45582&device_brand=Android&imei=359250052187091&imsi=460002010621516&mac=40%3A45%3Ada%3A99%3A38%3A3a&device_type=HammerHead&ser=913600345152&os_version=4.4.4&os_api=19&resolution=1776*1080&dpi=480'
    print(query_parse(u))
    print(url_parse(u))
