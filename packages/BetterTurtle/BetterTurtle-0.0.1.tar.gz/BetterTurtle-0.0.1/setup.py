from setuptools import setup

with open("README.md", "r") as fh:
	long_description = fh.read()

setup(
	name='BetterTurtle',
	version='0.0.1',
	description='A better turtle module for python. Uses turtle module to create a turtle object with additional functionality.',
	long_description=long_description,
	long_description_content_type="text/markdown",
	py_modules=["BetterTurtle"],
	package_dir={'': 'src'}
)