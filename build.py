#!/usr/bin/env python3
# encoding: utf-8

import os
import shutil
from distutils.core import Extension, Distribution
from distutils.command.build_ext import build_ext


ext_modules = [Extension("pyroscope_io.agent", sources=["agent.c"], extra_objects=[
    "libpyroscope.pyspy.a", "librustdeps.a"])]


def build():

    distribution = Distribution(
        {'name': 'pyroscope_io', 'ext_modules': ext_modules})

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

