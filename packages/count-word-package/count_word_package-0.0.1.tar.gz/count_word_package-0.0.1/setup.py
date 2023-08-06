import setuptools


with open("README.md", "r") as fh:
    description = fh.read()

setuptools.setup(
    name="count_word_package",
version="0.0.1",
author="Ken mwangi",
author_email="contact@kenmwangi.com", 
packages=["count_word_package"],
description="Word Count using Counter collections function package",
long_description=description,
long_description_content_type="text/markdown",
url="https://github.com/kenmwangi/count-word",
license="MIT",
python_requires=">=3.8",
install_requires=[]
)