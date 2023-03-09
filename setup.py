from setuptools import setup

setup(name='pyMAP',
      version='0.1',
      description='Library for processing IMAP-lo Calibration data',
      url='http://https://github.com/jonbowr/pyMAP',
      author='J. S. Bower',
      author_email='jonathan.bower@unh.edu',
      license='NOSA',
      packages=['data','bowPy','tof'],
      install_requires=[
          'numpy',
          'pandas',
          'scipy',
          'matplotlib',
          'mpl_toolkits',
          'periodictable',
          'cStringIO',
          'sqlalchemy'
      ],
      zip_safe=False)