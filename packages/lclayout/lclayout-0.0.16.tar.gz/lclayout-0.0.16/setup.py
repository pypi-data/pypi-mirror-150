# Copyright 2019-2020 Thomas Kramer.
# SPDX-FileCopyrightText: 2022 Thomas Kramer
#
# SPDX-License-Identifier: CERN-OHL-S-2.0

from setuptools import setup, find_packages


def readme():
    with open("README.md", "r") as f:
        return f.read()


setup(name='lclayout',
      version='0.0.16',
      description='CMOS standard cell layout generator.',
      long_description=readme(),
      long_description_content_type="text/markdown",
      keywords='cmos cell generator layout klayout vlsi asic',
      classifiers=[
          # 'License :: OSI Approved :: GNU Affero General Public License v3',
          'Development Status :: 3 - Alpha',
          'Topic :: Scientific/Engineering',
          'Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)',
          'Programming Language :: Python :: 3'
      ],
      url='https://codeberg.org/librecell/lclayout',
      author='T. Kramer',
      author_email='code@tkramer.ch',
      license='OHL-S v2.0',
      packages=find_packages(),
      package_data={'': ['examples/*']},
      entry_points={
          'console_scripts': [
              'lclayout = lclayout.standalone:main',
              # 'drc_cleaner = lclayout.drc_cleaner.standalone:main',
          ]
      },
      install_requires=[
          'librecell-common>=0.0.9',
          'toml==0.10.*',
          'klayout>=0.27.3',  # GPLv3, minimum of 0.27.3 because of case-sensitive netlists.
          'numpy==1.*',  # BSD
          'networkx==2.*',  # BSD
          'scipy>=1.5.*',  # BSD
          'liberty-parser>=0.0.10',  # GPLv3
          'pysmt==0.9.*',  # Apache-2.0
          'z3-solver==4.8.*',  #
      ],
      zip_safe=False)
