from setuptools import find_packages, setup


setup(name='kubectl-prettylogs-wrapper',
      version='1.0',
      description='Wrapper for kubectl logs command to print pretty logs and stacktrace',
      author='Aldo Gonzalez',
      author_email='aldo.gonzalez@dummy.com',
      url='https://www.dummy.org/pending/',
      packages=find_packages(exclude=["tests"]),
      )