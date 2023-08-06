﻿import io
from os.path import abspath, dirname, join
from setuptools import find_packages, setup


HERE = dirname(abspath(__file__))
LOAD_TEXT = lambda name: io.open(join(HERE, name), encoding='UTF-8').read()
DESCRIPTION = '\n\n'.join(LOAD_TEXT(_) for _ in [
    'README.rst'
])

setup(
  name = 'pysortcsv',      
  packages = ['pysortcsv'], 
  version = '0.0.1',  
  license='MIT', 
  description = 'Learning by oattao123',
  long_description=DESCRIPTION,
  author = 'oattao123',                 
  author_email = 'dceriythrrmkic@gmail.com',     
  url = 'https://github.com/oattao123/pysortcsv',  
  download_url = 'https://github.com/oattao123/pysortcsv/archive/refs/tags/v0.0.1.zip',  
  keywords = ['py', 'sort', 'csv'],
  install_raquires=[
    'csv',
    'random'
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',     
    'Intended Audience :: Education',     
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)