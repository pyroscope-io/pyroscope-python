#!/usr/bin/env python3
# encoding: utf-8

import os
import shutil
import platform
from distutils.core import Extension, Distribution
from distutils.command.build_ext import build_ext


ext_modules = [Extension("pyroscope.agent", sources=["agent.c"], extra_objects=[
    "libpyroscope.pyspy.a", "librustdeps.a"])]


def run(str):
    res = os.system(str)
    if res != 0:
        raise Exception(f"Failed to run {str}")

def build(_):
    distribution = Distribution(
        {'name': 'pyroscope', 'ext_modules': ext_modules})
    arch = 'amd64' if platform.machine().lower() == 'x86_64' else 'arm64'
    os_name = 'linux' if platform.system().lower() == 'linux' else 'mac'

    if os.getenv("PYROSCOPE_PYTHON_LOCAL"):
        print("PYROSCOPE_PYTHON_LOCAL yes")
        run(f"cd ../pyroscope && make build-rust-dependencies-docker")
        run(f"cp ../pyroscope/out/libpyroscope.pyspy.a libpyroscope.pyspy.a")
        run(f"cp ../pyroscope/out/libpyroscope.pyspy.h libpyroscope.pyspy.h")
        run(f"cp ../pyroscope/out/librustdeps.a librustdeps.a")
    else:
        pyroscope_libs_sha = "df45c48"
        # TODO: improve this logic
        prefix = f"https://dl.pyroscope.io/static-libs/{pyroscope_libs_sha}/{os_name}-{arch}"
        run(f"rm -f libpyroscope.pyspy.a libpyroscope.pyspy.h librustdeps.a")
        run(f"wget -nc {prefix}/libpyroscope.pyspy.a -O libpyroscope.pyspy.a")
        run(f"wget -nc {prefix}/libpyroscope.pyspy.h -O libpyroscope.pyspy.h")
        run(f"wget -nc {prefix}/librustdeps.a -O librustdeps.a")

    cmd = build_ext(distribution)
    cmd.ensure_finalized()
    cmd.run()

    # As we are building manually, the output is not automatically placed in proper
    # directory, therefore we have to move it there. Otherwise it would not end up
    # in final package.
    for output in cmd.get_outputs():
        relative_extension = os.path.relpath(output, cmd.build_lib)
        shutil.copyfile(output, relative_extension)
        mode = os.stat(relative_extension).st_mode
        mode |= (mode & 0o444) >> 2
        os.chmod(relative_extension, mode)


if __name__ == '__main__':
    build()

