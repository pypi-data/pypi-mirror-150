import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="kylinautosolve",
    version="1.0.6",
    description="The official client package of Kylin Autosolve for Python",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/kylin-public/kylin-autosolve-client-python",
    author="Kylin Team",
    author_email="kylinbot@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["kylinautosolve", 'kylinautosolve.pb', 'kylinautosolve.examples', 'kylinautosolve.rpc'],
    include_package_data=True,
    install_requires=["websockets", "pyee"],
    entry_points={
    },
)