def run(
    addr,
    port,
    wsgi_handler,
    ipv6=False,
    threading=False,
    on_bind=None,
    # server_cls=WSGIServer,
):
    """
    开始启动wsgi服务，监听
    :param addr:
    :param port:
    :param wsgi_handler:
    :param ipv6:
    :param threading:
    :param on_bind:
    :return:
    """
    # server_address = (addr, port)
    # if threading:
    #     httpd_cls = type("WSGIServer", (socketserver.ThreadingMixIn, server_cls), {})
    # else:
    #     httpd_cls = server_cls
    # httpd = httpd_cls(server_address, WSGIRequestHandler, ipv6=ipv6)
    # if on_bind is not None:
    #     on_bind(getattr(httpd, "server_port", port))
    # if threading:
    #     # ThreadingMixIn.daemon_threads indicates how threads will behave on an
    #     # abrupt shutdown; like quitting the server by the user or restarting
    #     # by the auto-reloader. True means the server will not wait for thread
    #     # termination before it quits. This will make auto-reloader faster
    #     # and will prevent the need to kill the server manually if a thread
    #     # isn't terminating correctly.
    #     httpd.daemon_threads = True
    # httpd.set_app(wsgi_handler)
    # httpd.serve_forever()
