#!/usr/bin/env python3
from pyroscope import agent
from multiprocessing import Process
from threading import Thread
from time import sleep
import os
import signal
import threading


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
    print("Terminating pid: ", p.pid)
    os.kill(p.pid, signal.SIGTERM)


def start_workers():
    pr = []
    pr.append(Process(target=fast_function))
    pr.append(Process(target=slow_function))

    for p in pr:
        p.start()
        gpid = os.getpgid(p.pid)
        print("Started pid: ", p.pid, " gpid: ", gpid)
        threading.Thread(target=killer, args=(p, 10)).start()

    [p.join() for p in pr]


if __name__ == "__main__":
    main_pid = os.getpid()
    main_gpid = os.getpgid(main_pid)
    print("Main pid: ", main_pid, " gpid: ", main_gpid)

    p = Process(target=start_workers)
    p.start()
    print("Workers process pid: ", p.pid)

    ret = agent.start("test name", p.pid, "http://localhost:4040")
    print("agent.start() -> %d" % ret)

    p.join()
    ret = agent.stop(p.pid)
    print("agent.stop() -> %d" % ret)
