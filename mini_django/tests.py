from wsgiref import simple_server


def application(environ, start_response):
    # 分发路由
    print(environ, 'envion')
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [b'<h1>Hello, web!</h1>']


class WSGIHandler(simple_server.WSGIRequestHandler):
    """
    处理request请求的
    """

    def __init__(self, *args, **kwargs):
        print('我初始化handler了', *args, **kwargs)
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        print('调用WSGIHandler')

    def handler(self):
        print('调用了handler方法')


class WSGIServer(simple_server.WSGIServer):
    """
    启动的wsgi服务¥
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


if __name__ == '__main__':
    # server.py
    # 从wsgiref模块导入:
    from wsgiref.simple_server import make_server

    # 导入我们自己编写的application函数:
    # 创建一个服务器，IP地址为空，端口是8000，处理函数是application:
    httpd = WSGIServer(('0.0.0.0', 8001), WSGIHandler)
    httpd.set_app(application)
    print('Serving HTTP on port 8001...')
    # 开始监听HTTP请求:
    httpd.serve_forever()
