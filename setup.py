# flake8: noqa: E501
from setuptools import setup, find_packages

VERSION = "0.1.1"
DESCRIPTION = "Working with opencv can be quite a hussel, a lot of boiler code, nested functions for specific use cases, this package is designed to make it easier to work with opencv, while focusing on the main task in hand. best for prototyping and quick testing. second part is speed and performance, this package is designed to be fast and efficient."

setup(
    name="opencv_wrap",
    version=VERSION,
    description=DESCRIPTION,
    long_description=open("README.rst").read(),
    url="https://github.com/rishi23root/opencv_wrap",
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
    install_requires=['absl-py>=2.1.0', 'attrs>=23.2.0', 'cffi>=1.16.0', 'contourpy>=1.2.1', 'cycler>=0.12.1', 'filelock>=3.13.4', 'flatbuffers>=24.3.25', 'fonttools>=4.51.0', 'fsspec>=2024.3.1', 'jax>=0.4.26', 'jaxlib>=0.4.26', 'Jinja2>=3.1.3', 'kiwisolver>=1.4.5', 'MarkupSafe>=2.1.5', 'matplotlib>=3.8.4', 'mediapipe>=0.10.11', 'ml-dtypes>=0.4.0', 'mpmath>=1.3.0', 'networkx>=3.3', 'numpy>=1.26.4', 'nvidia-cublas-cu12>=12.1.3.1', 'nvidia-cuda-cupti-cu12>=12.1.105', 'nvidia-cuda-nvrtc-cu12>=12.1.105', 'nvidia-cuda-runtime-cu12>=12.1.105', 'nvidia-cudnn-cu12>=8.9.2.26', 'nvidia-cufft-cu12>=11.0.2.54', 'nvidia-curand-cu12>=10.3.2.106', 'nvidia-cusolver-cu12>=11.4.5.107', 'nvidia-cusparse-cu12>=12.1.0.106', 'nvidia-nccl-cu12>=2.19.3', 'nvidia-nvjitlink-cu12>=12.4.127', 'nvidia-nvtx-cu12>=12.1.105', 'opencv-contrib-python>=4.9.0.80', 'opencv-python>=4.9.0.80', 'opt-einsum>=3.3.0', 'packaging>=24.0', 'pillow>=10.3.0', 'protobuf>=3.20.3', 'pycparser>=2.22', 'pyparsing>=3.1.2', 'python-dateutil>=2.9.0.post0', 'scipy>=1.13.0', 'six>=1.16.0', 'sounddevice>=0.4.6', 'sympy>=1.12', 'torch>=2.2.2', 'triton>=2.2.0', 'typing_extensions>=4.11.0'],
    zip_safe=False,
)
