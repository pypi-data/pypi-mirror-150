from setuptools import find_packages, setup
import pathlib

with open(str(pathlib.Path(__file__).parent.absolute()) + "/fliton_fib_py/version.py", "r") as fh:
    version = fh.read().split("=")[1].replace("'", "")

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="fliton_fib_py",
    version=version,
    author="Adam Wong",
    author_email="wizzardcloud@gmail.com",
    description="Calculate Fibonacci number series",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AdamW666/fliton-fib-py",
    packages=find_packages(exclude=("tests",)),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'fib_number=fliton_fib_py.cmd.fib_numb:fib_numb',
        ]
    },
    install_requires=[
        "PyYAML>=4.1.2",
        "dill>=0.2.8"
    ],
    extra_require={
        "server": ["Flask>=1.0.0"]
    },
)
