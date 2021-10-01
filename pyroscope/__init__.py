from collections import namedtuple
from contextlib import contextmanager

from pyroscope import agent

Config = namedtuple('Config', ('app_name', 'server_address',
                    'auth_token', 'sample_rate', 'with_subprocesses', 'log_level'))


class PyroscopeError(Exception):
    pass


def configure(app_name, server_address, auth_token="", sample_rate=100, with_subprocesses=0, log_level="debug", tags=None):
    agent.start(app_name, server_address, auth_token, sample_rate, int(with_subprocesses), log_level)
    if tags is not None:
        tag(tags)


def stop():
    agent.stop()


def change_name(name):
    agent.change_name(name)


@contextmanager
def tag_wrapper(tags):
    for key, value in tags.items():
        agent.set_tag(key, value)
    try:
        yield
    finally:
        for key in tags.keys():
            agent.set_tag(key, "")


def tag(tags):
    for key, value in tags.items():
        agent.set_tag(key, value)


def remove_tags(*keys):
    for key in keys:
        agent.set_tag(key, "")


def build_summary():
    return agent.build_summary()


def test_logger():
    agent.test_logger()
