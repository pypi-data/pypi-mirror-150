import itertools
import os.path
import sys

from setuptools import find_packages, setup

# Don't import dishpill module here, since deps may not be installed
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "dishpill"))
from version import VERSION  # noqa:E402

# Environment-specific dependencies.
extras = {
    "pong": ["pygame==2.1.0"]
}

extras["all"] = list(
    itertools.chain.from_iterable(map(lambda group: extras[group], extras.keys()))
)

setup(
    name="dishpill",
    version=VERSION,
    description="corticallabs game environment",
    url="https://www.corticallabs.com/",
    author="Cortical labs",
    license="MIT",
    packages=[package for package in find_packages() if package.startswith("dishpill")],
    zip_safe=False,
    install_requires=[
        "numpy>=1.18.0",
        "cloudpickle>=1.2.0",
        "importlib_metadata>=4.10.0; python_version < '3.10'"
    ],
    extras_require=extras,
    package_data={
        "dishpill": [
            "py.typed",
        ]
    },
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
