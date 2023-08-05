# PyTraffic - Setup.py

''' This is the 'setup.py' file. '''

# Imports
from setuptools import setup, find_packages

# README.md
with open("README.md") as readme_file:
    README = readme_file.read()

# Setup Arguements
setup_args = dict (
    name="PyTraffic",
    version="1.1.8",
    description="PyTraffic is an advanced Python package to work on traffic-related functions and use cases.",
    long_description_content_type="text/markdown",
    long_description=README,
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    author="Aniketh Chavare",
    author_email="anikethchavare@outlook.com",
    keywords=["Traffic", "Traffic Density", "Traffic Density Estimation", "License Plates", "License Plate Detection", "License Plate Recognition", "Vehicles", "Vehicle Detection"],
    url="https://github.com/Anikethc/PyTraffic",
    download_url="https://pypi.org/project/PyTraffic"
)

# Install Requires
install_requires = ["opencv-python", "imutils", "numpy", "pytesseract", "pillow"]

# Run the Setup File
if __name__ == "__main__":
    setup(**setup_args, install_requires=install_requires)