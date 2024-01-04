from asgiref.sync import iscoroutinefunction
from functools import partial
import asyncio
import inspect


async def test():
    pass


@asyncio.coroutine
def test_aa():
    pass


async def test_bb():
    pass


@inspect.markcoroutinefunction
def test_cc():
    pass


if __name__ == '__main__':
    a = iscoroutinefunction(test)
    print(a)
    print(iscoroutinefunction(test_aa))
    print(iscoroutinefunction(partial(test_bb)))
    print(iscoroutinefunction(test_cc))
