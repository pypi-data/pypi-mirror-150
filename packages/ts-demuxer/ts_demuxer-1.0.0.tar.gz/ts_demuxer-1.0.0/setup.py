from distutils.core import setup
from setuptools import find_packages

with open('README.rst', 'r', encoding='u8') as f:
    long_description = f.read()

setup(name='ts_demuxer',  # 包名
      version='1.0.0',  # 版本号
      description='ts demux',
      long_description_content_type="text/markdown",
      long_description=long_description,
      author='xuhx20',
      author_email='xuhx20@qq.com',
      url='https://gitee.com/xiao200/py_ts_demux.git',
      install_requires=[],
      license='BSD License',
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.8',
          'Topic :: Software Development :: Libraries'
      ],
      )
