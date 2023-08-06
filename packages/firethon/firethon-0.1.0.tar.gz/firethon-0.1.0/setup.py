import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / 'README.md').read_text()

setup(
    name="firethon",
    version="0.1.0",
    description="A simple API wrapper for firebase",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/dalerzafarovich/firethon",
    author="Daler Sattarov",
    author_email="zdaler014@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["firethon"],
    include_package_data=True,
    install_requires=["requests", "google-auth"]
)
