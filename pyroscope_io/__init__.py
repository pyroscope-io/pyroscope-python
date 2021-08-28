from pyroscope_io import _agent


class PyroscopeError(Exception):
    pass


class Config:
    def __init__(self, app_name, server_address, auth="", sample_rate=100, with_subprocesses=0, log_level="debug"):
        self.app_name = app_name
        self.server_address = server_address
        self.auth = auth
        self.sample_rate = sample_rate
        self.with_subprocesses = with_subprocesses
        self.log_level = log_level
        self.started = False


__config = None


def configure(c):
    assert isinstance(c, Config)
    global __config
    __config = c


def __is_started():
    global __config
    return __config.started


def __set_started(started):
    global __config
    __config.started = started


def __set_name(name):
    global __config
    __config.app_name = name


def start():
    if isinstance(__config, type(None)):
        raise PyroscopeError("Not configured!")

    if __is_started():
        raise PyroscopeError("Already started!")

    if _agent.start(__config.app_name, __config.server_address, __config.auth,
                    __config.sample_rate, __config.with_subprocesses, __config.log_level):
        raise PyroscopeError()

    __set_started(True)


def stop():
    if not __is_started():
        raise PyroscopeError("Not started!")

    if _agent.stop():
        raise PyroscopeError()

    __set_started(False)


def change_name(name):
    if not __is_started():
        raise PyroscopeError("Not started!")

    __set_name(name)
    if _agent.change_name(__config.app_name):
        raise PyroscopeError()


def set_tag(key, value):
    if not __is_started():
        raise PyroscopeError("Not started!")

    if _agent.set_tag(key, value):
        raise PyroscopeError()


def build_summary():
    return _agent.build_summary()


def test_logger():
    if _agent.test_logger():
        raise PyroscopeError()


def set_logger_level(level):
    if _agent.set_logger_level(level):
        raise PyroscopeError()
