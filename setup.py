# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

requires = ['Sphinx>=0.6', 'six']

setup(
    name='sphinxcontrib-documentedlist',
    version='0.5',
    url='https://github.com/chintal/sphinxcontrib-documentedlist',
    download_url='http://pypi.python.org/pypi/sphinxcontrib-documentedlist',
    license='BSD',
    author='Chintalagiri Shashank',
    author_email='shashank@chintal.in',
    description='Sphinx DocumentedList extension',
    long_description=read('README.rst'),
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Sphinx :: Extension',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    namespace_packages=['sphinxcontrib'],
)
