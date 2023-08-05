#!/usr/bin/env python3

# Set this to True to enable building extensions using Cython.
# Set it to False to build extensions from the C file (that
# was previously created using Cython).
# Set it to 'auto' to build with Cython if available, otherwise
# from the C file.
import sosecrets_core
from setuptools import Extension
from setuptools import setup
import sys
USE_CYTHON = 'auto'

# THE TRICK IS CANNOT HAVE `__init__.py` FILES IN `SOSECRETS_CORE`!!!
# BETTER TO COMPILE USING CYTHON TO C THEN LINK EXTENSIONS WITH SETUPTOOLS

if USE_CYTHON:
    try:
        from Cython.Distutils import build_ext
        from Cython.Build import cythonize
    except ImportError:
        if USE_CYTHON == 'auto':
            USE_CYTHON = False
        else:
            raise

cmdclass = {}
ext_modules = []

if sys.version_info[0] == 2:
    raise Exception('Python 2.x is no longer supported')

if USE_CYTHON:
    ext_modules += [
        Extension("sosecrets_core.secrets", ["sosecrets_core/secrets.pyx"]),
    ]
    cmdclass.update({'build_ext': build_ext})
else:
    ext_modules += [
        Extension("sosecrets_core.secrets", ["sosecrets_core/secrets.c"]),
    ]

setup(
    name='sosecrets_core',
    version="1.0.4",
    description='Simple Secret Primitive for Python',
    author='Jim Chng',
    author_email='jimchng@outlook.com',
    url='http://github.com/jymchng/sosecrets-core',
    packages=['sosecrets_core'],
    package_dir={
        'sosecrets_core': 'sosecrets_core',
    },
    cmdclass=cmdclass,
    ext_modules=ext_modules,

    long_description=open('README.md').read(),

    license="MIT",
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Cython",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
    ],
    keywords='secrets security secrets-management',
)
