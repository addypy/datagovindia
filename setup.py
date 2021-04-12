from setuptools import setup, find_packages
from os import path

directory = path.abspath(path.dirname(__file__))

with open(path.join(directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="datagovindia",
    version='0.1',
    author='Aditya Karan Chhabra',
    author_email='aditya0chhabra@gmail.com',
    packages=find_packages(include=['datagovindia', 'datagovindia.*'],exclude=['data','.*gz']),
    scripts=['datagovindia/__init__.py','datagovindia/util.py'],
    url='http://github.com/addypy/datagovindia/',
    license='LICENSE.txt',
    description="A Python API-wrapper for Government of India’s Open Government Data OGD platform",
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',        
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        "Programming Language :: Python :: 3.9",
        "Natural Language :: English",
        "Operating System :: OS Independent",        
    ],   
    keywords='opendata ogd ogd-india opendataindia datagovin datagovindia india india-data indiadata',
    install_requires=[
           "requests",
            "numpy",
            "pandas"
                ],
)