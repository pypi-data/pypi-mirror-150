import setuptools
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name = 'invoiceJB',
    version = '0.1.0',
    author = 'JamesBang',
    author_email = 'JBProgramNotes@gmail.com',
    description = 'Taiwan invoice number',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url = 'https://github.com/JBProgramNotes/invoiceJB',
    packages=setuptools.find_packages(),
    keywords = ['invoice'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
