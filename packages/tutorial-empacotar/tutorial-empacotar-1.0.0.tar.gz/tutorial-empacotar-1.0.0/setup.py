from setuptools import setup, find_packages

setup(
    name="tutorial-empacotar",
    version="1.0.0",
    package_dir={"": "src"},
    packages=find_packages(where="src", exclude=['test']),
)