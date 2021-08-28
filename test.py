import os
import pyroscope_io as pyro
import random
import time


def work(n):
    i = 0
    while i < n:
        i += 1


def fast_function():
    pyro.set_tag("work", "fast")
    work(20000)
    pyro.set_tag("work", "")


def slow_function():
    pyro.set_tag("work", "slow")
    work(80000)
    pyro.set_tag("work", "")


if __name__ == "__main__":

    pid = os.getpid()
    pyro.configure(pyro.Config("test.python.app",
                   "http://localhost:4040", "", 100, int(True), "debug"))

    pyro.start()
    print(f"build_summary {pyro.build_summary()}")
    pyro.set_logger_level(5)

    print(f"original process {pid}")
    ret = os.fork()
    print(f"fork {ret}")

    while True:
        r = random.random()
        if r < 0.5:
            print(f"pid {os.getpid()}")
            time.sleep(random.random())
        elif r < 0.5:
            fast_function()
        else:
            slow_function()
