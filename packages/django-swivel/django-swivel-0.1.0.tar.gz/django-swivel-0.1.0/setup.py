'''
Created on 11/05/2022

@author: Yasir O Atabani
'''

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='django-swivel',
      version="0.1.0",
      author='Yasir O. Atabani',
      author_email='yasiratabani@gmail.com',
      url='http://yatabani.com/django-swivel/',
      packages=['swivel']
)
