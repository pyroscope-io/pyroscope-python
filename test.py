import os
import pyroscope_io as pyroscope
import random
import time


def work(n):
    i = 0
    while i < n:
        i += 1


def fast_function():
    with pyroscope.tag_wrapper({ "function": "fast" }):
        work(20000)


def slow_function():
    pyroscope.tag({ "function": "slow" })
    work(80000)
    pyroscope.remove_tags("function")


if __name__ == "__main__":
    pyroscope.configure(
        app_name          = "test.python.app",
        server_address    = "http://localhost:4040",
        sample_rate       = 100,
        with_subprocesses = True,
        log_level         = "debug"
    )

    pyroscope.tag({
        "container_id": "123",
    })

    print(f"build_summary {pyroscope.build_summary()}")

    while True:
        r = random.random()
        if r < 0.5:
            fast_function()
        else:
            slow_function()
