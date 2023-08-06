import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='colaquant',
    version='0.0.2',
    description='可乐的量化分析框架',
    author='Cola Li',
    author_email='Indigocola121@gmail.com',
    long_description=long_description,
    long_description_content_type = "text/markdown",
    url = 'https://pypi.org/project/colaquant/',
    packages=['colaquant']
)