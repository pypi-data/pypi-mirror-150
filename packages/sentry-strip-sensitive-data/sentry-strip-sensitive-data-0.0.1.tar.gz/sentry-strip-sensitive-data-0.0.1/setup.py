from setuptools import setup
import sentry_strip_sensitive_data

DESCRIPTION = "sentry strip sensitive data"
NAME = 'sentry-strip-sensitive-data'
AUTHOR = 'Go Nambu'
URL = 'https://github.com/go-nambu/sentry-strip-sensitive-data.git'
LICENSE = 'MIT'
DOWNLOAD_URL = 'https://github.com/go-nambu/sentry-strip-sensitive-data.git'
VERSION = sentry_strip_sensitive_data.__version__
PYTHON_REQUIRES = ">=3.6"

INSTALL_REQUIRES = []

EXTRAS_REQUIRE = {}

PACKAGES = [
    'sentry_strip_sensitive_data'
]

CLASSIFIERS = [
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3 :: Only',
]

setup(
        name=NAME,
        author=AUTHOR,
        maintainer=AUTHOR,
        description=DESCRIPTION,
        license=LICENSE,
        url=URL,
        version=VERSION,
        download_url=DOWNLOAD_URL,
        python_requires=PYTHON_REQUIRES,
        install_requires=INSTALL_REQUIRES,
        extras_require=EXTRAS_REQUIRE,
        packages=PACKAGES,
        classifiers=CLASSIFIERS
        )
