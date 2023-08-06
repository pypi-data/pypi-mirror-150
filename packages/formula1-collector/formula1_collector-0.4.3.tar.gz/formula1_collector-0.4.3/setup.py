from setuptools import setup

setup(
   name='formula1_collector',
   version='0.4.3',
   author='Ignasi Rovira',
   url='https://github.com/kithuto/formula-1-collector',
   packages=['formula1_collector'],
   license='MIT',
   description='A library for realtime formula 1 data',
   long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
   install_requires=[
       "pandas",
       "bs4",
       "lxml",
       'html5lib',
   ],
)