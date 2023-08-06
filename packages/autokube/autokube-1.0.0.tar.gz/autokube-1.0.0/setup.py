from setuptools import setup, find_packages
from importlib_metadata import entry_points

setup(
    name="autokube",
    version="1.0.0",
    license='MIT',
    author_email='krishna.mishra@afourtech.com',
    description="Autokube package is a cli tool to automate kubernetes command via python",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    install_requires=['kubernetes','colorama'],
    author="Krishna Mishra",
    packages=find_packages(),
    scripts=['bin/autokube']
)
