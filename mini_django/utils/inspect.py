import inspect


def get_callable_params(method_or_func):
    """
    获取函数或者方法的参数列表。
    :param method_or_func:
    :return:
    1. 验证当前函数是方法还是函数
    2. 获取到func对象
    """
    is_method = inspect.ismethod(method_or_func)
    func = method_or_func.__func__ if is_method else method_or_func


def get_func_params(func, remove_first):
    """
    获取函数的参数
    :param func:
    :param remove_first:
    :return:
    """
    pamters = inspect.Signature(func).parameters.values()
    if remove_first:
        pamters = pamters[1:]
    return pamters


def valid_func_accepty_kwargs(func):
    """
    验证函数是否接受关键字参数
    :param func:
    :return:
    https://docs.python.org/zh-cn/3/library/inspect.html#inspect.Parameter
    """
    return any(p for p in get_callable_params(func) if p.kind == p.VAR_KEYWORD)
