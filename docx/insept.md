# inspect
## 版本
### python
3.9.6
### inspect
python 自带

## 具体功能
### 判断是否是一个绑定方法(ismethod)

```python
import inspect


def get_func_params(func):
    """
    获取函数参数
    :return:
    """
    # https://docs.python.org/zh-cn/3.9/library/inspect.html?highlight=signature
    sig = inspect.signature(func)
    print(inspect.ismethod(func)) 


class TestObject(object):
    def test_aa(self, *args, **kwargs):
        print('test-aa-------')

    @classmethod
    def test_bb(cls, *args, **kwargs):
        print('test_bb')

    @staticmethod
    def test_cc(*args, **kwargs):
        print('test_cc')

    def __call__(self, a, b, c, d, e, *args, **kwargs):
        print('aabbcc')


if __name__ == '__main__':
    # get_func_params(TestObject())
    get_func_params(TestObject().test_aa)  # True
    get_func_params(TestObject.test_bb)  # True
    get_func_params(TestObject().test_bb)  # true
    get_func_params(TestObject().test_cc)  # False
    get_func_params(TestObject.test_cc)  # False
    get_func_params(lambda x: x)  # False
    get_func_params(TestObject) # False


```

