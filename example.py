#!/usr/bin/env python3
import os
import signal
import threading
from pyroscope import agent
from multiprocessing import Process
from threading import Thread
from time import sleep


def work(n):
    i = 0
    while i < n:
        i += 1


def fast_function():
    while True:
        work(25000)


def slow_function():
    while True:
        work(50000)


def killer(p, timeout):
    sleep(timeout)
    print(f"Terminating pid: {p.pid}")
    os.kill(p.pid, signal.SIGTERM)


def start_workers():
    pr = [Process(target=fast_function), Process(target=slow_function)]
    killers = []

    for p in pr:
        p.start()
        pgid = os.getpgid(p.pid)
        print(f"Started pid: {p.pid} pgid: {pgid}")
        k = threading.Thread(target=killer, args=(p, 10))
        k.start()
        killers.append(k)

    for p in pr:
        p.join()

    for k in killers:
        k.join()


if __name__ == "__main__":
    main_pid = os.getpid()
    main_pgid = os.getpgid(main_pid)
    print(f"Main pid: {main_pid} pgid: {main_pgid}")

    p = Process(target=start_workers)
    p.start()
    print(f"Workers process pid: {p.pid}")

    sample_rate = 100
    with_subprocesses = True
    auth_token = ""
    log_level = "debug"
    ret = agent.start("test_name", p.pid,
                      "http://localhost:4040", auth_token, sample_rate, int(with_subprocesses), log_level)
    print(f"agent.start() -> {ret}")
    if ret:
        exit(ret)

    ret = agent.change_name("new_test_name", p.pid)
    print(f"agent.change_name() -> {ret}")
    if ret:
        exit(ret)

    p.join()
    ret = agent.stop(p.pid)
    print(f"agent.stop() -> {ret}")
    if ret:
        exit(ret)
