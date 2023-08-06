"""Setup for the custom-utils package."""

from itertools import chain
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

EXTRAS_REQUIRE = {
    'slack': ['slack-sdk==3.21.3'],
    'mongodb': ['pymongo==3.10.0'],
    's3': ['boto', 'boto3', 'joblib'],
    'mysql':  ['SQLAlchemy', 'mysql-connector-python',],
    'bigquery': ['tqdm==4.49.0', 'google-cloud-bigquery==2.1.0', 'pandas_gbq', 'google-cloud'],

}

# construct special 'full' extra that adds requirements for all built-in
EXTRAS_REQUIRE['full'] = list(set(chain(*EXTRAS_REQUIRE.values())))

setup(
    author="Rahul Kumar",
    author_email="rahulnkumar7@gmail.com",
    name='custom-utils',
    description='Utilities for database connectors, slack alerter, loggers etc',
    version="0.0.313",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/RahulnKumar/custom-utils',
    packages=find_packages(),
    python_requires=">=3.6.9",
    install_requires=['python-dotenv', 'subprocess32',],
    extras_require=EXTRAS_REQUIRE,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Artificial Intelligence'
    ],
)
