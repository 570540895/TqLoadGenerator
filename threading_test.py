import threading


def func():
    print("func print")


def run():
    timer = threading.Timer(5, func)
    print("run print")
    timer.start()


if __name__ == '__main__':
    run()
