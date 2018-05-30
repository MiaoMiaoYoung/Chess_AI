from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [Extension('socrates_ancientc', ['socrates_ancient.pyx',],),]

setup(
    name="socrates_ancientc",
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules
)