from setuptools import find_packages, setup

with open('README.md', 'r', encoding='utf-8') as fp:
    long_description = fp.read()

setup(name='gameauto',
      version='1.0.4',
      description='Android Game Auto Pypi',
      author='KateTseng',
      author_email='Kate.TsengK@outlook.com',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/NakanoSanku',
      license='MIT',
      keywords='game',
      project_urls={},
      packages=find_packages(),
      include_package_data=True,
      install_requires=['minidevice>=1.0.4','ncnn>=1.0.20230517'],
      python_requires='>=3'
      )
