from mini_django.core.handler import base


class WsgiHandler(base.BaseHandler):

    def __init__(self, *args, **kwargs):
        self.load_middlen()
        super().__init__(*args, **kwargs)

    def __call__(self, environ, start_response):
        """
        :param environ:  handler的response
        :param start_response: 返回response
        :return:
        """
        print("调用了__call__方法")
