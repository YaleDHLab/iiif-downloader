from setuptools import setup
from os.path import join
import glob

setup (
  name='iiif_downloader',
  version='0.0.8',
  packages=['iiif_downloader'],
  keywords = ['iiif', 'image-data', 'api'],
  description='Download images from IIIF servers',
  url='https://github.com/yaledhlab/iiif-downloader',
  author='Douglas Duhaime',
  author_email='douglas.duhaime@gmail.com',
  license='MIT',
  install_requires=[
    'requests>=2.22.0',
  ],
)
