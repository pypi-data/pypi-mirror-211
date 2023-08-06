from setuptools import setup, find_packages

setup(
    name='ox_script',
    version='2.0.0',
    author='Postek Electronics Co., Ltd.',
    author_email='support@postek.com.cn',
    packages=find_packages(),
    license="MIT",
    description="The ox_script details offically supported APIs. The printer have a version of ox_script on the printer with all functions fully implemented.\nMost printer specific functions are left blank intentionally as they are meant to be executed on the printer and will throw an error if called on your devices. This file is provided more so for the beneift of keeping your IDE of choice happy while programming, providing extensive comments on the different functions and allowing for easy install through pip. ",
    url="https://github.com/POSTEK-OX-Script",
    install_requires=[
        "pandas",
        "openpyxl",
    ],
)
