def import_string(pathlib: str):
    """
    通过字符串导入模块
    :param pathlib:
    :return:
    """
    # mini_django.core.a  mini_django.core a
    try:
        path_, class_name = pathlib.rsplit('.', 1)
    except ValueError as _:
        ImportError("%s dones‘t look like a module path'" % pathlib)
