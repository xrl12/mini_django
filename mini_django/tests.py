import inspect


def get_callable_parameters(meth_or_func):
    """
    区分是method还是func。

    :param meth_or_func:
    :return:
    """
    is_method = inspect.ismethod(meth_or_func)
    func = meth_or_func.__func__ if is_method else meth_or_func
    return get_func_params(func, is_method)


def get_func_params(func, remove_first_param):
    """
    获取函数的参数列表
    :param func: func属性
    :param remove_first_param: 是否移除第一个参数，因为method第一个参数是self，或者cls
    :return:
    """
    parameters = tuple(inspect.signature(func).parameters.values())
    if remove_first_param:
        parameters = parameters[1:]
    return parameters


class Test(object):
    def test_aabb(self, *args, **kwargs):
        pass

    @classmethod
    def test_class(cls, *args, **kwargs):
        pass


if __name__ == '__main__':
    # get_callable_parameters(Test().test_aabb)
    # get_callable_parameters(Test().test_class)
    for paramter in get_callable_parameters(Test.test_class):
        print(paramter.VAR_POSITIONAL)
        print(paramter.kind)
        print(paramter.name)
