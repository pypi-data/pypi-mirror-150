from setuptools import setup

# Setting up
setup(
    name="dateconfig",
    version='1.1',
    author="Python Wiz",
    author_email="pydatepackage@gmail.com",
    description="Format date",
    packages=['dateconfig'],
    install_requires=['openpyxl', 'pygsheets'],
    zip_safe=False
  
)