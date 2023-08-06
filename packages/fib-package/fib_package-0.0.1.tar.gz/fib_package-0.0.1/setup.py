from setuptools import find_packages, setup

with open("README.md", "r") as fh:
 long_description = fh.read()

setup(
    name="fib_package",
    version="0.0.1",
    author="Evandro Lippert",
    author_email="evandro.lippert@gmail.com",
    description="Calculates a Fibonacci number",
    url="https://github.com/EvandroLippert/fib_package",
    install_requires=[],
    packages=find_packages(exclude=("tests",)),
    long_description=long_description,
    classifiers=[
    "Development Status :: 4 - Beta",
    "Programming Language :: Python :: 3",
    "Operating System :: OS Independent",
    ],
    python_requires='>=3',
    tests_require=['pytest'],
    
    # To use the CLI script
    entry_points={
        'console_scripts': [
        'fib-number = \
        flitton_fib_py.cmd.fib_numb:fib_numb',
        ],
        },

)