# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name = 'longPolling',
    version = '0.0.4',
    keywords = ['long polling',"flask","http","thread"],
    description = 'Simple long polling implementation',
    long_description = open("README.rst","r",encoding="utf-8").read(),
    author = 'kuankuan',
    author_email = '2163826131@qq.com',
    url="https://kuankuan2007.gitee.io/docs/long-polling/",
    install_requires = [
        'requests',
        'flask',
        'rsa'
    ],
    packages = ['longPolling'],
    
    license = 'Mulan PSL v2',
    platforms=[
        "windows",
        "linux",
        "macos"
    ] ,
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'License :: OSI Approved :: Mulan Permissive Software License v2 (MulanPSL-2.0)'
    ]
)
