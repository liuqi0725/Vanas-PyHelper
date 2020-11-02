from setuptools import setup, find_packages


with open('requirements.txt') as f:
    deps = [dep for dep in f.read().split('\n') if dep.strip() != '']
    install_requires = deps

with open('README.rst') as f:
    DESC = f.read()

setup(name='VanasPyHelper',
      version="0.2",
      description="Vanas py 通用核心帮助工具包",
      long_description=DESC,
      packages=find_packages(),
      zip_safe=False,
      include_package_data=True,
      install_requires=install_requires)
