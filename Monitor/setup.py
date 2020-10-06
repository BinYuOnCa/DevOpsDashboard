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


# 安装 dependenices. 因为 bug 的原因, 需要将 url 分开处理，分别传给 `install_requires` 和 `dependency_links`
def get_depends():
    with open('requirements.txt') as f:
        return f.read().splitlines()

# 使用 unittest 测试框架
import unittest
def get_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite


# 可以在安装前检查依赖的版本，并自动升级到最新版(依赖必须发布到 pipy 中，否则会因为无法找到而出错)：
# autoupgrade 0.2.0 之后才支持 master, 需要手工安装：pip install https://bitbucket.org/jorkar/autoupgrade/get/master.tar.gz --trusted-host=bitbucket.org
# 或python -m pip install git+https://bitbucket.org/jorkar/autoupgrade.git@master#autoupgrade-0.2.0 --trusted-host=bitbucket.org
#from autoupgrade import AutoUpgrade
#AutoUpgrade("CodeRepositoryServices", index="https://localhost:9090/pypi").upgrade_if_needed()

# 打包前执行 `git tag -a $(python setup.py --version)`　将 __version__ 注册为 tag number
setup(
    author='Jeff Wang',
    author_email='jeffwji@test.com',
    name="devops_monitor",
    long_description=long_description(),

    # 命令行："python setup.py --version" 可以获得版本号。
    version=__version__,
    #version_command='git describe --always --long --dirty=-dev',  # 3) 获得　tag 动态获得版本号(参考文档 <git release flow>)
    # `--always` 如果没有打过标签会出现错误信息 `fatal: No names found, cannot describe anything.`，这个参数将返回 commit hash number 代替 tag 以避免错误.
    # `--long --dirty=-dev` 获得长格式版本信息： <version>-<times>-<commit-hash>-<dirty> 例如：0.0.2-0-g00bd0b4-dev

    ########
    ## 数据文件打包规则
    #
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
    #package_data={
    #    # 模块（含有 __init__.py 文件）下的 conf 子目录下的任何包中含有 .properties 的文件。
    #    'mymodule': ['conf/*.properties'],
    #},
    #include_package_data=True,
    #
    # `data_files`（推荐）可以包含任意路径，包括根目录下的额外数据文件。它主要用于需要根据安装环境修改的文件，比如配置信息，因此不适合以模块的方式打包。
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

    #
    test_suite='setup.get_test_suite',
)
