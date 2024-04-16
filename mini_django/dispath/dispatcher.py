import weakref
import threading
from mini_django.utils.inspect import valid_func_accept_kwargs
from asgiref.sync import iscoroutinefunction


def make_id(target):
    """
    生成一个唯一的id
    查看是否是一个类函数，然后返回内存地址
    :param target:
    :return:

    """
    if hasattr(target, '__func__'):
        return id(target.self), id(target.__func__)
    return id(target)


class Signal(object):
    __doc__ = """"
    信号类，
    
    
    """

    def __init__(self):
        self.receivers = []  # 接收列表
        self.lock = threading.Lock()  # 上锁
        self.deal_revers = False  # 死亡的接收者，

    def connect(self, receiver, sender, weak=True, dispatch_uid=False):
        """
        订阅者和发布者连接起来
        Arguments
        sender:
        :return:
        receiver:
            接收者
            一个函数或者一个类的实例方法，一个信号的接收者。
            接收者必须是哈洗对象，接收者也可是使用async

            如果 weaker是true，那么receviers必须是weak referenceable

            receiver必须是可以使用关键字参数的，

            如果使用了dispatch_uid这个参数，如果已经存在了dispatch_uid这个接收器，那么他将不会再添加

        sender
            接收者接听那个发送着的信号。必须是python对象或者是none给接收者或其他的发送着

        weak
            是否使用weak ref给发送者，默认会使用弱引用给接收者，如果这个参数是false
            强引用会被使用

        dispatch_uid
            一个接收者的唯一标识符，通常是一个字符串，但是他也可以是一任意一个哈希值

        1. 验证接收者是否可以被调用，和验证接收者是否支持关键词函数
        2. 给接收者和发送者生成一个唯一的id
            检查是否传入了dispatch_uid，如果传入了，那么就使用这个，如果没有传入，使用内存地址

        总结
            验证是否可以被调用
            验证是否是异步函数
            验证是否支持关键字参数（必须支持）
            生成唯一ID

            检查接收者的唯一性

            把已经死亡的接收者给清空
            查看是否使用弱引用。
                使用
                    根据是否是bound函数，维护的接收者的引用对象
                不使用
                    维护接收者
        """
        # 1. 验证接收者是否可以被调用
        if not callable(receiver):
            raise RuntimeError('receiver not callable')
        # 2. 验证接收者是否支持关键词函数
        if not valid_func_accept_kwargs(receiver):
            raise RuntimeError('receiver does not accept keyword arguments')

        # 3. 给接收者和发送者生成一个唯一的id
        if dispatch_uid:
            lookup_key = (dispatch_uid, make_id(sender))
        else:
            lookup_key = (make_id(receiver), make_id(sender))
        # 4. 验证接收者是否支持async
        is_async = iscoroutinefunction(receiver)
        with self.lock:
            # 多进程
            """
            获取接收者对象，
            区分是否是bound函数，如果是bound函数，则对象就是实例，如果不是则对象就是本身
            """
            receiver_obj = receiver
            # 检查是否使用弱引用
            if weak:
                ref = weakref.ref
                # 1. 检查是否为bound方法
                if hasattr(receiver, '__self__') and hasattr(receiver, '__func__'):
                    ref = weakref.WeakMethod
                    receiver_obj = getattr(receiver, '__self__')
                receiver = ref(receiver)
                # 2. 监听接收者对象，当有接收者对象死亡当时候，触发
                weakref.finalize(receiver_obj, self._remove_receiver)
            # 3. 清理掉死亡当接受者
            self.clear_dead_receiver()
            # 4. 判断当前接收者是否可重复了
            if not any([lookup_key == lookup for lookup, _, _ in self.receivers]):
                self.receivers.append([lookup_key, receiver, is_async])

    def clear_dead_receiver(self):
        """
        清除已经死掉的接收者
        :return:
        """
        if self.deal_revers:
            self.receivers = [

            ]

    def send(self, sender, **kwargs):
        """
        发布者监听信息
        todo
        1. 检查接收
        发送信用给告诉所有已经连接的监听着
        如果有一个监听者有了异常，通过发送者把错误返回来。
        所以
        :param sender:
        :return:
        """

    def _remove_receiver(self, true=True):
        self.deal_revers = true
