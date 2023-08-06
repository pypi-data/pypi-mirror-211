from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as fp:
    long_description = fp.read()

setup(name='minidevice',
      version='1.0.2',
      description='Android Auto Pypi',
      author='KateTseng',
      author_email='Kate.TsengK@outlook.com',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/NakanoSanku',
      license='MIT',
      keywords='game',
      project_urls={},
      packages=['minidevice'],
      install_requires=['opencv-python>=4.7.0.72', 'uiautomator2>=2.16.23','pyminitouch>=0.3.3'],
      python_requires='>=3'
     )
