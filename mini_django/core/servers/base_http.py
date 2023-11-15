from wsgiref import simple_server
from mini_django import settings


def get_internal_wsgi_application():
    """
    获取wsgi_application应用
    从配置文件里面取，
    如果配置文件没有，就返回默认的，如果有就返回配置文件的wsgi 应用
    :return:
    """
    try:
        wsgi_application = settings.WSGI_APPLICATION

    except AttributeError as ex:
        pass


class WSGIServer(simple_server.WSGIServer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class WSGIRequestHandler(simple_server.WSGIRequestHandler):
    pass


def run(
        addr,
        port,
        wsgi_handler,
        ipv6=False,
        threading=False,
        on_bind=None,
        server_cls: WSGIServer = WSGIServer,
):
    """
    开始启动wsgi服务，监听

    :param server_cls: wsgi服务，
    :param on_bind:
    :param addr:
    :param port:
    :param wsgi_handler: 处理http请求的方法
    :param ipv6:
    :param threading:
    :param on_bind Func:
    :return:
    """
    server_address = (addr, port)
    httpd = server_cls(server_address, WSGIRequestHandler)
    httpd.set_app(wsgi_handler)
    httpd.serve_forever()


if __name__ == '__main__':
    get_internal_wsgi_application()
