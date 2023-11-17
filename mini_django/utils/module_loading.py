import sys
from importlib import import_module


def import_string(pathlib: str):
    """
    通过字符串导入制定的类
    :param pathlib:
    :return:
    """
    # mini_django.core.a  mini_django.core a
    try:
        path_, class_name = pathlib.rsplit('.', 1)
    except ValueError as _:
        ImportError("%s dones‘t look like a module path'" % pathlib)


def cached_import(path, class_name):
    """
    从缓存里面导入类，
    检查当前类是否存在
    检查是否已经加载，获取module的meta信息，查看是否初始化完成
    :param path:
    :param class_name:
    :return:
    """
    if not (
            (module := sys.modules.get(class_name)) and
            (spec := getattr(module, '__spec__', None)) and
            (_initializing := getattr(spec, '_initializing', False))
    ):
        module = import_module(path, class_name)
    return getattr(module, class_name)
