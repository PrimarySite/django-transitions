import os
import sys

from setuptools import find_packages
from setuptools import setup

version = '0.1'

setup(name='django_transitions',
      version=version,
      description="Integrate pytransitions with Django.",
      long_description=(open("README.rst").read() + "\n"),
      classifiers=[
          'Framework :: Django',
          'Framework :: Django :: 1.11',
          'Framework :: Django :: 2.0',
          'Framework :: Django :: 2.2',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: BSD License',
      ],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='django permission restframework',
      author='Christian Ledermann',
      author_email='christian.ledermann@gmail.com',
      url='https://github.com/PrimarySite/django-transitions',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'Django',
          'transitions',
      ],
      entry_points="""
        # -*- Entry points: -*-
        """,
      )
