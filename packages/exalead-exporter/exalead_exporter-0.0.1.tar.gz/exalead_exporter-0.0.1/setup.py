from exalead_exporter.constants import (PKG_NAME, PKG_VERSION)
from setuptools import setup, find_packages

# Global variables
name = PKG_NAME
version = PKG_VERSION

setup(
    name=name,
    version=version,
    description='A Python-based Exalead for Prometheus',
    long_description_content_type='text/markdown',
    long_description=open('README.md', 'r').read(),
    author="peekjef72",
    author_email="jfpik78@gmail.com",
    url="https://github.com/peekjef72/exalead_exporter",
    entry_points={
        'console_scripts': [
            'exalead_exporter = exalead_exporter.exalead_exporter:main',
            'build_exalead_exporter_conf = exalead_exporter.build_conf:main'
        ]
    },
    # package_dir={"": "exalead_exporter_package"},
    # packages=find_packages(where="exalead_exporter"),
    packages=find_packages(),
    install_requires=open('./requirements.txt').readlines(),

    package_data={
    	"exalead_exporter": ["conf/*.yml", "conf/metrics/*.yml"],
    },
)

