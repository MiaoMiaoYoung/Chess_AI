from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [Extension('chessmodc', ['__init__.py',],), Extension('chessmodc.polyglot', ['polyglot.py',],)]

setup(
    name="chessmodc",
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules
)