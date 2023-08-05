import pathlib
from setuptools import setup
HERE = pathlib.Path(__file__).parent
setup(
  name="gdwrapper",
  version="0.0.2",
  description="A Python API for Geometry Dash",
  author="Rylixmods SFC",
  author_email="rylixmods@gmail.com",
  license="MIT",
  packages=["gdwrapper"],
  install_requires=['requests'],
  zip_safe=False
)
