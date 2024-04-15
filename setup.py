# flake8: noqa: E501
from setuptools import setup, find_packages

VERSION = "0.0.5"
DESCRIPTION = "working with opencv can be quite a hussel, a lot of boiler code, nested functions for specific use cases, this package is designed to make it easier to work with opencv, while focusing on the main task in hand."

setup(
    name="opencv-wrap",
    version=VERSION,
    description=DESCRIPTION,
    long_description=open("README.rst").read(),
    url="https://github.com/rishi23root/opencv.util",
    author="rishi23root",
    author_email="rishi23root@gmail.com",
    license="MIT",
    include_package_data=True,
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    packages=find_packages(),
    install_requires=['absl-py>=2.1.0', 'attrs>=23.2.0', 'cffi>=1.16.0', 'contourpy>=1.2.0', 'cycler>=0.12.1', 'flatbuffers>=23.5.26', 'fonttools>=4.49.0', 'jax>=0.4.24', 'kiwisolver>=1.4.5', 'matplotlib>=3.8.3', 'mediapipe>=0.10.10', 'ml-dtypes>=0.3.2', 'numpy>=1.26.4', 'opencv-contrib-python>=4.9.0.80', 'opencv-python>=4.9.0.80', 'opt-einsum>=3.3.0', 'packaging>=23.2', 'pillow>=10.2.0', 'protobuf>=3.20.3', 'pycparser>=2.21', 'pyparsing>=3.1.1', 'python-dateutil>=2.8.2', 'scipy>=1.12.0', 'six>=1.16.0', 'sounddevice>=0.4.6'],
    zip_safe=False,
    entry_points={
        "console_scripts": ["pyresparser=pyresparser.command_line:main"],
    },
)
