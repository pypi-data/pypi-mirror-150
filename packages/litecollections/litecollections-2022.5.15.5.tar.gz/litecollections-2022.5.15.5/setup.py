from __future__ import print_function
from distutils.core import setup
import sys, os, setuptools

# base settings
version = '2022.5.15.5'
name = 'litecollections'

# find the modules in this repo
packages = setuptools.find_packages()

# sanity check that packages looks right
assert name in packages, [name, packages]  # if package name doesnt show up, something is wrong

# base packages required to install this
required_packages = []

# if $TEST_TOOLS env var is '1' add hypothesis to the required packages
if 'TEST_TOOLS' in os.environ and os.environ['TEST_TOOLS'] == '1':
  required_packages.append('hypothesis')

# main setup command
setup(
  name = name,
  version = version,
  packages = packages,
  license = open('LICENSE','r').read(),
  install_requires = required_packages,
  zip_safe=True,
  description = 'python collections except its all backed by sqlite',
  author = 'Cody Kochmann',
  author_email = 'kochmanncody@gmail.com',
  maintainer = 'Cody Kochmann',
  maintainer_email = 'kochmanncody@gmail.com',
  url = 'https://github.com/CodyKochmann/litecollections',
  download_url = 'https://github.com/CodyKochmann/litecollections/tarball/{}'.format(version),
  keywords = ['sqlite', 'collections', 'persistent', 'performance', 'scale', 'datascience', 'acid', 'database'],
  classifiers = []
)
