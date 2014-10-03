from setuptools import find_packages
from setuptools import setup

entry_points = """
    [paste.app_factory]
    main = testroutes:main
"""

setup(name='testroutes',
      version='0.1',
      packages=find_packages(),
      entry_points=entry_points)
