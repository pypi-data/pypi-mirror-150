# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# This call to setup() does all the work
setup(
    name="ldn-serializer",
    version="0.1.0",
    description="Demo library",
    long_description="Serializer of python objects",
    long_description_content_type="text/markdown",
    url="https://medium-multiply.readthedocs.io/",
    author="leinadalien",
    author_email="danila.box@tut.by",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=["ldn_serializer"],
    include_package_data=True
)