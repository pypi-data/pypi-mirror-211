# This Python file uses the following encoding: utf-8
from setuptools import setup, find_packages

setup(name='MS_visualizer_lite',
      packages=find_packages(),
      version='0.0.1',
      description='Description.',
      long_description='Long description.',
      author=['ThiloSchild', 'David Teschner', 'MatteoLacki'],
      author_email='matteo.lacki@gmail.com',
      url='https://github.com/MatteoLacki/MS_visualizer2.git',
      keywords=['Great module', 'Devel Inside'],
      classifiers=['Development Status :: 1 - Planning',
                   'License :: OSI Approved :: BSD License',
                   'Intended Audience :: Science/Research',
                   'Topic :: Scientific/Engineering :: Chemistry',
                   'Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3.7'],
      install_requires=[
          'dash',
          'plotly',
          'pandas',
          'jsonschema',
          'opentimspy',
          'opentims_bruker_bridge',
          'dash-bootstrap-components==1.2.1',
          'flask_caching',
          'toml',
          'Flask',
      ],
      entry_points={
        'console_scripts': [
            'MS_visualize_lite = MS_visualize_lite.bin.run:main'
        ],
      }
      )
