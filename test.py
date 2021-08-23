import os
from pyroscope_io import agent
import random
import time

pid = os.getpid()
agent.start("test.python.app", "http://localhost:4040", "", 100, 0, "debug")
print(f"build_summary {agent.build_summary()}")
agent.set_logger_level(5)

print(f"original process {pid}")
ret = os.fork()
print(f"fork {ret}")

def work(n):
	i = 0
	while i < n:
		i += 1


def fast_function():
	agent.set_tag("work", "fast")
	work(20000)
	agent.set_tag("work", "")


def slow_function():
	agent.set_tag("work", "slow")
	work(80000)
	agent.set_tag("work", "")


while True:
	r = random.random()
	if r < 0.5:
		print(f"pid {os.getpid()}")
		time.sleep(random.random())
	elif r < 0.5:
		fast_function()
	else:
		slow_function()
