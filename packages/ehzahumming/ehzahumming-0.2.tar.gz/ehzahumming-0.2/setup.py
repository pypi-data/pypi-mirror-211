from setuptools import setup, find_packages

setup(
    name="ehzahumming",
    version="0.2",
    packages=find_packages(),
    description="A simple utility to generate humming sounds",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="ehzawad",
    author_email="ehzawad@gmail.com",
    url="https://github.com/ehzawad/ehzahumming",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
