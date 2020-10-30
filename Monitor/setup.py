# -*- coding: utf-8 -*-

"""
Example of how to use setuptools
"""

__version__ = "1.0.0"

from setuptools import setup, find_packages


# Read description from README file.
def long_description():
    from os import path
    this_directory = path.abspath(path.dirname(__file__))
    with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
        return f.read()


def get_depends():
    with open('requirements.txt') as f:
        return f.read().splitlines()


# 使用 unittest 测试框架
import unittest
def get_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite


setup(
    author='Jeff Wang',
    author_email='jeffwji@test.com',
    name="devops_monitor",
    long_description=long_description(),

    # 命令行："python setup.py --version" 可以获得版本号。
    version=__version__,
    
    ### 指定或排除目录或模块：
    # find_package 想限制查找的访问，以下表示查找除了 tests 和 test 目录之外的所有其他目录下的项目文件。
    packages=find_packages(
        exclude=['tests', 'test']
    ),
    # 也可以直接指定只打包某些目录
    #   packages=['submodule1', 'submodule2']
    # 但是不会包含 module1/submoduleA 和 module/submoduleB。如果要包含其下子目录，需要改成:
    #   packages=find_packages()，或明确罗列每一个 submodule 的路径。
    #
    ### 打包格式：
    # 1）wheel 格式（推荐格式，需要安装 `pip install twine`）：
    # 打包命令：`python setup.py egg_info -bDEV bdist_wheel rotate -m.egg -k3`
    # 打包文件名：{dist}-{version}(-{build})?-{python_version}-{abi}-{platform}.whl
    #
    # 或 egg 格式（easy_install 格式）
    # 打包命令：`python setup.py egg_info -bDEV bdist_egg rotate -m.egg -k3`
    #
    # `egg_info` 参数打印出打包信息。
    # wheel 只打包 py 文件，如果希望加入其他文件，需要以下配置：
    #
    # `package_data` 用于将`子模块/子目录`（注意必须是`子模块/子目录`，既不能用于项目根，也不能用于`子目录`，或`子目录/子目录`下的文件）下的非代码文件。
    # 它主要用于模块内部数据的打包，文件最终被安装到 `site` 目录下，可以通过访问模块路径取得。
    #
    # `data_files` 可以包含任意路径，包括根目录下的额外数据文件。它主要用于需要根据安装环境修改的文件，比如配置信息适合以模块方式打包的
    data_files=[
        # 参数格式: (打包文件中的目录名称 , [源代码中的路径])。
        ('conf', ['conf/config.properties']),
    ],
    # wheel 格式中这些文件将被打包到 `[package]/<package_name-version>.data/data/` 路径下，比如将 `conf/conf.properties` 打包到
    # `[package]/<package_name-version>.data/data/conf/config.properties`。路径中的 `conf` 由 tuple 中第一个元素指定。
    #
    # egg 文件中文件被直接打包到包根目录的 `/conf/config.properties`，目录中的 `conf` 由 tuple 中的第一个元素指定。
    #
    # pip install 将数据（非模块）文件安装到 `$PYTHONPATH/conf/config.properties` 目录下。路径中的 `conf` 由 tuple 的第一个元素指定。
    #
    # pip 可以安装 wheel 格式但是不能安装 egg 文件。egg 通过 `python -m easy_install dist/xxx.egg` 来安装。
    #
    # 2）tar.gz 格式
    # 打包命令：`python setup.py egg_info -bDEV sdist rotate -m.egg -k3`
    #
    # `MANIFEST.in` 用于配置需要被打包的文件，可以指定任意文件，比如 项目根目录下的文件 README.md 等。
    #
    # MANIFEST.in 不工作于 wheel 等格式。它只对 sdist 打包参数生效。数据（非模块）文件安装到 `.venv/conf/conf.properties` 目录下。
    #

    install_requires=get_depends(),

    # python setup.py test
    test_suite='setup.get_test_suite',
)
