import sys
from datetime import datetime
from mini_django.core.servers.base_http import run
from mini_django import settings


class RunServer():
    """
    todo Django中的  django/django/core/management/commands/runserver.py 中的Command类
    mini Django 暂时不写命令，只实现发送请求返回结果
    """

    def __init__(self):
        self.protocol = "http://"

    def run(self, use_reloader):
        """
        启动wsgi服务，
        todo 现在不写热加载，后面在追加热加载，先只考虑手动修改
        检查是否要热加载，然后根据不同来启动wsgi服务
        :param use_reloader: 是否热加载
        :return:
        """
        if use_reloader:
            # 暂时跳过热加载
            pass
        self.inner_run()

    def get_handler(self, *args, **options) -> None:
        """
        获取到一个WSGIhandler，todo 用户出去发过来的请求
        :param args:
        :param options:
        :return:
        """


    def inner_run(self, *args, **options):
        """
        获取到WSGIhandler服务，
        然后在
        启动wsgi服务
        :param args:
        :param options:
        :return:
        """
        handler = self.get_handler()
        run()

    def get_version(self):
        """
        获取Django版本
        :return: string
        """
        return "1.0.0"

    def on_bind(self, server_port, addr):
        """
        提示用户输出内容
        :param server_port:
        :return:
        不支持ipv6
        """
        now = datetime.now().date()

        quit_command = "CTRL-BREAK" if sys.platform == "win32" else "CONTROL-C"
        tim_message = f"""
        {now}\n
        Django version {self.get_version()}, using settings {settings.SETTINGS_MODULE!r}\n
        Starting development server at {self.protocol}://{addr}:{server_port}/\n
        Quit the server with {quit_command}.,
        """
        print(tim_message)
