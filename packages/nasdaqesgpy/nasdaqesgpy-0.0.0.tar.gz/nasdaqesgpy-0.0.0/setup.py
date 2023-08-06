from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='nasdaqesgpy',
  description='This is a very basic library that would give internal users access to our scraping efforts.',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Viktor Aghajanyan',
  author_email='aghajanyanviktor@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='napp', 
  packages=find_packages(),
  install_requires=[''] 
)
