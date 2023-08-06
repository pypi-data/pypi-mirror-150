# -*- coding: utf-8 -*-
"""
@File        : setup.py
@Author      : yu wen yang
@Time        : 2022/4/28 2:43 下午
@Description :
"""
import setuptools

setuptools.setup(
    name="django-simple-department",
    version="0.1.1",
    author="yuwenyang",
    author_email="ywyhpnn@126.com",
    description="一个测试的包",
    long_description="一个特别长的描述",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(exclude=[
        "manage.py", "django_simple_departments", "django_simple_departments.*", 't', 't.*'
    ]),
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    install_requires=[],
    python_requires=">=3"
)