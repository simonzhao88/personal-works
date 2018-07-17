import socket


# 定义类的属性来存储请求信息
class Request(object):
    # 初始化函数，一般用来定义类的属性
    # 属性可以理解为类用来存储数据的容器
    def __init__(self):
        self.path = ''
        self.query = {}


request = Request()


# 保存数据到本地
def save(n):
    n = str(n)
    with open('count.txt', 'w', encoding='utf-8') as f:
        f.write(n)


# 本地读取数据
def load():
    with open('count.txt', 'r', encoding='utf-8') as f:
        n = f.read()
        return int(n)


def template(filename):
    """
    实现渲染模板
    :param filename:
    :return:
    """
    with open('templates/' + filename, 'r', encoding='utf-8') as f:
        return f.read()


def route_index(request):
    # 点击主页 点击量加1
    save(load() + 1)
    header = 'HTTP/1.1 210 OK\r\nContent-Type:text/html\r\n'
    body = template('index.html')
    body = body.replace('{{count}}', str(load()))
    r = header + '\r\n' + body
    # str 转成 bytes
    return r.encode(encoding='utf-8')


def route_static(request):
    if request.path == '/audio':
        print('request.path', request.path)
        content_type = 'audio/mp3'
    else:
        content_type = 'image/gif'

    filename = request.query.get('file', '27.jpg')
    path = 'static/' + filename
    with open(path, 'rb') as f:
        header = 'HTTP/1.1 210 OK\r\nContent-Type: {}\r\n\r\n'.format(content_type)
        header = bytes(header, encoding='utf-8')
        response = header + f.read()
        return response


def parsed_path(path):
    """
    处理请求的地址
    :param path:/video?av=1024&id=2/
    :return:
    """
    index = path.find('?')
    if index == -1:
        return path, {}
    else:
        path, query_s = path.split('?', 1)
        args = query_s.split('&')
        query = {}
        for arg in args:
            k, v = arg.split('=')
            query[k] = v
        return path, query


def response_for_path(path):
    path, query = parsed_path(path)
    # 将按到的信息存储起来
    request.path = path
    request.query = query
    # 路由字典
    r = {
        '/': route_index,
        '/audio': route_static,
        '/img': route_static,
        '/favicon.ico': route_static
    }
    response = r.get(path)
    # 调用response函数
    return response(request)


def run(host='', port=3000):
    with socket.socket() as s:
        # 绑定地址和端口
        s.bind((host, port))
        while True:
            # 监听
            s.listen(3)
            connection, address = s.accept()
            # 每次接收1024bytes
            r = connection.recv(1024)

            r = r.decode('utf-8')
            if len(r.split()) < 2:
                continue
            path = r.split()[1]
            # 解析请求并生成返回数据
            response = response_for_path(path)
            # 返回请求
            connection.sendall(response)
            # 关闭本次连接
            connection.close()


if __name__ == '__main__':
    run('0.0.0.0', 3000)
