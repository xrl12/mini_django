""""
重启服务类
"""
import itertools
import subprocess
import os
import signal
import sys
import threading
import time
from collections import defaultdict
from pathlib import PosixPath
import weakref
import types
from zipimport import zipimporter
from pathlib import Path
from functools import lru_cache

# from mini_django.dispath.dispatcher import Signal

# change_file = Signal()

DJANGO_AUTORELOAD_ENV = "RUN_MAIN"


def trigger_reload():
    """
    结束进程
    :return:
    """
    sys.exit(3)


class BaseReloader(object):
    def __init__(self, *args, **kwargs):
        self.stop_conditional = threading.Event()
        self.extra_file = {}
        self.direction_global = defaultdict()

    """
    监听文件是否发生改变
    """

    def watch_dir(self):
        """
        监听的文件
        :return:
        """

    def watch_file(self):
        """
        监听目录
        :return:
        """
        yield from iter_all_python_modules()

    def wait_app_ready(self):
        """
        查看app是否准备好（暂时不实现，等后面把app功能引入进来，在实现）
        :return:
        """
        return True

    def run_loop(self):
        """
        开始监听文件
        查看是否需要关闭
        :return:
        """
        tick = self.tick()
        while not self.should_stop:
            next(tick)
        self.stop()

    def tick(self):
        raise NotImplementedError('subclass must implement tick')

    def check_availability(self):
        raise NotImplementedError('subclass must implement availability')

    def notify_file_change(self, path: Path):
        """
            当文件发生改变的 时候触发，
            todo 发送一个信号，文件发生变化
        :return:
        """
        trigger_reload()

    @property
    def should_stop(self) -> bool:
        """
        需要停止当前服务
        :return:
        """
        return self.stop_conditional.isSet()

    def stop(self):
        """
        停止
        :return:
        """
        self.stop_conditional.set()

    def run(self):
        """
        主入口
        :return:
        """
        self.wait_app_ready()
        self.run_loop()


@lru_cache(maxsize=1)
def iter_all_python_modules():
    """
    迭代python所有模块
    :return:
    """
    keys = sorted(tuple(sys.modules))
    # 过滤调所有弱应用调模块
    modules = [m for m in map(sys.modules.__getitem__, keys) if m is not isinstance(m, weakref.ProxyType)]
    return iter_module_or_files(modules)


def iter_module_or_files(modules) -> [Path]:
    """
        检查当前模块是否是标准模块类型
        判断是否标准导入（如果标准导入一定是有spec属性的）
        判断是否是动态创建的，如果是动态创建的，就没有has_location属性
        **总结：就是过滤掉不需要监听的文件**

        返回Path对象

    :return:
    """
    sys_file_path = []
    result = set()
    for module in modules:
        if not isinstance(module, types.ModuleType):  # 检查当前模块是否是模块对象
            continue
        spec = getattr(module, '__spec__', None)
        if not spec:
            continue
        if getattr(module, '__name__') in ['__name__']:  # 判断是否在
            """
            判断是否在当前模块
            ├── mini_django
            │    ├── __init__.py
            │    ├── tests.py
            
            for i in map(sys.modules.__getitem__, keys):
                spec = getattr(i, '__spec__')
                if spec is None:
                    print('spec', i, i.__name__)
            在tests.py里面执行，就会i.__name__就会变成 __main__
            也就是说mini_django变成__main__
            """
            module.__file__ and sys_file_path.append(module.__file__)
        if spec.has_location:
            origin = (spec.loader.archive if isinstance(spec.loader, zipimporter) else spec.origin)
            sys_file_path.append(origin)
        for file in itertools.chain(sys_file_path):
            path = Path(file)
            if not path.exists():
                continue
            # sys_file_path.append(path.resolve().absolute())
            result.add(path.resolve().absolute())
    return frozenset(result)


class StatReloader(BaseReloader):
    def __init__(self, *args, **kwargs):
        self.global_time = 1  # 监听文件间隔时间
        super().__init__(args, kwargs)

    def check_availability(self):
        """
        监听文件的前序准备
        :return:
        """
        return True

    def tick(self):
        """
        监听文件，检查文件是否发生变化
        :return:
        """
        change_log = {}
        while True:
            for file, st_mtime in self.snapshot_files():
                last_st_mtime = change_log.get(file, None)
                change_log[file] = st_mtime
                if last_st_mtime is None:
                    continue
                elif last_st_mtime < st_mtime:
                    change_log[file] = st_mtime
                    self.notify_file_change(file)
            time.sleep(self.global_time)
            yield

    def snapshot_files(self) -> [str, str]:
        """
            返回文件地址和最后修改的时间
        :return:
        """
        snapshot_file = set()
        for file in self.watch_file():
            file: PosixPath
            if file in snapshot_file:
                continue
            elif not file.exists():
                continue
            st_mtime = file.stat().st_mtime
            snapshot_file.add(file)
            yield file, st_mtime


def get_reload_class() -> BaseReloader:
    """
    键擦好
    获取重启类
    Django里面会判断是否有pywatchman，这里现在只用自己手写的。

    :return:
    """
    return StatReloader()


def restart_with_reloader(*args, **kwargs):
    new_environ = {**os.environ, DJANGO_AUTORELOAD_ENV: "true"}
    while True:
        p = subprocess.run(['python', 'manage.py'], env=new_environ, close_fds=False)
        if p.returncode != 3:
            return p.returncode


def run_with_reload(main_func, *args, **kwargs):
    """
    Django每次更改完文件，都会从这里运行
    :param main_func:  运行Django的主文件
    :param args:
    :param kwargs:
    :return:
    todo
    1. 注册一个签名，当使用kill杀死进程当时候自动退出
    2. 判断是否是用户手起来的，

    3. 获取到监听类，
    4. 启动
    """
    """
           这里的判断，一开始 Django_AUTORELOAD_ENV 这个环境变量不能是’true'
        因为他会在restart_with_reloader这里执行一个死循环，然后设置Django_AUTORELOAD_ENV的值是true
        ，然后判断错误代码，如果错误代码不是3就return了，
        如果是3就继续循环
    """
    signal.signal(signal.SIGTERM, lambda x: sys.exit(0))
    if os.environ.get(DJANGO_AUTORELOAD_ENV) == 'true':
        reload = get_reload_class()
        start_new_thread(main_func, reload, *args, **kwargs)

    else:
        restart_with_reloader(*args, **kwargs)


def start_new_thread(main_func, reload: BaseReloader, *args, **kwargs):
    """
    开始启动一个新的进程
    :param main_func:
    :param args:
    :param kwargs:
    :return:
    """
    thread = threading.Thread(target=main_func, args=args, kwargs=kwargs, name='mini-django-main')
    thread.daemon = True
    thread.start()

    if not reload.should_stop:
        reload.run()
