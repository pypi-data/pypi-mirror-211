from setuptools import setup

setup(
    name='HaplyHAPI',
    version='1.0.0',
    install_requires=[
        'pyserial',
    ],
    author="Antoine Weill--Duflos (Haply Robotics)",
    author_email="antoine@haply.co",
    description="Python implementation of the haply hAPI",
    long_description="This package provides a Python API for using with the haply 2diy and similar hardware, more info can be found at https://2diy.haply.co",

)