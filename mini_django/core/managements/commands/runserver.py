class RunServer():
    """
    todo Django中的  django/django/core/management/commands/runserver.py 中的Command类
    mini Django 暂时不写命令，只实现发送请求返回结果
    """

    def run(self, use_reloader):
        """
        启动wsgi服务，
        检查是否要热加载，然后根据不同来启动wsgi服务
        :param use_reloader: 是否热加载
        :return:
        """

    def get_handler(self, *args, **options):
        """
        获取到一个WSGIhandler，todo 用户出去发过来的请求
        :param args:
        :param options:
        :return:
        """

    def inner_run(self, *args, **options):
        """
        启动wsgi服务
        :param args:
        :param options:
        :return:
        """

