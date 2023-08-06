# This file is placed in the Public Domain.
# pylint: disable=C0114,C0116,W1514


from setuptools import setup


def read():
    return open("README.rst", "r").read()


setup(
    name="nopaths",
    version="5",
    author="No Paths <nopaths@proton.me>",
    author_email="nopaths@proton.me",
    url="http://github.com/nopaths/nopaths",
    zip_safe=True,
    description="there are no paths",
    long_description=read(),
    long_description_content_type="text/x-rst",
    license="Public Domain",
    packages=[
              "nopaths",
              'nopaths.modules'
             ],
    scripts=["bin/nopaths"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: Public Domain",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
     ],
)
