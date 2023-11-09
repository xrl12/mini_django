# python有用函数
## contextmanager
装饰器，帮我们实现了__enter__方法，可以让我们方法使用with
```python
from contextlib import contextmanager
from time import sleep


@contextmanager
def test1():
    try:
        yield 'yield'
    finally:
        print('hello world')


with test1() as ex:
    print(ex)
    print("abcdefghijklmnopqrstuvwxyzxyzno you sese i can see my abc")
    sleep(10)

```