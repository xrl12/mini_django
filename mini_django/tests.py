from threading import Thread
import signal
import sys

IS_CLOSE = False


def is_exit():
    global IS_CLOSE
    return IS_CLOSE


def worker(task):
    while True:
        if is_exit():
            print("exit ......")
            return


def handler_sigterm(*args):
    global IS_CLOSE
    IS_CLOSE = True


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, handler_sigterm)
    thread1 = Thread(target=worker, args='1')
    thread1.start()
    thread1.join(10)
