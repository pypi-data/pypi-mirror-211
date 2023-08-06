from setuptools import setup

DIST_NAME = "pg_environment"
DIST_VERSION = "1.0.1"
__author__ = "baozilaji@gmail.com"

setup(
	name=DIST_NAME,
	version=DIST_VERSION,
	description="python game: environment",
	packages=['pg_environment'],
	author=__author__,
	python_requires='>=3',
	install_requires=[
		'pg-common>=0'
	],
)
