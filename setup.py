import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), "layercake", "__version__.py")) as version_file:
    exec(version_file.read())   # pylint: disable=W0122

_INSTALL_REQUIRES = [
    'munch',
]

setup(name="layercake",
      classifiers=[
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3.3",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5",
      ],
      description="Configuration stack",
      license="BSD3",
      author="Dror Levin",
      author_email="spatz@psybear.com",
      version=__version__,      # pylint: disable=E0602
      packages=find_packages(exclude=["tests"]),
      url="https://github.com/getslash/layercake",
      install_requires=_INSTALL_REQUIRES,
      scripts=[],
      namespace_packages=[],
)
