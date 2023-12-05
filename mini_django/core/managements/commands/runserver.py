import sys
from datetime import datetime
from mini_django.core.servers.base_http import run, get_internal_wsgi_application
from mini_django import settings


class RunServer():
    """
    todo Django中的  django/django/core/management/commands/runserver.py 中的Command类
    mini Django 暂时不写命令，只实现发送请求返回结果
    """

    def __init__(self):
        self.protocol = "http://"

    def run(self, use_reloader, addr, port, threading):
        """
        启动wsgi服务，
        todo 现在不写热加载，后面在追加热加载，先只考虑手动修改
        检查是否要热加载，然后根据不同来启动wsgi服务
        :param use_reloader: 是否热加载
        :param addr: host地址
        :param port: 端口
        :param threading: 多线程
        :return:
        """
        if use_reloader:
            # 暂时跳过热加载
            pass
        self.inner_run(addr, port, threading)

    def get_handler(self, *args, **options):
        """
        获取到一个WSGIhandler，todo 用户出去发过来的请求
        :param args:
        :param options:
        :return:
        """
        return get_internal_wsgi_application()

    def inner_run(self, addr, port, threading):
        """
        获取到WSGIhandler服务，
        然后在
        启动wsgi服务
        :param addr: 地址
        :param port: 端口
        :param threading 是否启动多线程
        :return:
        """
        wsgi_handler = self.get_handler()
        run(addr, port, wsgi_handler, True, threading, on_bind=self.on_bind)

    def get_version(self):
        """
        获取Django版本
        :return: string
        """
        return "1.0.0"

    def on_bind(self, addr, server_port):
        """
        提示用户输出内容
        :param server_port:
        :return:
        不支持ipv6
        """
        now = datetime.now().date()

        quit_command = "CTRL-BREAK" if sys.platform == "win32" else "CONTROL-C"
        if addr == '0':
            addr = '0.0.0.0'
        tim_message = f"""
        {now}\n
        Django version {self.get_version()}, using settings {settings.SETTINGS_MODULE!r}\n
        Starting development server at {self.protocol}{addr}:{server_port}/\n
        Quit the server with {quit_command}.,
        """
        print(tim_message)
