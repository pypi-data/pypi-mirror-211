from distutils.core import setup
import setuptools

packages = ['pyndjs']
setup(name='pyndjs',
      version='0.0.5',
      author='唐旭东',
      packages=packages,
      package_dir={'requests': 'requests'},
      install_requires=[
          "six"
      ])
