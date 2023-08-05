from distutils.command.build_ext import build_ext
from distutils.errors import CCompilerError, DistutilsExecError, DistutilsPlatformError

from setuptools import Extension, find_packages, setup

try:
    from Cython.Build import cythonize

    USE_CYTHON = True
except ImportError:
    USE_CYTHON = False
USE_CYTHON = False
print(USE_CYTHON)
ext = '.pyx' if USE_CYTHON else '.c'
print(ext)

extensions = [Extension("myscaledb._types", ["myscaledb/_types" + ext])]

if USE_CYTHON:
    extensions = cythonize(extensions, compiler_directives={'language_level': 3})


class BuildFailed(Exception):
    pass


# This class was copy/paced from
# https://github.com/aio-libs/aiohttp/blob/master/setup.py
class ve_build_ext(build_ext):
    # This class allows C extension building to fail.

    def run(self):
        try:
            build_ext.run(self)
        except (DistutilsPlatformError, FileNotFoundError):
            raise BuildFailed()

    def build_extension(self, ext):
        try:
            build_ext.build_extension(self, ext)
        except (CCompilerError, DistutilsExecError, DistutilsPlatformError, ValueError):
            raise BuildFailed()


def read(fname):
    with open(fname, encoding="utf8") as fp:
        content = fp.read()
    return content


setup_opts = dict(
    name='myscaledb-client',
    version='1.1.5',
    description='Myscale http client for python 3.6+',
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    author='zhuo chen',
    author_email='zhuoc@moqi.ai',
    packages=find_packages(exclude=('test*',)),
    package_dir={'myscaledb': 'myscaledb'},
    include_package_data=True,
    install_requires=[
        'sqlparse>=0.3.0',
        'aiodns>=3.0.0',
        'cchardet>=2.1.7',
        'aiobotocore[awscli]>=2.2.0' 'aiohttp>=3.0.1',
    ],
    license='MIT',
    url='https://github.com/moqi-ai/aiochclient',
    zip_safe=False,
    keywords='Myscale async python aiohttp',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    test_suite='tests',
    ext_modules=extensions,
    extras_require={
        # aiohttp client
        'aiohttp': ['aiohttp>=3.0.1'],
        'aiohttp-speedups': ['aiodns', 'cchardet', 'ciso8601>=2.1.1', 'aiohttp>=3.0.1'],
        # httpx client
        'httpx': ['httpx'],
        'httpx-speedups': ['ciso8601>=2.1.1', 'httpx'],
    },
    cmdclass=dict(build_ext=ve_build_ext),
)

try:
    setup(**setup_opts)
except BuildFailed:
    print("************************************************************")
    print("Cannot compile C accelerator module, use pure python version")
    print("************************************************************")
    del setup_opts['ext_modules']
    del setup_opts['cmdclass']
    setup(**setup_opts)
