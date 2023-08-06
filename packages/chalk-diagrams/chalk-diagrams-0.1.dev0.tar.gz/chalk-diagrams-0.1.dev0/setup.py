from distutils.core import setup

setup(
    name="chalk-diagrams",
    version="0.1dev",
    packages=[
        "chalk",
    ],
    description="A declarative drawing API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Dan Oneață",
    author_email="dan.oneata@gmail.com",
    url="https://github.com/danoneata/chalk",
)
