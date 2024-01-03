# python中的method和func
## 什么是method，什么是func(个人理解)
method就是一个类里面的函数。
method会隐式的传递一个self或者cls参数，这个self、cls参数就是这个类的实例 。
method会有一个__func__属性，指向了这个method的func。

func就是一个函数，他不会隐式的传递一个self参数。
func是没有__func__属性的。
func 就是一个代码块，他可以是lambda 也可以是我们使用的def定义的函数。
但是注意一下，类的@statisticmethod 他们不是method，他们是func。


## 举个例子
我们可以使用inspect.ismethod来判断一个对象是否是method
```python
import inspect


def valid_is_method(meth_or_func):
    is_method = inspect.ismethod(meth_or_func)
    print(is_method, meth_or_func.__name__)


class TestObject(object):
    def test_method(self):
        pass

    @classmethod
    def test_classmethod(cls):
        pass

    @staticmethod
    def test_staticmethod():
        pass


def test_function():
    pass


if __name__ == '__main__':
    valid_is_method(TestObject().test_method)  # True test_method
    valid_is_method(TestObject().test_classmethod)  # True test_classmethod
    valid_is_method(TestObject.test_classmethod)  # True test_classmethod
    valid_is_method(TestObject.test_staticmethod)  # False test_staticmethod
    valid_is_method(test_function)  # False test_function
    valid_is_method(lambda x: x)  # False <lambda>
```
在这里我们可以很直观的看到，只有类里面的函数才是method。而且类的静态方法不是method，他是func。

