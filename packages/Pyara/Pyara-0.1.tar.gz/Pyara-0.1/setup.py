"""Metadata of package"""

from setuptools import setup, find_packages

setup(name='Pyara',
      version='0.1',
      url='https://github.com/Millcool/Pyara.git',
      license='MIT',
      author='Ilya Mironov',
      author_email='ilyamironov210202@gmail.com',
      description='Library for audio classification',
      packages=find_packages(exclude=['tests']),
      long_description=open('README.md').read(),
      zip_safe=False)