from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='serp_onpremise',
  version='0.1.1',
  author='astrotourist',
  author_email='d@orbl.io',
  description='Python API client for SERP on-premise API',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://serptech.ru',
  packages=find_packages(),
  classifiers=[
    'Programming Language :: Python :: 3.7',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  python_requires='>=3.7'
)