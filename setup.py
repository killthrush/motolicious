from setuptools import setup, find_packages

setup(name='motolicious',
      version='0.0',
      description='Hack',
      long_description='Hackity Hack Hack',
      author='Ben Peterson',
      license='MIT',
      packages=find_packages(),
      package_data={
          '': ['*.json', '*.txt', '*.yml']
      })
