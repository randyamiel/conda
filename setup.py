﻿#!/usr/bin/env python
# (c) 2012-2014 Continuum Analytics, Inc. / http://continuum.io
# All Rights Reserved
#
# conda is distributed under the terms of the BSD 3-clause license.
# Consult LICENSE.txt or http://opensource.org/licenses/BSD-3-Clause.

import sys
import os

if 'develop' in sys.argv:
    from setuptools import setup
    using_setuptools = True
    print("Using setuptools")
else:
    from distutils.core import setup
    using_setuptools = False
    print("Not using setuptools")

from distutils.command.install import install as _install

import versioneer


if sys.version_info[:2] < (2, 7) or sys.version_info > (3, 0) and sys.version_info < (3, 3):
    sys.exit("conda is only meant for Python 2.7 or 3.3 and up.  current version: %d.%d" % sys.version_info[:2])

try:
    if os.environ['CONDA_ACTIVE_ENV']:
        # Try to prevent accidentally installing conda into a non-root conda environment
        sys.exit("You appear to be in a non-root conda environment. Conda is only "
            "supported in the root environment. Deactivate and try again. If you believe "
            "this message is in error, run CONDA_ACTIVE_ENV='' python setup.py.")
except KeyError:
    pass

versioneer.versionfile_source = 'conda/_version.py'
versioneer.versionfile_build = 'conda/_version.py'
versioneer.tag_prefix = '' # tags are like 1.2.0
versioneer.parentdir_prefix = 'conda-' # dirname like 'myproject-1.2.0'


if sys.platform == 'win32' and using_setuptools:
    kwds = {'entry_points': {"console_scripts":
                            ["conda = conda.cli.main:main"]},
            'scripts':  ['bin\\activate.bat', 'bin\\deactivate.bat'],
            }

    def _post_install(dir):
        from subprocess import call
        for script in ("activate.bat", "deactivate.bat"):
            call(["unix2dos", os.path.join(sys.prefix, "Scripts", script)],)

    class install(_install):
        def run(self):
            _install.run(self)
            self.execute(_post_install, (self.install_lib,),
                        msg="Converting UNIX line endings to Windows")
    cmdclass = {"install": install, "develop": install}
else:
    kwds = {'scripts': ['bin/conda', 'bin/activate', 'bin/deactivate'], }
    cmdclass = {}


setup(
    name="conda",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass().update(cmdclass),
    author="Continuum Analytics, Inc.",
    author_email="ilan@continuum.io",
    url="https://github.com/conda/conda",
    license="BSD",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
    ],
    description="package management tool",
    long_description=open('README.rst').read(),
    packages=['conda', 'conda.cli', 'conda.progressbar'],
    install_requires=['pycosat', 'pyyaml', 'requests'],
    **kwds
)
