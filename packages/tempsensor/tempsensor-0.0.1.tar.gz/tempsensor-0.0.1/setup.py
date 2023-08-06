from setuptools import setup, find_packages
import os

ROOT_DIR='tempsensor'
with open(os.path.join(ROOT_DIR, 'VERSION')) as version_file:
    version = version_file.read().strip()

# read the contents of your README file
#this_directory = os.path.abspath(os.path.dirname(__file__))
#with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
#    long_description = f.read()    

setup(name='tempsensor',
      version=version,
      description='tempsensor: Tools to work with temperature sensor data',
      long_description='Tools to convert and fit temperature sensor data like NTC, thermocouple, platin sensors.',
      url='https://github.com/redvypr/tempsensor',
      author='Peter Holtermann',
      author_email='peter.holtermann@systemausfall.org',
      license='GPLv03',
      #packages=['redvypr'],
      packages=find_packages(),
      scripts = [],
      entry_points={},
      package_data = {'':['VERSION']},
      install_requires=[],
      classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Scientific/Engineering',          
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',  
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
      ],
      python_requires='>=3.5',
      zip_safe=False)
