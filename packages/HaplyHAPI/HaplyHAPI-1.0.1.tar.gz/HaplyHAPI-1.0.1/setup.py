from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='HaplyHAPI',
    version='1.0.1',
    install_requires=[
        'pyserial',
    ],
    author="Antoine Weill--Duflos (Haply Robotics)",
    author_email="antoine@haply.co",
    description="Python implementation of the haply hAPI",
    long_description=long_description,
    long_description_content_type="text/markdown",

)
