from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='simple-arithmetic',
    version='0.0.1',
    description='Sample python package containing simple arithmetic functions',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LunaticFrisbee/sample-py-package",
    author='LunaticFrisbee (Avnish Chauhan)',
    author_email="avnishchauhan065@gmail.com",
    py_modules=['arithmetic'],
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)


# name => the name of the module people will use to import (pip install <name>) & doesn't need to be the same as the python code filename
# py_modules =>  list of the actual python code files that will be included in the package
# package_dir => a map telling setuptools that the code files are in the src directory
# install_requires => list of dependencies that will be installed when the package is installed