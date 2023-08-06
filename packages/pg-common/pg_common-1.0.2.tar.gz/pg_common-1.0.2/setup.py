from setuptools import setup

DIST_NAME = "pg_common"
DIST_VERSION = "1.0.2"
__author__ = "baozilaji@gmail.com"

setup(
	name=DIST_NAME,
	version=DIST_VERSION,
	description="python game: common lib",
	packages=['pg_common'],
	author=__author__,
	python_requires='>=3'
)
