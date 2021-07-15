#!/usr/bin/env python3
# encoding: utf-8

import os
import shutil
from distutils.core import Extension, Distribution
from distutils.errors import CCompilerError, DistutilsExecError, DistutilsPlatformError
from distutils.command.build_ext import build_ext

ext_modules = [Extension("pyroscope.agent", sources=["agent.c"], extra_objects=[
    "libpyroscope.pyspy.a", "librustdeps.a"])]


def build():

    distribution = Distribution(
        {'name': 'pyroscope', 'ext_modules': ext_modules})

    cmd = build_ext(distribution)
    cmd.ensure_finalized()
    cmd.run()

    # Copy built extensions back to the project
    for output in cmd.get_outputs():
        relative_extension = os.path.relpath(output, cmd.build_lib)
        shutil.copyfile(output, relative_extension)
        mode = os.stat(relative_extension).st_mode
        mode |= (mode & 0o444) >> 2
        os.chmod(relative_extension, mode)


if __name__ == '__main__':
    build()

