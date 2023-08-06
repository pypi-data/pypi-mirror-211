from setuptools import setup, find_packages

setup(
    name="loadtime",
    version="1.0.0",
    author="Tom Misawa",
    author_email="riversun.org@gmail.com",
    description="Package to display a progress bar for long processes with uncertain end times",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/riversun/LoadTime",
    packages=find_packages(exclude=["tests.*", "tests", "examples.*", "examples"]),
    tests_require=["pytest"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=[
    ]
)
