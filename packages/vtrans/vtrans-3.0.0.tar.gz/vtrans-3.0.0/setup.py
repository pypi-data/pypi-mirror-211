from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Intended Audience :: End Users/Desktop',
  'License :: Freeware',
  'Operating System :: MacOS :: MacOS X',
  'Topic :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'Operating System :: Microsoft :: Windows :: Windows 8.1',
  'Operating System :: Microsoft :: Windows :: Windows 8',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python',
  'Programming Language :: Python :: 3.8'
]

setup(
  name='vtrans',
  version='3.0.0',
  description='This is a self-updating translator for free and unlimited usage with upto 130 langauges',
  long_description=open('README.md',"r",encoding="utf-8").read(),
  long_description_content_type='text/markdown',
  url='https://github.com/megalosVigneswaran/vtrans/tree/main/vtrans',  
  author='S.Vigneswaran',
  author_email='t896242@gmail.com',
  license='MIT',
  classifiers=classifiers,
  keywords=['translator', 'googletranslate', 'self-updating', 'googletrans','vtrans'],
  packages=find_packages(),
  package_data={
        'vtrans': ['config.txt'],
    },
  install_requires=['googletrans==3.1.0a0', 'pandas', 'requests', 'beautifulsoup4', 'astor'] 
)
